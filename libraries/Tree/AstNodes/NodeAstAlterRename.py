from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstAlterRename(TreeAstNode):
    def __init__(self, table_id, old_id, new_id):
        super().__init__(TypeAst.ALTER_RENAME)
        self.table_id = table_id
        self.old_id = old_id
        self.new_id = new_id