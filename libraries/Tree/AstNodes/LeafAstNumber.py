from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstNumber(TreeAstNode):
    def __init__(self, value):
        super().__init__(TypeAst.NUMBER)
        self.value = value