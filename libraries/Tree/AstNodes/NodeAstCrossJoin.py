from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstCrossJoin(TreeAstNode):
    def __init__(self, ref, name):
        super().__init__(TypeAst.CROSS_JOIN)
        self.name = name
        self.ref = ref