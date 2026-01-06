from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstSelectWith(TreeAstNode):
    def __init__(self, val):
        super().__init__(TypeAst.SELECT_WITH)
        self.val = val