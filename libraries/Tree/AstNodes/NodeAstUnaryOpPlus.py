from libraries.Tree.AstNodes.NodeAstUnaryOp import NodeAstUnaryOp
from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstUnaryOpPlus(NodeAstUnaryOp):
    def __init__(self, expr):
        super().__init__(TypeAst.UNARY_OP_PLUS)
        self.expr = expr