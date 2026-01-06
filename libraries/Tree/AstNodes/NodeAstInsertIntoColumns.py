from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstInsertIntoColumns(TreeAstNode):
    def __init__(self, id, lstColumns, lstValues):
        super().__init__(TypeAst.INSERT_INTO_VALUES)
        self.id = id
        self.lstColumns = lstColumns
        self.lstValues = lstValues