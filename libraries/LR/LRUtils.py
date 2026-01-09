import copy

from tqdm import tqdm

from libraries.Grammar.Grammar import Grammar
from libraries.SetOfItems import SetOfItems
from libraries.Symbol.Dot import Dot
from libraries.Symbol.EndSymbol import EndSymbol
from libraries.Symbol.Epsilon import Epsilon
from libraries.Symbol.Symbol import Symbol
from libraries.Symbol.SymbolType import SymbolType
from libraries.Utils import firstDict, firstSet


class LRUtils():
    def __init__(self, gr: Grammar):
        self.gr = gr
        self.firstDict = firstDict(gr)
        #self.followDict = followDict(gr)

    def closureLR(self, I: SetOfItems):
        J = copy.copy(I)
        f = True
        while f:
            f = False
            for pair in J.set:
                if pair[1] >= len(self.gr[pair[0]].body):
                    continue
                if self.gr[pair[0]].body[pair[1]].type != SymbolType.NONTERMINAL:
                    continue
                betta = self.gr[pair[0]].body[pair[1]+1:]
                betta.append(pair[2])
                #print(betta)
                #print(self.firstDict)
                els = firstSet(self.firstDict, betta)
                addition = self.gr[pair[0]].body[pair[1]].value
                for index, prod in enumerate(self.gr):
                    if prod.head.value == addition:
                        for el in els:
                            #if el == Epsilon():
                            #    pass
                            #el
                            if prod.body[0] == Epsilon() and not (index, 1, el) in J.set:
                                J.set.append((index, 1, el))
                                f = True
                            elif prod.body[0] != Epsilon() and not (index, 0, el) in J.set:
                                J.set.append((index, 0, el))
                                f = True
        return J

    def goto(self, I: SetOfItems, X:Symbol):
        f = True
        res = SetOfItems()
        while f:
            f = False
            for trio in I.set:
                if trio[1] >= len(self.gr[trio[0]].body):
                    continue
                if self.gr[trio[0]].body[trio[1]] == X and not (trio[0], trio[1] + 1, trio[2]) in res.set:
                    f = True
                    res.append((trio[0], trio[1] + 1, trio[2]))
        return self.closureLR(res)

    def grammar_to_states(self, I: SetOfItems):
        J = Grammar([])
        for row, sym, letter in I.set:
            rw = copy.deepcopy(self.gr[row])
            rw.body.arr.insert(sym, Dot())
            rw.letter = letter
            J.append(rw)
        return J

    def items(self):
        start = SetOfItems()
        start.append((0, 0, EndSymbol()))
        C = [self.closureLR(start)]
        S = self.gr.get_symbols()
        f = True
        pbar = tqdm(desc="Построение состояний", unit="итераций")
        while f:
            f = False
            for el in C:
                for s in S:
                    next_state = self.goto(el, s)
                    if not next_state.is_empty() and not next_state in C:
                        f = True
                        C.append(next_state)
                        pbar.set_postfix({"Состояний": len(C)})
            pbar.update(1)
        return C

    def get_states_str(self, states: list[SetOfItems]):
        index = 0
        states_str = ""
        for state in states:
            new_g = self.grammar_to_states(state)
            states_str = states_str + "I" + str(index) + "\n" + str(new_g) + "\n"
            index += 1
        return states_str
    def write_states(self, states: list[SetOfItems]):
        res = self.get_states_str(states)
        print(res)