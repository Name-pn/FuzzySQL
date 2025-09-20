from libraries.Symbol.EndSymbol import EndSymbol
from libraries.Grammar.Grammar import Grammar
import pandas as pd

from libraries.Command import LRError, LRShift, LRReduce, LRAccept, LRState, CommandType
from libraries.Utils import items, followDict, goto, find

class SLRTable(pd.DataFrame):
    def __init__(self, gr:Grammar):
        S1 = gr.get_terminals()
        S1.append(EndSymbol())
        S2 = gr.get_nonterminals()
        S = S1 + S2
        states = items(gr)
        indexes = [i for i in range(len(states))]
        array = [[LRError() for el in S] for el in indexes]
        super().__init__(array, indexes, S)
        flws = followDict(gr)
        for i_state, state in enumerate(states):
            for s in S:
                next = goto(state.set, gr, s)
                if next.is_empty():
                    continue
                else:
                    j_state = find(states, next)
                    if j_state == -1:
                        raise Exception("Состояние не найдено")
                    if s.is_nonterminal():
                        self.check(i_state, s, LRState(j_state))
                        self.loc[i_state, s] = LRState(j_state)
                        continue
                    self.check(i_state, s, LRShift(j_state))
                    self.loc[i_state, s] = LRShift(j_state)

            for point in state.set:
                if len(gr[point[0]].body) <= point[1]:
                    if gr[point[0]].head == gr.start:
                        self.check(i_state, EndSymbol(), LRAccept())
                        self.loc[i_state, EndSymbol()] = LRAccept()
                        continue
                    symbols = flws[gr[point[0]].head]
                    for s in symbols:
                        self.check(i_state, s, LRReduce(point[0]))
                        self.loc[i_state, s] = LRReduce(point[0])
        print(self)

    def check(self, i_state, s, new_command):
        if self.loc[i_state, s] != LRError():
            if self.loc[i_state, s].type == CommandType.SHIFT and new_command.type == CommandType.REDUCE:
                raise Exception("Конфликт SR")
            elif self.loc[i_state, s].type == CommandType.REDUCE and new_command.type == CommandType.REDUCE:
                raise Exception("Конфликт RR")
            else:
                raise Exception("Конфликт которого не должно быть")