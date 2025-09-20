from libraries.Symbol.Epsilon import Epsilon
from libraries.Symbol.NonTerminal import NonTerminal
from libraries.Grammar.ProductionBody import ProductionBody


class Production():
    def __init__(self, head: NonTerminal, body: ProductionBody):
        self.head = head
        self.body = body
        self.letter = None
        self.isEps = False
        if body[0] == Epsilon():
            self.isEps = True

    def __str__(self):
        if self.letter is None:
            return str(self.head) + " -> " + str(self.body)
        else:
            return str(self.head) + " -> " + str(self.body) + ", " + str(self.letter)