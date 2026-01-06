from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstUpdate(TreeAstNode):
    def __init__(self, id, AList, where):
        super().__init__(TypeAst.VALUES)
        self.id = id
        self.AList = AList
        self.where = where