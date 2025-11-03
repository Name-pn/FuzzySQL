from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstFuzzyColomn(TreeAstNode):
    def __init__(self, id):
        super().__init__(TypeAst.FUZZY_COLOMN)
        self.id = id