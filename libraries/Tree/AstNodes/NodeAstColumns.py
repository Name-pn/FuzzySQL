from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstColumns(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.COLUMNS_NODE)
        self.lst = lst