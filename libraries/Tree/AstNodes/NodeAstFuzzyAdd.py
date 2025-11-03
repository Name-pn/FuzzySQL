from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstFuzzyAdd(TreeAstNode):
    def __init__(self, id, a, b, c, d):
        super().__init__(TypeAst.FUZZY_ADD_COMMAND)
        self.id = id
        self.a = a
        self.b = b
        self.c = c
        self.d = d