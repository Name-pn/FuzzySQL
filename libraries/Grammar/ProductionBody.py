from libraries.Symbol.Epsilon import Epsilon
from libraries.Symbol.Symbol import Symbol

class ProductionBody():
    def __init__(self, lst: list[Symbol]):
        self.arr = lst

    def __getitem__(self, item):
        return self.arr[item]

    def __str__(self):
        res = ""
        for el in self.arr:
            res += str(el) + " "
        return res[:-1]

    def __len__(self):
        if len(self.arr) == 1:
            if self.arr[0] == Epsilon():
                return 0
        return len(self.arr)