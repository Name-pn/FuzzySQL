from enum import Enum, auto
from typing import Optional

from libraries.Environment import Environment
from libraries.Symbol.Symbol import Symbol
from libraries.Symbol.SymbolType import SymbolType
from dataclasses import dataclass
class TokenType(Enum):
    """Единый enum для всех типов токенов"""
    # ASTERISK = auto()
    # EQUAL_S = auto()
    # ID_VAR = auto()
    # Специальные токены
    UNDEF = auto()
    FUZZY_VALUE = auto()
    FUZZY_COLUMN = auto()

    # Типы данных
    TYPE = auto()

    # Ключевые слова SQL
    ADD = auto()
    FSELECT = auto()
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    GROUP = auto()
    BY = auto()
    ORDER = auto()
    ASC = auto()
    DESC = auto()
    OR = auto()
    AND = auto()
    NOT = auto()
    EXISTS = auto()
    HAVING = auto()
    WITH = auto()
    OUTER = auto()
    CROSS = auto()
    JOIN = auto()
    LEFT = auto()
    RIGHT = auto()
    TABLE = auto()
    INNER = auto()
    FULL = auto()
    MODIFY = auto()
    REMOVE = auto()
    CREATE = auto()
    SET = auto()
    INSERT = auto()
    INTO = auto()
    VALUES = auto()
    ALTER = auto()
    RENAME = auto()
    DROP = auto()
    UNIQUE = auto()
    PRIMARY = auto()
    KEY = auto()
    DEFAULT = auto()
    NULL = auto()
    UPDATE = auto()
    DELETE = auto()
    ON = auto()

    # Пробельные символы (игнорируем)
    SPACE = auto()
    COMMENT = auto()

    # Идентификаторы и литералы
    ID = auto()
    DOT = auto()
    COMMA = auto()
    SEPARATOR = auto()
    REAL_NUMBER = auto()
    NUMBER = auto()
    STRING = auto()
    COLON = auto()

    # Операторы
    EQUAL = auto()
    COMPARISON = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLICATION = auto()
    DIVIDE = auto()
    MOD = auto()
    EXPONENTIATION = auto()

    # Скобки
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()


@dataclass(frozen=True)
class TokenDefinition:
    """
    Определение токена: тип и регулярное выражение.
    Неизменяемый класс для безопасности.
    """
    type: TokenType
    pattern: str
    is_literal: bool = False  # True для токенов, которые нужно сохранять как литералы (ID, NUMBER, STRING)
    is_ignored: bool = False  # True для токенов, которые нужно игнорировать (SPACE, COMMENT)

    def __post_init__(self):
        """Валидация после создания"""
        if not self.pattern:
            raise ValueError(f"Pattern for {self.type} cannot be empty")

