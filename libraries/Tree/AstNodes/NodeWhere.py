from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstWhere(TreeAstNode):
    def __init__(self, expr):
        super().__init__(TypeAst.WHERE)
        self.expr = expr
