from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstId(TreeAstNode):
    def __init__(self, value):
        super().__init__(TypeAst.ID)
        self.value = value