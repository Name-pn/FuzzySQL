from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstValues(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.VALUES)
        self.lst = lst