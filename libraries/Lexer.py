import re

from libraries.Environment import Environment
from libraries.Symbol.LTerminal import LTerminal
from libraries.Symbol.Terminal import CategoryRegex, Terminal, Category


class SQLLexer():
    def __init__(self, env: Environment):
        self.regex = "(?i)"
        for index, cat in enumerate(CategoryRegex, 0):
            if index == 0:
                pass
            elif index == 1:
                self.regex = self.regex + fr"(?P<g{index}>\b{env.get('valueprefix')}\b)|"
            elif index == 2:
                self.regex = self.regex + fr"(?P<g{index}>\b{env.get('columnprefix')}\b)|"
            else:
                self.regex = self.regex + f"(?P<g{index}>{cat.value})|"
        self.regex = self.regex[:-1]
        #print(self.regex[:])
        #print(self.regex)
        self.regex = re.compile(self.regex)

    def add_token(self, lst, index, lexem):
        match (index):
            case Category.SPACE.value | Category.COMMENT.value:
                pass
            case Category.FUZZY_VALUE.value | Category.FUZZY_COLUMN.value | Category.DOT.value | Category.COMMA.value | Category.SEPARATOR.value | Category.OPEN_BRACKET.value | Category.CLOSE_BRACKET.value | Category.SELECT.value | Category.FROM.value | Category.WHERE.value | Category.GROUP.value | Category.BY.value | Category.ORDER.value | Category.OR.value | Category.AND.value | Category.NOT.value | Category.EXISTS.value | Category.HAVING.value | Category.JOIN.value | Category.LEFT.value | Category.RIGHT.value | Category.TABLE.value | Category.INNER.value | Category.MODIFY.value | Category.REMOVE.value | Category.ADD.value | Category.CREATE.value | Category.SET.value | Category.INSERT.value | Category.INTO.value | Category.VALUES.value | Category.ALTER.value | Category.RENAME.value | Category.DROP.value | Category.UNIQUE.value | Category.PRIMARY.value | Category.KEY.value | Category.DEFAULT.value | Category.NULL.value | Category.DELETE.value | Category.COLON.value | Category.UPDATE.value | Category.EQUAL.value | Category.MULTIPLICATION.value | Category.ASC.value | Category.DESC.value | Category.WITH.value | Category.FSELECT.value:
                lst.append(Terminal(Category(index)))
            # | Category.TYPE1.value | Category.TYPE2.value
            case Category.TYPE.value | Category.ID.value | Category.REAL_NUMBER.value | Category.NUMBER.value | Category.STRING.value | Category.EQUAL.value | Category.COMPARISON.value | Category.PLUS.value | Category.MINUS.value | Category.MOD.value | Category.DIVIDE.value | Category.MULTIPLICATION.value | Category.EXPONENTIATION.value:
                lst.append(LTerminal(lexem, Category(index)))
            case _:
                print(f"Лексема {lexem}, индекс {index}")
                print("Неопознанный токен")


    def tokenize(self, query: str) -> [Terminal]:
        matches = self.regex.finditer(query)
        res = []
        for match in matches:
            # Исключая токены с отступами и комментарии заполняем res
            #if match.lastindex != Category.SPACE.value and match.lastindex != Category.COMMENT.value:
            self.add_token(res, match.lastindex, match[match.lastgroup])
                #res.append(Terminal(Category(match.lastindex), match[match.lastgroup]))
        #for i in res:
        #   print(i)
        return res