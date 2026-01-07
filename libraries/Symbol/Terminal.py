from enum import Enum, auto

from libraries.Symbol.Symbol import Symbol
from libraries.Symbol.SymbolType import SymbolType

class CategoryRegex(Enum):
    UNDEF = r"312"
    FUZZY_VALUE = r"321"
    FUZZY_COLUMN = r"123"
    TYPE = r"\b(?:INT|INTEGER|REAL|DATE|INTERVAL|FUZZY|CHARACTER|CHAR|VARCHAR|BIT|FLOAT|TIME|TIMESTAMP|DEC|DECIMAL|NUMERIC)\b"
    #TYPE0 = r"\b(?:INT|INTEGER|REAL|DATE|INTERVAL|FUZZY)\b"
    #TYPE1 = r"\b(?:CHARACTER|CHAR|VARCHAR|BIT|FLOAT|TIME|TIMESTAMP)\b"
    #TYPE2 = r"\b(?:DEC|DECIMAL|NUMERIC)\b"
    ADD = r"\bADD\b"
    FSELECT = r"\bFSELECT\b"
    SELECT = r"\bSELECT\b"
    FROM = r"\bFROM\b"
    WHERE = r"\bWHERE\b"
    GROUP = r"\bGROUP\b"
    BY = r"\bBY\b"
    ORDER = r"\bORDER\b"
    ASC = r"\bASC\b"
    DESC = r"\bDESC\b"
    OR = r"\bOR\b"
    AND = r"\bAND\b"
    NOT = r"\bNOT\b"
    EXISTS = r"\bEXISTS\b"
    HAVING = r"\bHAVING\b"
    WITH = r"\bWITH\b"
    OUTER = r"\bOUTER\b"
    CROSS = r"\bCROSS\b"
    JOIN = r"\bJOIN\b"
    LEFT = r"\bLEFT\b"
    RIGHT = r"\bRIGHT\b"
    TABLE = r"\bTABLE\b"
    INNER = r"\bINNER\b"
    FULL = r"\bFULL\b"
    MODIFY = r"\bMODIFY\b"
    REMOVE = r"\bREMOVE\b"
    CREATE = r"\bCREATE\b"
    SET = r"\bSET\b"
    INSERT = r"\bINSERT\b"
    INTO = r"\bINTO\b"
    VALUES = r"\bVALUES\b"
    ALTER = r"\bALTER\b"
    RENAME = r"\bRENAME\b"
    DROP = r"\bDROP\b"
    UNIQUE = r"\bUNIQUE\b"
    PRIMARY = r"\bPRIMARY\b"
    KEY = r"\bKEY\b"
    DEFAULT = r"\bDEFAULT\b"
    NULL = r"\bNULL\b"
    UPDATE_R = r"\bUPDATE\b"
    DELETE_R = r"\bDELETE\b"
    #KEYWORD_R = r"\b(?:select|from|where|group|by|order|or|and|not|exists|having|join|left|right|" \
    #            r"table|inner|modify|remove|add|create|set|insert|into|values|alter|rename|drop|unique" \
    #            r"|primary|key|AUTO_INCREMENT)\b"
    ID_R = r"[A-Za-z][A-Za-z0-9_]*"
    DOT_R = r"\."
    COMMA_R = r"\,"
    SEPARATOR_R = r";"
    REAL_NUMBER_R = r"[0-9]+\.[0-9]*"
    NUMBER_R = r"[0-9]+"
    STRING_R = r"['][^']*[']"
    SPACE_R = r"\s+"
    COMMENT_R = r"\-\-[^\n\r]*"
    OPEN_BRACKET_R = r"\("
    CLOSE_BRACKET_R = r"\)"
    COLON_R = ":"
    EQUAL = "="
    COMPARISON = r"!=|>=|<=|<<|>>|=!|!=!|>!|<!|>=!|<=!|<>|[<>]"
    PLUS = r"\+"
    MINUS = r"-"
    MULTIPLICATION = r"\*"
    DIVIDE = r"\/"
    MOD = r"\%"
    EXPONENTIATION_R = r"[\^]"

class Category(Enum):
    UNDEF = 0
    FUZZY_VALUE = auto()
    FUZZY_COLUMN = auto()
    TYPE = auto()
    #TYPE0 = auto()
    #TYPE1 = auto()
    #TYPE2 = auto()
    ADD = auto()
    FSELECT = auto()
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    GROUP = auto()
    BY = auto()
    ORDER = auto()
    ASC = auto()
    DESC = auto()
    OR = auto()
    AND = auto()
    NOT = auto()
    EXISTS = auto()
    HAVING = auto()
    WITH = auto()
    OUTER = auto()
    CROSS = auto()
    JOIN = auto()
    LEFT = auto()
    RIGHT = auto()
    TABLE = auto()
    INNER = auto()
    FULL = auto()
    MODIFY = auto()
    REMOVE = auto()
    CREATE = auto()
    SET = auto()
    INSERT = auto()
    INTO = auto()
    VALUES = auto()
    ALTER = auto()
    RENAME = auto()
    DROP = auto()
    UNIQUE = auto()
    PRIMARY = auto()
    KEY = auto()
    DEFAULT = auto()
    NULL = auto()
    UPDATE = auto()
    DELETE = auto()
    #KEYWORD = 6
    ID = auto()
    DOT = auto()
    COMMA = auto()
    SEPARATOR = auto()
    REAL_NUMBER = auto()
    NUMBER = auto()
    STRING = auto()
    SPACE = auto()
    COMMENT = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    COLON = auto()
    EQUAL = auto()
    COMPARISON = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLICATION = auto()
    DIVIDE = auto()
    MOD = auto()
    EXPONENTIATION = auto()


class Terminal(Symbol):
    def __init__(self, terminal_type:Category = Category.UNDEF):
        super().__init__(terminal_type.name.lower(), SymbolType.TERMINAL)
        self.ttype = terminal_type

    def __str__(self):
        return str(self.value)