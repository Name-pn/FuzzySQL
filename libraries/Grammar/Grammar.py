from libraries.Symbol.Epsilon import Epsilon
from libraries.Symbol.NonTerminal import NonTerminal
from libraries.Grammar.Production import Production
from libraries.Symbol.SymbolType import SymbolType


class Grammar():
    def __init__(self, lst: list[Production], start: NonTerminal = NonTerminal("S")):
        self.start = start
        self.dict = lst

    def __str__(self):
        i = 0
        res = ""
        for el in self.dict:
            res += str(i) + " " + str(el) + "\n"
            i += 1
        return res

    def __len__(self):
        return self.dict.__len__()

    def __getitem__(self, item):
        return self.dict[item]

    def append(self, el):
        self.dict.append(el)

    def get_symbols(self):
        st = set()
        for el in self.dict:
            if not el.head in st:
                st.add(el.head)
            for s in el.body.arr:
                if not s in st:
                    st.add(s)
        if Epsilon() in st:
            st.remove(Epsilon())
        return st

    def get_terminals(self):
        s = self.get_symbols()
        res = []
        for el in s:
            if el.type == SymbolType.TERMINAL:
                res.append(el)
        return res

    def get_nonterminals(self):
        s = self.get_symbols()
        res = []
        for el in s:
            if el.type == SymbolType.NONTERMINAL:
                res.append(el)
        return res