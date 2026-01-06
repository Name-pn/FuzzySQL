from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstInnerJoin(TreeAstNode):
    def __init__(self, ref, name):
        super().__init__(TypeAst.INNER_JOIN)
        self.name = name
        self.ref = ref