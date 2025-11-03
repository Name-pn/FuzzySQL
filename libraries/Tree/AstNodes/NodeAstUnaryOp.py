from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstUnaryOp(TreeAstNode):
    def __init__(self, op, value):
        super().__init__(TypeAst.UNARY_OP)
        self.op = op
        self.value = value