from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstFuzzyRemove(TreeAstNode):
    def __init__(self, id):
        super().__init__(TypeAst.FUZZY_REMOVE_COMMAND)
        self.id = id