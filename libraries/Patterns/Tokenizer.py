from libraries.Lexer import SQLLexer
from libraries.Patterns.Observer import Observer


class Tokenizer(Observer):
    def __init__(self, lexer: SQLLexer):
        self.lexer = lexer
        self.tokens = None
        self.text_string = None
        self.string_starts = []

    def _init_string_starts(self, string):
        self.string_starts = [0]
        for i, c in enumerate(string):
            if c == '\n':
                self.string_starts.append(i + 1)

    def update(self, payload):
        self.text_string = payload
        self._init_string_starts(payload)
        self.tokens = self.lexer.tokenize_with_positions_all_tokens(payload)