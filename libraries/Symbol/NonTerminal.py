from libraries.Symbol.Symbol import Symbol
from libraries.Symbol.SymbolType import SymbolType

class NonTerminal(Symbol):
    def __init__(self, value):
        super().__init__(value, SymbolType.NONTERMINAL)

    def __str__(self):
        return str(self.value)