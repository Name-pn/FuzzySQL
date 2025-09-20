from tqdm import tqdm

from libraries.LR.LRUtils import LRUtils
from libraries.SetOfItems import SetOfItems


class LALRUtils(LRUtils):
    def getBase(self, state: SetOfItems):
        res = SetOfItems()
        for row, sym, letter in state.set:
            res.append((row, sym))
        st = set(res.set)
        #res = list(st)
        return st

    def getIndexesThatBase(self, base, all):
        res = []
        for index, el in enumerate(all):
            if base == self.getBase(el):
                res.append(index)
        return res

    def union(self, indexes, lst):
        st = SetOfItems()
        for index in indexes:
            for el in lst[index].set:
                st.append(el)
        st2 = set(st.set)
        st.set = list(st2)
        return st


    def combineBases(self):
        all = self.items()
        res = []
        st = set()
        for index, state in enumerate(tqdm(all, desc="Комбинирование состояний", unit="state")):#all):
            if not index in st:
                base = self.getBase(state)
                lst = self.getIndexesThatBase(base, all)
                uni = self.union(lst, all)
                res.append(uni)
                st.update(lst)
        return res

    def find(self, states: [SetOfItems], next: SetOfItems):
        base = self.getBase(next)
        for index, el in enumerate(states):
            st = set(self.getBase(el))
            if st == set(base):
                return index
        return -1