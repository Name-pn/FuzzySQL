from libraries.Symbol.EndSymbol import EndSymbol, END_SYMBOL
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
    def _on_reduce(self, state, symbol, action):
        raise NotImplementedError("Метод должен быть реализован в подклассе")

    @abc.abstractmethod
    def _on_shift(self, state, symbol):
        raise NotImplementedError("Метод должен быть реализован в подклассе")

    def _build_action_dict(self):
        """Вместо DataFrame возвращаем dict {(state, symbol): Action}"""
        self.action_dict = self.table.to_dict(orient='list')
        # Здесь логика заполнения из _create_table (или переделайте _create_table)
        # Пример:
        # for state in self.table:
        #     for sym in ...:
        #         val = self.table.loc[state, sym]
        #         self.action_dict[(state, sym)] = val

    def __init__(self, gr: Grammar, history_flag: bool = False):
        self.gr = gr
        self.table = self._create_table()
        self._build_action_dict()
        self.history_flag = history_flag
        if history_flag:
            self.historyColumns = ["Номер", "Стек", "Символы", "Вход", "Действие"]
            self.history = pd.DataFrame(columns=self.historyColumns)
        self.clear()

    def clear(self):
        self.stack = [0]

    def reduce_states(self, state, symbol, action):
        #prodIndex = self.table.loc[state, symbol].value
        prodIndex = action.value
        A = self.gr[prodIndex].head
        n = len(self.gr[prodIndex].body)
        if n > 0:
            del self.stack[-n:]
        #for i in range(n):
        #    self.stack.pop()
        state = self.stack[-1]
        self.stack.append(self.action_dict[A][state].value)

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
                symbol = END_SYMBOL
            action = self.action_dict[symbol][state]
            if action.type == CommandType.SHIFT:
                self._on_shift(state, symbol)
                self.stack.append(action.value)
                index += 1
            elif action.type == CommandType.REDUCE:
                self._on_reduce(state, symbol, action)
                self.reduce_states(state, symbol, action)
            elif action.type == CommandType.ACCEPT:
                self.clear()
                break
            else:
                self.clear()
                raise Exception(f"Ошибка анализа в позиции {index}")

    def recognize_debug(self, tokens: list[Symbol]):
        index = 0
        self.number = 0
        self.symbols = []
        while True:
            state = self.stack[-1]
            if index < len(tokens):
                symbol = tokens[index]
            else:
                symbol = END_SYMBOL
            action = self.action_dict[symbol][state]
            if action.type == CommandType.SHIFT:
                if self.history_flag:
                    self.history_add(tokens, index, CommandType.SHIFT)
                    self.symbols.append(tokens[index])  # .lexem
                self._on_shift(state, symbol)
                self.stack.append(action.value)
                index += 1
            elif action.type == CommandType.REDUCE:
                if self.history_flag:
                    self.history_add(tokens, index, CommandType.REDUCE)
                    self.reduce_symbols(state, symbol)
                self._on_reduce(state, symbol, action)
                self.reduce_states(state, symbol, action)
            elif action.type == CommandType.ACCEPT:
                if self.history_flag:
                    self.history_add(tokens, index, CommandType.ACCEPT)
                self.clear()
                break
            else:
                if self.history_flag:
                    self.history_add(tokens, index, CommandType.ERROR)
                self.clear()
                raise Exception(f"Ошибка анализа в позиции {index}")