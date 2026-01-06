from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstDeleteFrom(TreeAstNode):
    def __init__(self, id):
        super().__init__(TypeAst.DELETE_FROM)
        self.id = id