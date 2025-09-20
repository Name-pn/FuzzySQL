import enum

class CommandType(enum.Enum):
    ACCEPT = enum.auto()
    SHIFT = enum.auto()
    REDUCE = enum.auto()
    ERROR = enum.auto()
    STATE = enum.auto()

class LRCommand():
    def __init__(self, type: CommandType, value: int):
        self.type = type
        self.value = value

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __hash__(self):
        return hash((self.type, self.value))

    def __repr__(self):
        match (self.type):
            case CommandType.ERROR:
                return "Err"
            case CommandType.ACCEPT:
                return "Acc"
            case CommandType.REDUCE:
                return "r" + str(self.value)
            case CommandType.SHIFT:
                return "s" + str(self.value)
            case CommandType.STATE:
                return str(self.value)

class LRAccept(LRCommand):
    def __init__(self):
        super().__init__(CommandType.ACCEPT, -1)

class LRShift(LRCommand):
    def __init__(self, value):
        super().__init__(CommandType.SHIFT, value)

class LRReduce(LRCommand):
    def __init__(self, value):
        super().__init__(CommandType.REDUCE, value)

class LRError(LRCommand):
    def __init__(self):
        super().__init__(CommandType.ERROR, -1)

class LRState(LRCommand):
    def __init__(self, value):
        super().__init__(CommandType.STATE, value)