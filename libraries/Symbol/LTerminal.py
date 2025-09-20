from libraries.Symbol.Terminal import Terminal, Category


class LTerminal(Terminal):
    def __init__(self, lexem:str, category: Category = Category.UNDEF):
        super().__init__(category)
        self.lexem = lexem