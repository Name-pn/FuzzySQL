from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstMultiSelect(TreeAstNode):
    def __init__(self, sFrom, where, order):
        super().__init__(TypeAst.SELECT)
        self.sFrom = sFrom
        self.sWhere = where
        self.sOrder = order