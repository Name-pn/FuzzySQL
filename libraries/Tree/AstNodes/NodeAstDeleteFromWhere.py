from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstDeleteFromWhere(TreeAstNode):
    def __init__(self, id, expr):
        super().__init__(TypeAst.DELETE_FROM_WHERE)
        self.id = id
        self.expr = expr