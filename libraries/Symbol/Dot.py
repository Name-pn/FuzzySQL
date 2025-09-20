from libraries.Symbol.Symbol import Symbol
from libraries.Symbol.SymbolType import SymbolType

class Dot(Symbol):
    def __init__(self):
        super().__init__("•", SymbolType.DOT)