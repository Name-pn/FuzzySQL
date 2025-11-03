from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstRealNumber(TreeAstNode):
    def __init__(self, value):
        super().__init__(TypeAst.REAL_NUMBER)
        self.value = value