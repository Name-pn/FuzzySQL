from enum import Enum, auto

class SymbolType(Enum):
    TERMINAL = auto()
    NONTERMINAL = auto()
    DOT = auto()
    EPSILON = auto()
    END_SYMBOL = auto()