# tokenSpecificationTest = [
#     TokenDefinition(TokenType.EQUAL_S, "=", True, False),
#     TokenDefinition(TokenType.ID_VAR, "id", True, False),
#     TokenDefinition(TokenType.ASTERISK, r"\*", True, False)
# ]
class TokenSpecification:
    """
    Спецификация всех токенов языка.
    Единое место для определения грамматики.
    """

    # Базовые паттерны (для переиспользования)
    KEYWORDS = {
        TokenType.ADD: r"ADD",
        TokenType.ON: r"ON",
        TokenType.FSELECT: r"FSELECT",
        TokenType.SELECT: r"SELECT",
        TokenType.FROM: r"FROM",
        TokenType.WHERE: r"WHERE",
        TokenType.GROUP: r"GROUP",
        TokenType.BY: r"BY",
        TokenType.ORDER: r"ORDER",
        TokenType.ASC: r"ASC",
        TokenType.DESC: r"DESC",
        TokenType.OR: r"OR",
        TokenType.AND: r"AND",
        TokenType.NOT: r"NOT",
        TokenType.EXISTS: r"EXISTS",
        TokenType.HAVING: r"HAVING",
        TokenType.WITH: r"WITH",
        TokenType.OUTER: r"OUTER",
        TokenType.CROSS: r"CROSS",
        TokenType.JOIN: r"JOIN",
        TokenType.LEFT: r"LEFT",
        TokenType.RIGHT: r"RIGHT",
        TokenType.TABLE: r"TABLE",
        TokenType.INNER: r"INNER",
        TokenType.FULL: r"FULL",
        TokenType.MODIFY: r"MODIFY",
        TokenType.REMOVE: r"REMOVE",
        TokenType.CREATE: r"CREATE",
        TokenType.SET: r"SET",
        TokenType.INSERT: r"INSERT",
        TokenType.INTO: r"INTO",
        TokenType.VALUES: r"VALUES",
        TokenType.ALTER: r"ALTER",
        TokenType.RENAME: r"RENAME",
        TokenType.DROP: r"DROP",
        TokenType.UNIQUE: r"UNIQUE",
        TokenType.PRIMARY: r"PRIMARY",
        TokenType.KEY: r"KEY",
        TokenType.DEFAULT: r"DEFAULT",
        TokenType.NULL: r"NULL",
        TokenType.UPDATE: r"UPDATE",
        TokenType.DELETE: r"DELETE",
    }

    # Типы данных SQL
    _SQL_TYPES = r"INT|INTEGER|REAL|DATE|INTERVAL|FUZZY|CHARACTER|CHAR|VARCHAR|BIT|FLOAT|TIME|TIMESTAMP|DEC|DECIMAL|NUMERIC"

    # Все определения токенов
    DEFINITIONS = [
        # Ключевые слова (должны идти до ID)
        *[TokenDefinition(type, rf"\b{pattern}\b")
          for type, pattern in KEYWORDS.items()],

        # Типы данных
        TokenDefinition(TokenType.TYPE, rf"\b(?:{_SQL_TYPES})\b", is_literal=True),

        # Специальные префиксы (будут заменены динамически)
        TokenDefinition(TokenType.FUZZY_VALUE, r"\b{valueprefix}\b"),
        TokenDefinition(TokenType.FUZZY_COLUMN, r"\b{columnprefix}\b"),

        # Игнорируемые токены
        TokenDefinition(TokenType.SPACE, r"\s+", is_ignored=True),
        TokenDefinition(TokenType.COMMENT, r"--[^\n\r]*", is_ignored=True),

        # Идентификаторы и литералы
        TokenDefinition(TokenType.ID, r"[A-Za-z][A-Za-z0-9_]*", is_literal=True),
        TokenDefinition(TokenType.STRING, r"'[^']*'", is_literal=True),
        TokenDefinition(TokenType.REAL_NUMBER, r"[0-9]+\.[0-9]*", is_literal=True),
        TokenDefinition(TokenType.NUMBER, r"[0-9]+", is_literal=True),

        # Операторы
        TokenDefinition(TokenType.EQUAL, r"="),
        TokenDefinition(TokenType.COMPARISON, r"!=|>=|<=|<<|>>|=!|!=!|>!|<!|>=!|<=!|<>|[<>]", is_literal=True),
        TokenDefinition(TokenType.PLUS, r"\+"),
        TokenDefinition(TokenType.MINUS, r"-"),
        TokenDefinition(TokenType.MULTIPLICATION, r"\*"),
        TokenDefinition(TokenType.DIVIDE, r"/"),
        TokenDefinition(TokenType.MOD, r"%"),
        TokenDefinition(TokenType.EXPONENTIATION, r"\^"),

        # Пунктуация
        TokenDefinition(TokenType.DOT, r"\."),
        TokenDefinition(TokenType.COMMA, r","),
        TokenDefinition(TokenType.SEPARATOR, r";"),
        TokenDefinition(TokenType.COLON, r":"),
        TokenDefinition(TokenType.OPEN_BRACKET, r"\("),
        TokenDefinition(TokenType.CLOSE_BRACKET, r"\)"),
    ]

    @classmethod
    def get_patterns(cls, env: Optional[Environment] = None) -> list[tuple[TokenType, str, bool, bool]]:
        """
        Возвращает список паттернов с подстановкой динамических значений.
        """
        patterns = []

        for defn in cls.DEFINITIONS:
            pattern = defn.pattern

            # Подставляем динамические значения из окружения
            if env:
                pattern = pattern.replace("{valueprefix}", env.get('valueprefix'))
                pattern = pattern.replace("{columnprefix}", env.get('columnprefix'))

            patterns.append((
                defn.type,
                pattern,
                defn.is_literal,
                defn.is_ignored
            ))

        return patterns


class Terminal(Symbol):
    def __init__(self, terminal_type:TokenType = TokenType.UNDEF):
        super().__init__(terminal_type.name.lower(), SymbolType.TERMINAL)
        self.ttype = terminal_type

    def __str__(self):
        return str(self.value)