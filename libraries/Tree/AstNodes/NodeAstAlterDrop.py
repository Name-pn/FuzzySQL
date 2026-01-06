from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstAlterDrop(TreeAstNode):
    def __init__(self, table_id, lst):
        super().__init__(TypeAst.ALTER_DROP)
        self.id = table_id
        self.lst = lst