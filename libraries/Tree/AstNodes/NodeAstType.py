from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstType(TreeAstNode):
    def __init__(self, type, a = None, b = None):
        super().__init__(TypeAst.TYPE_NODE)
        self.leaf_type = type
        self.a = a
        self.b = b