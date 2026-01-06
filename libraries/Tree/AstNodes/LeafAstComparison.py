from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstComparison(TreeAstNode):
    def __init__(self, op):
        super().__init__(TypeAst.COMPARISON)
        self.op = op