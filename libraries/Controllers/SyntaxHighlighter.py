from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, Optional

from libraries.Lexer import SQLLexer
from libraries.Patterns.Tokenizer import Tokenizer
from libraries.Symbol.Terminal import TokenType, Terminal


class SyntaxCategory(Enum):
    """Категории для подсветки синтаксиса"""
    KEYWORD = auto()  # Ключевые слова
    TYPE = auto()  # Типы данных
    STRING = auto()  # Строковые литералы
    NUMBER = auto()  # Числа
    COMMENT = auto()  # Комментарии
    OPERATOR = auto()  # Операторы
    FUNCTION = auto()  # Функции
    SPECIAL = auto()  # Специальные токены
    IDENTIFIER = auto()  # Идентификаторы
    PUNCTUATION = auto()  # Пунктуация



@dataclass
class SyntaxStyle:
    """Стиль для категории синтаксиса"""
    color: tuple[int, int, int]  # RGB
    bold: bool = False
    italic: bool = False
    underline: bool = False


class SyntaxTheme:
    """Тема подсветки синтаксиса"""
    category_map: Optional[Dict[TokenType, SyntaxCategory]] = None
    styles: Optional[Dict[SyntaxCategory, SyntaxStyle]] = None

    @classmethod
    def _build_category_map(self) -> Dict[TokenType, SyntaxCategory]:
        """Маппинг типов токенов на категории"""
        return {
            # Ключевые слова SQL
            TokenType.SELECT: SyntaxCategory.KEYWORD,
            TokenType.FROM: SyntaxCategory.KEYWORD,
            TokenType.WHERE: SyntaxCategory.KEYWORD,
            TokenType.JOIN: SyntaxCategory.KEYWORD,
            TokenType.ADD: SyntaxCategory.KEYWORD,
            TokenType.FSELECT: SyntaxCategory.KEYWORD,
            TokenType.GROUP: SyntaxCategory.KEYWORD,
            TokenType.BY: SyntaxCategory.KEYWORD,
            TokenType.ORDER: SyntaxCategory.KEYWORD,
            TokenType.ASC: SyntaxCategory.KEYWORD,
            TokenType.DESC: SyntaxCategory.KEYWORD,
            TokenType.OR: SyntaxCategory.KEYWORD,
            TokenType.AND: SyntaxCategory.KEYWORD,
            TokenType.NOT: SyntaxCategory.KEYWORD,
            TokenType.EXISTS: SyntaxCategory.KEYWORD,
            TokenType.HAVING: SyntaxCategory.KEYWORD,
            TokenType.WITH: SyntaxCategory.KEYWORD,
            TokenType.OUTER: SyntaxCategory.KEYWORD,
            TokenType.CROSS: SyntaxCategory.KEYWORD,
            TokenType.LEFT: SyntaxCategory.KEYWORD,
            TokenType.RIGHT: SyntaxCategory.KEYWORD,
            TokenType.TABLE: SyntaxCategory.KEYWORD,
            TokenType.INNER: SyntaxCategory.KEYWORD,
            TokenType.FULL: SyntaxCategory.KEYWORD,
            TokenType.MODIFY: SyntaxCategory.KEYWORD,
            TokenType.REMOVE: SyntaxCategory.KEYWORD,
            TokenType.CREATE: SyntaxCategory.KEYWORD,
            TokenType.SET: SyntaxCategory.KEYWORD,
            TokenType.INSERT: SyntaxCategory.KEYWORD,
            TokenType.INTO: SyntaxCategory.KEYWORD,
            TokenType.VALUES: SyntaxCategory.KEYWORD,
            TokenType.ALTER: SyntaxCategory.KEYWORD,
            TokenType.RENAME: SyntaxCategory.KEYWORD,
            TokenType.DROP: SyntaxCategory.KEYWORD,
            TokenType.UNIQUE: SyntaxCategory.KEYWORD,
            TokenType.PRIMARY: SyntaxCategory.KEYWORD,
            TokenType.KEY: SyntaxCategory.KEYWORD,
            TokenType.DEFAULT: SyntaxCategory.KEYWORD,
            TokenType.NULL: SyntaxCategory.KEYWORD,
            TokenType.UPDATE: SyntaxCategory.KEYWORD,
            TokenType.DELETE: SyntaxCategory.KEYWORD,
            # ... все ключевые слова

            # Типы данных
            TokenType.TYPE: SyntaxCategory.TYPE,

            # Литералы
            TokenType.STRING: SyntaxCategory.STRING,
            TokenType.NUMBER: SyntaxCategory.NUMBER,
            TokenType.REAL_NUMBER: SyntaxCategory.NUMBER,

            # Операторы
            TokenType.EQUAL: SyntaxCategory.OPERATOR,
            TokenType.COMPARISON: SyntaxCategory.OPERATOR,
            TokenType.PLUS: SyntaxCategory.OPERATOR,
            TokenType.MINUS: SyntaxCategory.OPERATOR,
            TokenType.MULTIPLICATION: SyntaxCategory.OPERATOR,
            TokenType.DIVIDE: SyntaxCategory.OPERATOR,
            TokenType.MOD: SyntaxCategory.OPERATOR,
            TokenType.EXPONENTIATION: SyntaxCategory.OPERATOR,
            # ... другие операторы

            # Комментарий и пустые символы
            TokenType.COMMENT: SyntaxCategory.COMMENT,
            TokenType.SPACE: SyntaxCategory.COMMENT,

            # Специальные
            TokenType.FUZZY_VALUE: SyntaxCategory.SPECIAL,
            TokenType.FUZZY_COLUMN: SyntaxCategory.SPECIAL,

            # Идентификаторы
            TokenType.ID: SyntaxCategory.IDENTIFIER,

            # Пунктуация
            TokenType.COMMA: SyntaxCategory.PUNCTUATION,
            TokenType.DOT: SyntaxCategory.PUNCTUATION,
            TokenType.SEPARATOR: SyntaxCategory.PUNCTUATION,
            TokenType.COLON: SyntaxCategory.PUNCTUATION,


        }

    @classmethod
    def _build_default_theme(self) -> Dict[SyntaxCategory, SyntaxStyle]:
        """Стандартная тема (можно сделать настраиваемой)"""
        return {
            SyntaxCategory.KEYWORD: SyntaxStyle((86, 156, 214)),  # Синий
            SyntaxCategory.TYPE: SyntaxStyle((78, 201, 176)),  # Бирюзовый
            SyntaxCategory.STRING: SyntaxStyle((214, 157, 133)),  # Оранжевый
            SyntaxCategory.NUMBER: SyntaxStyle((181, 206, 168)),  # Зеленый
            SyntaxCategory.COMMENT: SyntaxStyle((197, 134, 192)),  # Фиолетовый
            SyntaxCategory.OPERATOR: SyntaxStyle((11, 2, 148)),  # Темно-синий
            SyntaxCategory.SPECIAL: SyntaxStyle((87, 166, 74)),  # Темно-зеленый
            SyntaxCategory.IDENTIFIER: SyntaxStyle((120, 120, 120)),  # серый
            SyntaxCategory.PUNCTUATION: SyntaxStyle((148, 99, 28)),  # Коричневый

        }

    @classmethod
    def get_style(cls, token_type: TokenType) -> Optional[SyntaxStyle]:
        """Получает стиль для типа токена"""
        if cls.category_map is None:
            cls.category_map = cls._build_category_map()
        if cls.styles is None:
            cls.styles = cls._build_default_theme()
        category = cls.category_map.get(token_type)
        return cls.styles.get(category) if category else None

