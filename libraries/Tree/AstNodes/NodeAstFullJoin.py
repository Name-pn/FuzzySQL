from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstFullJoin(TreeAstNode):
    def __init__(self, ref, name):
        super().__init__(TypeAst.FULL_JOIN)
        self.name = name
        self.ref = ref