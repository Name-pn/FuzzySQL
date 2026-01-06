from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstBinOp(TreeAstNode):
    def __init__(self, expr1, op, expr2):
        super().__init__(TypeAst.BIN_OP)
        self.expr1 = expr1
        self.op = op
        self.expr2 = expr2