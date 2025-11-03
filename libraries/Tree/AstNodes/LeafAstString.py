from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstString(TreeAstNode):
    def __init__(self, value):
        super().__init__(TypeAst.STRING)
        self.value = value