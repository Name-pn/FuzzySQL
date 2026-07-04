import time
import tracemalloc
from pympler import asizeof
from pprint import pprint

# ANTLR4 импорты

from antlr4 import *
from antlr4.error.ErrorStrategy import DefaultErrorStrategy

from parser_data.gen.SqlLexer import SqlLexer as ANTLRSqlLexer
from parser_data.gen.SqlParser import SqlParser

from lexer_lib import RegexNFA, Match
from libraries.Symbol.LTerminal import LTerminal
from libraries.Symbol.Terminal import Terminal, TokenType, TokenSpecification

# Твои импорты
from libraries.Environment import Environment
from libraries.Lexer import SQLLexer
from libraries.Grammar.Grammar import Grammar
from libraries.LALR.LALRAnalyzerCST import LALRAnalyzerCST

# ========== Глобальная инициализация (ОДИН РАЗ) ==========
print("⏳ Инициализация парсеров...")

# Твой LALR парсер (таблица загружается один раз)
GRAMMAR_TABLE = Grammar.load("./parser_data/grammar.txt")
LALR_PARSER = LALRAnalyzerCST(GRAMMAR_TABLE)
TABLE = Environment()
TABLE.load("./parser_data/conf.pkl")
LEXER = SQLLexer(TABLE)
MY_LEXER = RegexNFA('test_lexer.txt')
SPECIFICATION = TokenSpecification.get_patterns(TABLE)
SPECIFICATION = sorted(SPECIFICATION, key=lambda x: x[0].value)
TOKEN_INFO = {}
for token_type, pattern, is_literal, is_ignored in SPECIFICATION:
    # Создаём уникальное имя группы
    group_name = f"t{token_type.value}"

    # Сохраняем информацию о токене для этой группы
    TOKEN_INFO[group_name] = (token_type, is_literal, is_ignored)
IGNORED = {48, 47}

# ANTLR парсер (инициализация лёгкая, без таблиц)
# Но тоже создадим глобальный экземпляр для честности
ANTLR_PARSER = None  # будет создан при первом вызове (или можно заранее)
dummy_stream = InputStream("")
ANTLR_LEXER = ANTLRSqlLexer(dummy_stream)
ANTLR_PARSER2 = SqlParser(CommonTokenStream(ANTLR_LEXER))

def get_antlr_parser():
    """Ленивая инициализация ANTLR парсера"""
    global ANTLR_PARSER
    if ANTLR_PARSER is None:
        # ANTLR не требует предварительной загрузки, просто создаём
        ANTLR_PARSER = True  # заглушка, реальный парсер создаётся в parse функции
    return ANTLR_PARSER


# ========== Обёртки для парсеров ==========

def antlr_parse(sql_text):
    """ANTLR4 парсер (создаёт лексер и парсер на каждый вызов)"""
    # 1. Создаём новый поток для запроса
    input_stream = InputStream(sql_text)
    # 2. Прямая установка нового ввода в лексер (работает в 100% случаев)
    ANTLR_LEXER._input = input_stream
    ANTLR_LEXER._token = None
    ANTLR_LEXER._tokenStartCharIndex = -1
    ANTLR_LEXER._tokenStartLine = -1
    ANTLR_LEXER._tokenStartColumn = -1
    ANTLR_LEXER._hitEOF = False

    # 3. Получаем токены и устанавливаем их в парсер
    stream = CommonTokenStream(ANTLR_LEXER)
    ANTLR_PARSER2._input = stream

    # 4. Сброс парсера
    ANTLR_PARSER2._ctx = None
    ANTLR_PARSER2._errHandler = DefaultErrorStrategy()
    ANTLR_PARSER2.reset()

    # 5. Парсинг
    tree = ANTLR_PARSER2.start()
    return tree
    # input_stream = InputStream(sql_text)
    # lexer = ANTLRSqlLexer(input_stream)
    # stream = CommonTokenStream(lexer)
    # parser = SqlParser(stream)
    # tree = parser.start()
    # return tree


def lalr_parse(sql_text):
    lexer = LEXER
    tokens = lexer.tokenize(sql_text)
    #print(tokens, "lalr")
    tree = LALR_PARSER.parse(tokens)  # используем глобальный экземпляр
    return tree

def match_to_lexem(text: str, lexer):
    match = lexer.next()
    while match is not None and match.pattern_id in IGNORED:
        match = lexer.next()
    if match is None:
        return None
    match_type = TokenType(match.pattern_id)
    if not TOKEN_INFO[f"t{match_type.value}"][1]:
        return Terminal(match_type)
    return LTerminal(text[match.start_index:match.end_index], match_type)

