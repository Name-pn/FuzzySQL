from libraries.Symbol.Symbol import Symbol
from libraries.Symbol.SymbolType import SymbolType

class Epsilon(Symbol):
    def __init__(self):
        super().__init__("ε", SymbolType.EPSILON)
