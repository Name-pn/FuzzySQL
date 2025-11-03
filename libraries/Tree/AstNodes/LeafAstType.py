from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstType(TreeAstNode):
    def __init__(self, value):
        super().__init__(TypeAst.TYPE)
        self.value = value