from libraries.Symbol.Epsilon import Epsilon
from libraries.Tree.TreeCst import TreeCstNode


class MixinCST():
    def __init__(self):
        self.parse_stack = []

    def _on_reduce(self, state, symbol):
        production = self.gr[self.table.loc[state, symbol].value]
        head = production.head
        length = len(production.body)
        node = TreeCstNode(head)
        if production.body[0] == Epsilon():
            length = 0
        if length > 0:
            node.children = self.parse_stack[-length:]
            del self.parse_stack[-length:]
        self.parse_stack.append(node)

    def _on_shift(self, state, symbol):
        self.parse_stack.append(TreeCstNode(symbol))

