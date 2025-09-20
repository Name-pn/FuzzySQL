from libraries.Symbol.SymbolType import SymbolType


class Symbol:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __hash__(self):
        return hash((self.value, self.type))

    def __eq__(self, other):
        return self.value == other.value and self.type == other.type

    def is_nonterminal(self):
        return self.type == SymbolType.NONTERMINAL

    def is_terminal(self):
        return self.type == SymbolType.TERMINAL
#def is_equal(X: Symbol, Y:Symbol):
#    return X.value == Y.value and X.type == Y.type