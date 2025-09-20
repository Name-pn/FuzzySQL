from libraries.Symbol.Symbol import Symbol
from libraries.Symbol.SymbolType import SymbolType

class EndSymbol(Symbol):
    def __init__(self):
        super().__init__("$", SymbolType.END_SYMBOL)
