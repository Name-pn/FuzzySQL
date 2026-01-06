from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstRightJoin(TreeAstNode):
    def __init__(self, ref, name):
        super().__init__(TypeAst.RIGHT_JOIN)
        self.name = name
        self.ref = ref