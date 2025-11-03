from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstColumnsID(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.COLUMNS_ID)
        self.lst = lst