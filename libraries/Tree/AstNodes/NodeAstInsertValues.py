from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstInsertValues(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.INSERT_VALUES)
        self.lst = lst