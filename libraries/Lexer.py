import re
from typing import Optional, Pattern

from libraries.Environment import Environment
from libraries.Symbol.LTerminal import LTerminal
from libraries.Symbol.Terminal import Terminal, TokenType, TokenSpecification

class DefaultLexer():
    def __init__(self, env: Optional[Environment] = None):
        self.env = env
        self.values = [(value.type, value.pattern, value.is_literal, value.is_ignored) for value in tokenSpecificationTest]
        self._regex: Optional[Pattern] = None
        self._token_info: dict[str, tuple[TokenType, bool, bool]] = {}
        self._compile_regex()

    def _compile_regex(self):
        """
        Компилирует регулярное выражение из спецификации токенов.
        """
        patterns = []

        for token_type, pattern, is_literal, is_ignored in self.values:
            # Создаём уникальное имя группы
            group_name = f"t{token_type.value}"

            # Сохраняем информацию о токене для этой группы
            self._token_info[group_name] = (token_type, is_literal, is_ignored)

            # Добавляем паттерн в общее выражение
            patterns.append(f"(?P<{group_name}>{pattern})")

        # Собираем финальное регулярное выражение
        # Важно: порядок паттернов определяет приоритет!
        combined = "(?i)" + "|".join(patterns)
        self._regex = re.compile(combined)

    def tokenize(self, text: str) -> list[Terminal]:
        """
        Токенизирует входной текст.
        """
        tokens = []

        for match in self._regex.finditer(text):
            # Определяем, какая группа сработала
            for group_name, value in match.groupdict().items():
                if value is not None:
                    token_type, is_literal, is_ignored = self._token_info[group_name]

                    # Пропускаем игнорируемые токены
                    if is_ignored:
                        break

                    # Создаём соответствующий токен
                    if is_literal:
                        tokens.append(LTerminal(value, token_type))
                    else:
                        tokens.append(Terminal(token_type))

        return tokens

class SQLLexer():
    def __init__(self, env: Optional[Environment] = None):
        self.env = env
        self._regex: Optional[Pattern] = None
        self._token_info: dict[str, tuple[TokenType, bool, bool]] = {}
        self._compile_regex()

    def _compile_regex(self):
        """
        Компилирует регулярное выражение из спецификации токенов.
        """
        patterns = []

        for token_type, pattern, is_literal, is_ignored in TokenSpecification.get_patterns(self.env):
            # Создаём уникальное имя группы
            group_name = f"t{token_type.value}"

            # Сохраняем информацию о токене для этой группы
            self._token_info[group_name] = (token_type, is_literal, is_ignored)

            # Добавляем паттерн в общее выражение
            patterns.append(f"(?P<{group_name}>{pattern})")

        # Собираем финальное регулярное выражение
        # Важно: порядок паттернов определяет приоритет!
        combined = "(?i)" + "|".join(patterns)
        self._regex = re.compile(combined)

    def tokenize(self, text: str) -> list[Terminal]:
        """
        Токенизирует входной текст.
        """
        tokens = []

        for match in self._regex.finditer(text):
            # Определяем, какая группа сработала
            group_name = match.lastgroup
            value = match.group(group_name)
            token_type, is_literal, is_ignored = self._token_info[group_name]

            # Пропускаем игнорируемые токены
            if is_ignored:
                continue

            # Создаём соответствующий токен
            if is_literal:
                tokens.append(LTerminal(value, token_type))
            else:
                tokens.append(Terminal(token_type))

        return tokens

    def tokenize_with_positions_all_tokens(self, text: str) -> list[tuple[Terminal, int, int]]:
        """
        Токенизирует с сохранением позиций (для подсветки синтаксиса).
        """
        tokens = []

        for match in self._regex.finditer(text):
            for group_name, value in match.groupdict().items():
                if value is not None:
                    token_type, is_literal, is_ignored = self._token_info[group_name]

                    if is_literal:
                        token = LTerminal(value, token_type)
                    else:
                        token = Terminal(token_type)

                    tokens.append((
                        token,
                        match.start(),
                        match.end()
                    ))

        return tokens