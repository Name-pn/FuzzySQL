from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstSet(TreeAstNode):
    def __init__(self, id, val):
        super().__init__(TypeAst.SET)
        self.id = id
        self.val = val