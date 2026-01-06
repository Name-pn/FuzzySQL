from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstOrderList(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.ORDER_LIST)
        self.lst = lst