class SyntaxHighlighter(Tokenizer):
    def __init__(self, lexer: SQLLexer):
        super().__init__(lexer)
        self.last_index = None

    def binary_search(self, array, index):
        l, r = 0, len(self.tokens)
        while l + 1 < r:
            m = (l + r) // 2
            if array[m][1] > index:
                r = m
            else:
                l = m
        return l

    def get_token_at_position(self, index_i, index_j)->Optional[Terminal]:
        if index_i >= len(self.string_starts):
            print("Нету массива позиций")
            return None
        if len(self.tokens) == 0:
            return None
        absolute_position = self.string_starts[index_i] + index_j
        # Если не было прошлого предсказания то юзаем бинарный поиск
        if self.last_index is None:
            index = self.binary_search(self.tokens, absolute_position)
            self.last_index = index
            return self.tokens[index][0]
        elif self.last_index < len(self.tokens):
            # А вот если было проверяем не является ли символом того же токена
            start = self.tokens[self.last_index][1]
            end = self.tokens[self.last_index][2]
            if absolute_position >= start and absolute_position < end:
                return self.tokens[self.last_index][0]
            elif self.last_index + 1 < len(self.tokens):
                start = self.tokens[self.last_index+1][1]
                end = self.tokens[self.last_index+1][2]
                if absolute_position >= start and absolute_position < end:
                    self.last_index = self.last_index + 1
                    return self.tokens[self.last_index][0]
                else:
                    index = self.binary_search(self.tokens, absolute_position)
                    self.last_index = index
                    return self.tokens[index][0]
            else:
                index = self.binary_search(self.tokens, absolute_position)
                self.last_index = index
                return self.tokens[index][0]
        else:
            index = self.binary_search(self.tokens, absolute_position)
            self.last_index = index
            return self.tokens[index][0]