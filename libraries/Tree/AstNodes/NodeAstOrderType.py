from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstOrderType(TreeAstNode):
    def __init__(self, asc = True):
        super().__init__(TypeAst.ORDER_TYPE)
        self.isAsc = asc