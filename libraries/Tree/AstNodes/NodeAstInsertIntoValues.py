from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstInsertIntoValues(TreeAstNode):
    def __init__(self, id, lst):
        super().__init__(TypeAst.INSERT_INTO_VALUES)
        self.id = id
        self.lst = lst