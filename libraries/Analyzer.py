from libraries.Symbol.EndSymbol import EndSymbol
from libraries.Grammar.Grammar import Grammar
from libraries.Command import CommandType
from libraries.Symbol.Epsilon import Epsilon
from libraries.Symbol.Symbol import Symbol
import abc
import pandas as pd

from libraries.Tree import TreeNode


class Analyzer(abc.ABC):
    @abc.abstractmethod
    def _create_table(self):
        pass

    def __init__(self, gr: Grammar):
        self.gr = gr
        self.table = self._create_table()
        self.historyColumns = ["Номер", "Стек", "Символы", "Вход", "Действие"]
        self.history = pd.DataFrame(columns=self.historyColumns)
        self.clear()

    def clear(self):
        self.stack = [0]

    def reduce(self, state, symbol):
        prodIndex = self.table.loc[state, symbol].value
        A = self.gr[prodIndex].head
        n = len(self.gr[prodIndex].body)
        for i in range(n):
            self.stack.pop()
        state = self.stack[-1]
        self.stack.append(self.table.loc[state, A].value)

    def history_add(self, string, index, type: CommandType):
        state = self.stack[-1]
        if index < len(string):
            symbol = string[index]
        else:
            symbol = EndSymbol()
        prodIndex = self.table.loc[state, symbol].value
        symbols_with_end = self.symbols # + [EndSymbol()]
        d = {"Номер": self.number, "Стек": str(self.stack), "Символы": str(symbols_with_end), "Вход": str(string[index:]+[EndSymbol()]), "Действие": "---"}
        self.number += 1
        if type == CommandType.SHIFT:
            d["Действие"] = f"Перенос {string[index]}"
        elif type == CommandType.REDUCE:
            d["Действие"] = f"Свертка {str(self.gr[prodIndex])}"
        elif type == CommandType.ACCEPT:
            d["Действие"] = "Принятие"
        elif type == CommandType.ERROR:
            d["Действие"] = "Ошибка"
        else:
            d["Действие"] = "Undef"
        self.history = pd.concat([self.history, pd.DataFrame(data=d, index=[0])], ignore_index=True)

    def parse(self, string: list[Symbol]):
        index = 0
        self.number = 0
        self.symbols = []
        while True:
            state = self.stack[-1]
            if index < len(string):
                symbol = string[index]
            else:
                symbol = EndSymbol()
            try:
                self.table.loc[state, symbol]
            except KeyError as e:
                print(f"В таблице нет {symbol}")
                self.clear()
                #self.history_add(string, index, CommandType.ERROR)
                return False
            if self.table.loc[state, symbol].type == CommandType.SHIFT:
                self.history_add(string, index, CommandType.SHIFT)
                self.symbols.append(string[index])
                self.stack.append(self.table.loc[state, symbol].value)
                index += 1
            elif self.table.loc[state, symbol].type == CommandType.REDUCE:
                self.history_add(string, index, CommandType.REDUCE)
                prodIndex = self.table.loc[state, symbol].value
                A = self.gr[prodIndex].head
                n = len(self.gr[prodIndex].body)
                for i in range(n):
                    self.symbols.pop()
                self.symbols.append(A)
                self.reduce(state, symbol)
            elif self.table.loc[state, symbol].type == CommandType.ACCEPT:
                self.history_add(string, index, CommandType.ACCEPT)
                self.clear()
                break
            else:
                self.history_add(string, index, CommandType.ERROR)
                self.clear()
                return False
        return True

    def build_tree(self, string: list[Symbol]):
        if not self.parse(string):
            return None
        self.parse_stack = []
        index = 0
        self.number = 0
        while True:
            state = self.stack[-1]
            if index < len(string):
                symbol = string[index]
            else:
                symbol = EndSymbol()
            if self.table.loc[state, symbol].type == CommandType.SHIFT:
                self.stack.append(self.table.loc[state, symbol].value)
                self.parse_stack.append(TreeNode(string[index]))
                index += 1
            elif self.table.loc[state, symbol].type == CommandType.REDUCE:
                production = self.gr[self.table.loc[state, symbol].value]
                head = production.head
                length = len(production.body)
                node = TreeNode(head)
                if production.body[0] == Epsilon():
                    length = 0
                if length > 0:
                    node.children = self.parse_stack[-length:]
                    del self.parse_stack[-length:]
                self.parse_stack.append(node)
                self.reduce(state, symbol)
            elif self.table.loc[state, symbol].type == CommandType.ACCEPT:
                self.clear()
                if len(self.parse_stack) == 1:
                    return self.parse_stack[0]
                else:
                    raise Exception("В стеке много элементов")
            else:
                raise Exception(f"Ошибка синтаксического анализа в символе {index}")
