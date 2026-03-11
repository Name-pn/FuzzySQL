from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, Optional

from libraries.Symbol.Terminal import TokenType


class SyntaxCategory(Enum):
    """Категории для подсветки синтаксиса"""
    KEYWORD = auto()  # Ключевые слова
    TYPE = auto()  # Типы данных
    STRING = auto()  # Строковые литералы
    NUMBER = auto()  # Числа
    COMMENT = auto()  # Комментарии
    OPERATOR = auto()  # Операторы
    FUNCTION = auto()  # Функции
    IDENTIFIER = auto()  # Идентификаторы
    PUNCTUATION = auto()  # Пунктуация
    SPECIAL = auto()  # Специальные токены


@dataclass
class SyntaxStyle:
    """Стиль для категории синтаксиса"""
    color: tuple[int, int, int]  # RGB
    bold: bool = False
    italic: bool = False
    underline: bool = False


class SyntaxTheme:
    """Тема подсветки синтаксиса"""

    def __init__(self):
        self.category_map: Dict[TokenType, SyntaxCategory] = self._build_category_map()
        self.styles: Dict[SyntaxCategory, SyntaxStyle] = self._build_default_theme()

    def _build_category_map(self) -> Dict[TokenType, SyntaxCategory]:
        """Маппинг типов токенов на категории"""
        return {
            # Ключевые слова SQL
            TokenType.SELECT: SyntaxCategory.KEYWORD,
            TokenType.FROM: SyntaxCategory.KEYWORD,
            TokenType.WHERE: SyntaxCategory.KEYWORD,
            TokenType.JOIN: SyntaxCategory.KEYWORD,
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
            # ... другие операторы

            # Идентификаторы
            TokenType.ID: SyntaxCategory.IDENTIFIER,

            # Пунктуация
            TokenType.COMMA: SyntaxCategory.PUNCTUATION,
            TokenType.DOT: SyntaxCategory.PUNCTUATION,
            TokenType.SEPARATOR: SyntaxCategory.PUNCTUATION,

            # Специальные
            TokenType.FUZZY_VALUE: SyntaxCategory.SPECIAL,
            TokenType.FUZZY_COLUMN: SyntaxCategory.SPECIAL,
        }

    def _build_default_theme(self) -> Dict[SyntaxCategory, SyntaxStyle]:
        """Стандартная тема (можно сделать настраиваемой)"""
        return {
            SyntaxCategory.KEYWORD: SyntaxStyle((86, 156, 214)),  # Синий
            SyntaxCategory.TYPE: SyntaxStyle((78, 201, 176)),  # Бирюзовый
            SyntaxCategory.STRING: SyntaxStyle((214, 157, 133)),  # Оранжевый
            SyntaxCategory.NUMBER: SyntaxStyle((181, 206, 168)),  # Зеленый
            SyntaxCategory.COMMENT: SyntaxStyle((87, 166, 74)),  # Темно-зеленый
            SyntaxCategory.OPERATOR: SyntaxStyle((255, 255, 255)),  # Белый
            SyntaxCategory.IDENTIFIER: SyntaxStyle((220, 220, 220)),  # Светло-серый
            SyntaxCategory.PUNCTUATION: SyntaxStyle((255, 255, 255)),  # Белый
            SyntaxCategory.SPECIAL: SyntaxStyle((197, 134, 192)),  # Фиолетовый
        }

    def get_style(self, token_type: TokenType) -> Optional[SyntaxStyle]:
        """Получает стиль для типа токена"""
        category = self.category_map.get(token_type)
        return self.styles.get(category) if category else None

class SyntaxController():
    def __init__(self, text):
        self.text = text