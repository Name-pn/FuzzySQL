from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstSelectFrom(TreeAstNode):
    def __init__(self, expr):
        super().__init__(TypeAst.SELECT_FROM)
        self.expr = expr