from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstLeftJoin(TreeAstNode):
    def __init__(self, ref, name):
        super().__init__(TypeAst.LEFT_JOIN)
        self.name = name
        self.ref = ref