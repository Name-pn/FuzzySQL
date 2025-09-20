import copy

from libraries.Symbol.Dot import Dot
from libraries.Symbol.EndSymbol import EndSymbol
from libraries.Symbol.Epsilon import Epsilon
from libraries.Grammar.Grammar import Grammar
from libraries.SetOfItems import SetOfItems
from libraries.Symbol.Symbol import Symbol
from libraries.Symbol.SymbolType import SymbolType


def closure(I, G:Grammar):
    J = copy.copy(I)
    f = True
    while f:
        f = False
        for pair in J.set:
            if pair[1] >= len(G[pair[0]].body):
                continue
            if G[pair[0]].body[pair[1]].type != SymbolType.NONTERMINAL:
                continue
            addition = G[pair[0]].body[pair[1]].value
            for index, prod in enumerate(G):
                if prod.head.value == addition:
                    if prod.body[0] == Epsilon() and not (index, 1) in J.set:
                        J.set.append((index, 1))
                        f = True
                    elif prod.body[0] != Epsilon() and not (index, 0) in J.set:
                        J.set.append((index, 0))
                        f = True

    return J

def goto(I, G:Grammar, X:Symbol)->SetOfItems:
    f = True
    res = SetOfItems()
    while f:
        f = False
        for pair in I:
            if pair[1] >= len(G[pair[0]].body):
                continue
            if G[pair[0]].body[pair[1]] == X and not (pair[0], pair[1] + 1) in res.set:
                f = True
                res.append((pair[0], pair[1] + 1))
    return closure(res, G)

def grammar_to_states(I:SetOfItems, G:Grammar):
    J = Grammar([])
    for row, sym in I.set:
        rw = copy.deepcopy(G[row])
        rw.body.arr.insert(sym, Dot())
        J.append(rw)
    return J

def items(G:Grammar):
    start = SetOfItems()
    start.append((0, 0))
    C = [closure(start, G)]
    S = G.get_symbols()
    f = True
    while f:
        f = False
        for el in C:
            for s in S:
                next_state = goto(el.set, G, s)
                if not next_state.is_empty() and not next_state in C:
                    f = True
                    C.append(next_state)
    return C

def write_states(states: list[SetOfItems], G:Grammar):
    index = 0
    for state in states:
        new_g = grammar_to_states(state, G)
        print("I" + str(index))
        print(new_g)
        index += 1

def find(states: [SetOfItems], state: SetOfItems):
    for index, el in enumerate(states):
        if el == state:
            return index
    return -1

def tryFindNonterminalFirst(s: Symbol, gr:Grammar, d: dict):
    if not d.get(s) is None:
        res = d[s]
    else:
        res = set()
    for prod in gr:
        epsilon = True
        if prod.head == s:
            if prod.body[0] == Epsilon():
                res.add(Epsilon())
                continue
            for el in prod.body:
                if not d.get(el) is None:
                    new_set = d[el]
                    res = res.union(new_set)
                    if not Epsilon() in new_set:
                        epsilon = False
                        break
                else:
                    epsilon = False
                    break
            if epsilon:
                res.add(Epsilon())
    return res


def firstDict(gr: Grammar):
    d = dict()
    S = gr.get_symbols()
    flag = True
    while flag:
        flag = False
        for s in S:
            if s.type == SymbolType.TERMINAL:
                if d.get(s) is None:
                    st = set()
                    st.add(s)
                    d[s] = st
                    flag = True
            elif s.type == SymbolType.NONTERMINAL:
                test = tryFindNonterminalFirst(s, gr, d)
                if test and d.get(s) != test:
                    d[s] = test
                    flag = True
    return d

def tryFindNonterminalFollow(el:Symbol, gr:Grammar, followDict, firstDict):
    res = set()
    if not followDict.get(el) is None:
        res = followDict[el]
    if gr.start == el:
        res.add(EndSymbol())
    for prod in gr:
        for index, s in enumerate(prod.body):
            if s == el:
                next_s = None
                if index + 1 < len(prod.body):
                    next_s = prod.body[index + 1]
                if next_s is None:
                    res = res.union(followDict[prod.head])
                    continue
                add_head = True
                for i in range(index + 1, len(prod.body)):
                    next_s = prod.body[i]
                    if not Epsilon() in firstDict[next_s]:
                        res = res.union(firstDict[next_s])
                        add_head = False
                        break
                    elif Epsilon() in firstDict[next_s]:
                        st = firstDict[next_s]
                        st.remove(Epsilon())
                        res = res.union(st)
                if add_head:
                    res = res.union(followDict[prod.head])
    return res



def followDict(gr: Grammar):
    d = dict()
    first = firstDict(gr)
    S = gr.get_nonterminals()
    for el in S:
        d[el] = set()
    flag = True
    while flag:
        flag = False
        for s in S:
            test = tryFindNonterminalFollow(s, gr, d, first)
            if test and d.get(s) != test:
                d[s] = test
                flag = True
    return d

def firstSet(firstDict, string: list[Symbol])->set[Symbol]:
    res = set()
    n = len(string)
    eps = set()
    eps.add(Epsilon())
    for index, s in enumerate(string):
        if s == EndSymbol():
            res.add(EndSymbol())
            return res
        union_set = firstDict[s]
        res = res.union(union_set)
        if index != n - 1:
            res = set(res) - eps
        if not Epsilon() in union_set:
            #res.remove(Epsilon())
            return res
