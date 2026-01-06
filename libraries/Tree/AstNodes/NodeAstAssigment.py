from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstAssigment(TreeAstNode):
    def __init__(self, expr, id):
        super().__init__(TypeAst.ASSIGMENT)
        self.expr = expr
        self.id = id