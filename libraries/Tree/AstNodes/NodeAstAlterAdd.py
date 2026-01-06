from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstAlterAdd(TreeAstNode):
    def __init__(self, table_id, lst):
        super().__init__(TypeAst.ALTER_ADD)
        self.id = table_id
        self.lst = lst