def my_lexer_parse(sql_text):
    sql_text = sql_text.lower()
    lexer = MY_LEXER
    tokens = []
    #pprint(SPECIFICATION, indent=2, width=80)
    lexer.setAnalize(sql_text)
    # token = lexer.next()
    # while token is not None:
    #     if not token.pattern_id in IGNORED:
    #         tokens.append(match_to_lexem(token, sql_text))
    #     token = lexer.next()
    #print(tokens)
    #exit(0)
    tree = LALR_PARSER.parse_by_stream(lambda: match_to_lexem(sql_text, lexer))  # используем глобальный экземпляр
    return tree


# ========== Бенчмарк (остаётся без изменений) ==========

TEST_ITERATIONS = 50

TEST_QUERIES = {
    'small': "SELECT * FROM users;",

    'medium': """
        SELECT id, name, age FROM users WHERE age > 18;
        INSERT INTO logs (user_id, action) VALUES (1, 'login');
        UPDATE users SET age = 19 WHERE id = 1;
        DELETE FROM sessions WHERE user_id = 1;
    """ * 25,

    'large': """
        SELECT id, name, email, created_at FROM users WHERE active = 1 ORDER BY created_at;
        SELECT orders.id, users.name, orders.total, orders.amount_prices FROM orders WHERE fv:big_amount < fc:amount_prices;
        FSELECT name, numbers, price FROM products WHERE price = fv:big_price OR price = fv:medium_price;
    """ * 50,

    'huge': """
        SELECT id, name, email, created_at FROM users WHERE active = 1 ORDER BY created_at;
        SELECT orders.id, users.name, orders.total, orders.amount_prices FROM orders INNER JOIN users ON orders.user_id = users.id WHERE fv:big_amount < fc:amount_prices;
        FSELECT name, numbers, price FROM products WHERE price = fv:big_price OR price = fv:medium_price;
    """ * 500
}


def benchmark_parser(parse_func, input_data, iterations=TEST_ITERATIONS):
    """Замер времени"""
    # Прогрев (3 итерации)
    for _ in range(3):
        try:
            parse_func(input_data)
        except Exception as e:
            print(f"  Ошибка при прогреве: {e}")
            return None

    times = []
    for i in range(iterations):
        start = time.perf_counter()
        try:
            result = parse_func(input_data)
            end = time.perf_counter()
            times.append(end - start)
        except Exception as e:
            print(f"  Ошибка на итерации {i}: {e}")
            return None

    if not times:
        return None

    return {
        'avg': sum(times) / len(times),
        'min': min(times),
        'max': max(times),
        'total': sum(times),
        'iterations': len(times)
    }


def measure_memory(parse_func, input_data):
    """Замер пикового потребления памяти (в MB)"""

    import gc
    gc.collect()

    tracemalloc.start()

    result = parse_func(input_data)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print("size ", asizeof.asizeof(result))
    # Возвращаем пик в байтах (или КБ/МБ)
    return peak

def bytes_to_vis_format(bytes: int) -> str:
    index = 0
    array = ["B", "KB", "MB", "GB"]
    if bytes == float('inf'):
        return "-"
    while bytes > 1024:
        index += 1
        bytes /= 1024
    return f"{bytes:.2f} {array[index]}"

