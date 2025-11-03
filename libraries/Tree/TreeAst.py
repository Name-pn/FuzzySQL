from enum import Enum, auto


class TypeAst(Enum):
    FUZZY_ADD_COMMAND = auto()
    FUZZY_MODIFY_COMMAND = auto()
    FUZZY_REMOVE_COMMAND = auto()
    FUZZY_SET_COMMAND = auto()

    TYPE_NODE = auto()
    VALUES = auto()
    FUZZY_COLOMN = auto()
    FUZZY_VALUE = auto()
    COLUMNS_ID = auto()
    INSERT_VALUES = auto()
    COLUMN_NODE = auto()
    COLUMNS_NODE = auto()
    NAME_NODE = auto()
    UNARY_OP = auto()

    #ATTR = auto()
    ATTR_DEFAULT = auto()
    ATTR_UNIQUE = auto()
    ATTR_NULL = auto()
    ATTR_NOT_NULL = auto()
    ATTR_PRIMARY_KEY = auto()

    ATTRS = auto()

    NULL = auto()
    TYPE = auto()
    NUMBER = auto()
    REAL_NUMBER = auto()
    STRING = auto()
    ID = auto()



class TreeAstNode():
    def __init__(self, type: TypeAst):
        self.type = type
