from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstSelect(TreeAstNode):
    def __init__(self, expr, sFrom, where, order, sWith):
        super().__init__(TypeAst.SELECT)
        self.sExpr = expr
        self.sFrom = sFrom
        self.sWhere = where
        self.sOrder = order
        self.sWith = sWith