def run_complete_benchmark():
    print("=" * 60)
    print("🚀 Сравнение производительности парсеров")
    print("=" * 60)
    print(f"📋 Таблица LALR загружена один раз (глобально)")
    print(f"🔄 Количество итераций: {TEST_ITERATIONS}")
    print()

    results = {}

    for name, sql in TEST_QUERIES.items():
        print(f"\n📊 Тест: {name.upper()} ({len(sql)} символов)")
        print("-" * 40)

        # ANTLR4
        print("  ⏳ Замер ANTLR4...")
        antlr_time = benchmark_parser(antlr_parse, sql)
        antlr_mem = measure_memory(antlr_parse, sql) if antlr_time else None

        print("  ⏳ Замер LALR(1)...")
        lalr_time = benchmark_parser(lalr_parse, sql)
        lalr_mem = measure_memory(lalr_parse, sql) if lalr_time else None

        print("  ⏳ Замер моего лексера LALR(1)...")
        my_lexer_time = benchmark_parser(my_lexer_parse, sql)
        my_lexer_mem = measure_memory(my_lexer_parse, sql) if lalr_time else None

        # Результаты
        if antlr_time and lalr_time:
            speed_ratio = lalr_time['avg'] / antlr_time['avg']
            faster = "🚀 LALR(1)" if speed_ratio < 1 else "🐍 ANTLR4"
            smaller = "🚀 LALR(1)" if lalr_mem < antlr_mem else "🐍 ANTLR4"
            speed_factor = 1 / speed_ratio if speed_ratio < 1 else speed_ratio

            print(f"\n  📈 РЕЗУЛЬТАТЫ:")
            print(f"     ANTLR4:  {antlr_time['avg'] * 1000:.3f} мс (среднее), {antlr_mem:.2f} B")
            print(f"     LALR(1): {lalr_time['avg'] * 1000:.3f} мс (среднее), {lalr_mem:.2f} B")
            print(f"     {faster} быстрее в {speed_factor:.2f}x")
            print(f"     my lexer {my_lexer_time['avg'] * 1000:.3f} мс (среднее), {my_lexer_mem:.2f} B")

            results[name] = {
                'my_lexer': {'avg_ms': my_lexer_time['avg'] * 1000, 'memory_mb': my_lexer_mem},
                'antlr': {'avg_ms': antlr_time['avg'] * 1000, 'memory_mb': antlr_mem},
                'lalr': {'avg_ms': lalr_time['avg'] * 1000, 'memory_mb': lalr_mem},
                'ratio': speed_ratio,
                'faster': faster,
                'smaller': smaller
            }
        elif antlr_time or lalr_time:
            if lalr_time:
                faster = "🚀 LALR(1)"
                smaller = "🚀 LALR(1)"
                print(f"\n  📈 РЕЗУЛЬТАТЫ:")
                print(f"     ANTLR4:  - мс (среднее), - B")
                print(f"     LALR(1): {lalr_time['avg'] * 1000:.3f} мс (среднее), {lalr_mem:.2f} B")
                print(f"     {faster} быстрее в")
                #print(f"     my lexer {my_lexer_time['avg'] * 1000:.3f} мс (среднее), {my_lexer_mem:.2f} B")

                results[name] = {
                    'my_lexer': {'avg_ms': my_lexer_time['avg'] * 1000, 'memory_mb': my_lexer_mem},
                    'lalr': {'avg_ms': lalr_time['avg'] * 1000, 'memory_mb': lalr_mem},
                    'faster': faster,
                    'ratio': 0,
                    'antlr': {'avg_ms': float('inf'), 'memory_mb': float('inf')},
                    'smaller': smaller
                }
            else:
                faster = "🐍 ANTLR4"
                smaller = "🐍 ANTLR4"
                print(f"\n  📈 РЕЗУЛЬТАТЫ:")
                print(f"     ANTLR4:  {antlr_time['avg'] * 1000:.3f} мс (среднее), {antlr_mem:.2f} B")
                print(f"     LALR(1): - мс (среднее), - B")
                #print(f"     my lexer {my_lexer_time['avg'] * 1000:.3f} мс (среднее), {my_lexer_mem:.2f} B")
                results[name] = {
                    'my_lexer': {'avg_ms': my_lexer_time['avg'] * 1000, 'memory_mb': my_lexer_mem},
                    'antlr': {'avg_ms': antlr_time['avg'] * 1000, 'memory_mb': antlr_mem},
                    'faster': faster,
                    'ratio': 0,
                    'lalr': {'avg_ms': float('inf'), 'memory_mb': float('inf')},
                    'smaller': smaller
                }
        else:
            print(f"\n  ❌ Ошибка при выполнении обоих парсеров")
            results[name] = {'error': True}

    # Итоговая таблица
    print("\n" + "=" * 60)
    print("📋 СВОДНАЯ ТАБЛИЦА СКОРОСТЕЙ")
    print("=" * 60)
    print(f"{'Тест':<12} {'ANTLR4 (мс)':<15} {'LALR(1) (мс)':<15} {'Победитель':<20} {"MY_LEXER":<15}")
    print("-" * 77)
    for name, data in results.items():
        if 'error' in data:
            print(f"{name:<12} {'ОШИБКА':<15} {'ОШИБКА':<15} {'-':<20} {'ОШИБКА':<15}")
        else:
            antlr_ms = data['antlr']['avg_ms']
            lalr_ms = data['lalr']['avg_ms']
            my_lexer = data['my_lexer']['avg_ms']
            print(f"{name:<12} {antlr_ms:<15.3f} {lalr_ms:<15.3f} {data['faster']:<20} {my_lexer:<15.3f}")

    # Итоговая таблица
    print("\n" + "=" * 60)
    print("📋 СВОДНАЯ ТАБЛИЦА ПАМЯТИ")
    print("=" * 60)
    print(f"{'Тест':<12} {'ANTLR4 (память)':<15} {'LALR(1) (память)':<15} {'Победитель':<20} {"MY_LEXER":<15}")
    print("-" * 77)
    for name, data in results.items():
        if 'error' in data:
            print(f"{name:<12} {'ОШИБКА':<15} {'ОШИБКА':<15} {'-':<20} {'ОШИБКА':<15}")
        else:
            my_lexer = data['my_lexer']['memory_mb']
            antlr_mem = data['antlr']['memory_mb']
            lalr_mem = data['lalr']['memory_mb']
            print(f"{name:<12} {bytes_to_vis_format(antlr_mem):<15} {bytes_to_vis_format(lalr_mem):<15} {data['smaller']:<20} {bytes_to_vis_format(my_lexer):<15}")

    return results


if __name__ == "__main__":

    input("Нажми Enter для запуска бенчмарка...")
    results = run_complete_benchmark()