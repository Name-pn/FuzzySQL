from libraries.Symbol.Terminal import Terminal, TokenType


class LTerminal(Terminal):
    def __init__(self, lexem:str, category: TokenType = TokenType.UNDEF):
        super().__init__(category)
        self.lexem = lexem

    # def __str__(self):
    #     return str(self.lexem)
    #
    # def __repr__(self):
    #     return str(self.lexem)