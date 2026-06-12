from enum import Enum, auto
class SymbolType(Enum):
    TERMINAL = auto()
    NONTERMINAL = auto()
    DOT = auto()
    EPSILON = auto()
    END_SYMBOL = auto()

# from venum import Enum
#
# SymbolType = Enum(('TERMINAL', 0),
#               ('NONTERMINAL', 1),
#               ('DOT', 2),
#               ('EPSILON', 3),
#               ('END_SYMBOL', 4))