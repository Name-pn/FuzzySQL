from libraries.Symbol.EndSymbol import EndSymbol
from libraries.Grammar.Grammar import Grammar
from libraries.Command import CommandType
from libraries.Symbol.Symbol import Symbol
import abc
import pandas as pd


class Analyzer(abc.ABC):
    @abc.abstractmethod
    def _create_table(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")

    @abc.abstractmethod
    def _on_reduce(self, state, symbol):
        raise NotImplementedError("Метод должен быть реализован в подклассе")

    @abc.abstractmethod
    def _on_shift(self, state, symbol):
        raise NotImplementedError("Метод должен быть реализован в подклассе")

    def __init__(self, gr: Grammar):
        self.gr = gr
        self.table = self._create_table()
        self.historyColumns = ["Номер", "Стек", "Символы", "Вход", "Действие"]
        self.history = pd.DataFrame(columns=self.historyColumns)
        self.clear()

    def clear(self):
        self.stack = [0]

    def reduce_states(self, state, symbol):
        prodIndex = self.table.loc[state, symbol].value
        A = self.gr[prodIndex].head
        n = len(self.gr[prodIndex].body)
        for i in range(n):
            self.stack.pop()
        state = self.stack[-1]
        self.stack.append(self.table.loc[state, A].value)

    def reduce_symbols(self, state, symbol):
        prodIndex = self.table.loc[state, symbol].value
        A = self.gr[prodIndex].head
        n = len(self.gr[prodIndex].body)
        for i in range(n):
            self.symbols.pop()
        self.symbols.append(A)

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

    def recognize(self, tokens: list[Symbol]):
        index = 0
        self.number = 0
        self.symbols = []
        while True:
            state = self.stack[-1]
            if index < len(tokens):
                symbol = tokens[index]
            else:
                symbol = EndSymbol()
            try:
                self.table.loc[state, symbol]
            except KeyError as e:
                print(f"В таблице нет {symbol}")
                self.clear()
                self.history_add(tokens, index, CommandType.ERROR)
                raise e
            if self.table.loc[state, symbol].type == CommandType.SHIFT:
                self.history_add(tokens, index, CommandType.SHIFT)
                self._on_shift(state, symbol)
                self.symbols.append(tokens[index])
                self.stack.append(self.table.loc[state, symbol].value)
                index += 1
            elif self.table.loc[state, symbol].type == CommandType.REDUCE:
                self.history_add(tokens, index, CommandType.REDUCE)
                self.reduce_symbols(state, symbol)
                self._on_reduce(state, symbol)
                self.reduce_states(state, symbol)
            elif self.table.loc[state, symbol].type == CommandType.ACCEPT:
                self.history_add(tokens, index, CommandType.ACCEPT)
                self.clear()
                break
            else:
                self.history_add(tokens, index, CommandType.ERROR)
                self.clear()
                raise Exception(f"Ошибка анализа в позиции {index}")

