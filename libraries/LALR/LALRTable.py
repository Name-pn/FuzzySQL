from libraries.LALR.LALRUtils import LALRUtils
from libraries.LR.LRUtils import LRUtils
from libraries.Symbol.EndSymbol import EndSymbol
from libraries.Grammar.Grammar import Grammar
import pandas as pd

from libraries.Command import LRError, LRShift, LRReduce, LRAccept, LRState, CommandType
from libraries.Utils import find
from tqdm import tqdm

class LALRTable(pd.DataFrame):
    def __init__(self, gr:Grammar):
        utils = LALRUtils(gr)
        S1 = gr.get_terminals()
        S1.append(EndSymbol())
        S2 = gr.get_nonterminals()
        S = S1 + S2
        states = utils.combineBases()
        #print(utils.write_states(states))
        indexes = [i for i in range(len(states))]
        array = [[LRError() for el in S] for el in indexes]
        super().__init__(array, indexes, S)
        for i_state, state in enumerate(tqdm(states, desc="Составление таблицы", unit="state")):#states):
            for s in S:
                next = utils.goto(state, s)
                if next.is_empty():
                    continue
                else:
                    j_state = utils.find(states, next)
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
                    s = point[2]
                    self.check(i_state, s, LRReduce(point[0]))
                    self.loc[i_state, s] = LRReduce(point[0])
        #print(self)

    def check(self, i_state, s, new_command):
        if self.loc[i_state, s] != LRError():
            if self.loc[i_state, s].type == CommandType.SHIFT and new_command.type == CommandType.REDUCE:
                raise Exception(f"Конфликт SR символ {s}, состояние {i_state} между сверткой {self.loc[i_state, s].value} и {new_command.value}")
            elif self.loc[i_state, s].type == CommandType.REDUCE and new_command.type == CommandType.REDUCE:
                raise Exception(f"Конфликт RR символ {s}, состояние {i_state} между сверткой {self.loc[i_state, s].value} и {new_command.value}")
            else:
                raise Exception("Конфликт которого не должно быть")