from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstUnaryOp(TreeAstNode):
    def __init__(self, type):
        super().__init__(type)