from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstOrderEl(TreeAstNode):
    def __init__(self, expr, orderType):
        super().__init__(TypeAst.ORDER_EL)
        self.expr = expr
        self.orderType = orderType