from enum import Enum, auto


class TypeAst(Enum):
    FUZZY_ADD_COMMAND = auto()
    FUZZY_MODIFY_COMMAND = auto()
    FUZZY_REMOVE_COMMAND = auto()
    FUZZY_SET_COMMAND = auto()

    COMMANDS = auto()
    ALTER_CREATE = auto()
    ALTER_ADD = auto()
    ALTER_MODIFY = auto()
    ALTER_DROP = auto()
    ALTER_RENAME = auto()
    SET = auto()
    INSERT_INTO = auto()
    INSERT_INTO_VALUES = auto()
    UPDATE = auto()
    ASSIGMENT = auto()
    ASSIGMENT_LIST = auto()
    DELETE_FROM = auto()
    DELETE_FROM_WHERE = auto()
    ORDER_LIST = auto()
    ORDER_EL = auto()
    ORDER_TYPE = auto()
    EMPTY = auto()
    WHERE = auto()
    REF_LIST = auto()
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
    UNARY_OP_MINUS = auto()
    UNARY_OP_PLUS = auto()
    UNARY_OP_NOT = auto()
    BIN_OP = auto()
    EXPR_LIST = auto()

    FULL_JOIN = auto()
    RIGHT_JOIN = auto()
    LEFT_JOIN = auto()
    INNER_JOIN = auto()
    CROSS_JOIN = auto()

    SELECT = auto()
    MULTI_SELECT = auto()
    SELECT_FROM = auto()
    SELECT_WITH = auto()

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
    COMPARISON = auto()



class TreeAstNode():
    def __init__(self, type: TypeAst):
        self.type = type
