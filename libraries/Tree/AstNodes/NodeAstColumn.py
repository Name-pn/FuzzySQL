from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstColumn(TreeAstNode):
    def __init__(self, id, type, attrs):
        super().__init__(TypeAst.COLUMN_NODE)
        self.id = id
        self.type = type
        self.attrs = attrs