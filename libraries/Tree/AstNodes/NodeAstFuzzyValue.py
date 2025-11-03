from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstFuzzyValue(TreeAstNode):
    def __init__(self, id):
        super().__init__(TypeAst.FUZZY_VALUE)
        self.id = id