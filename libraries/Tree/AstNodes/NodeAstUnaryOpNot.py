from libraries.Tree.AstNodes.NodeAstUnaryOp import NodeAstUnaryOp
from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstUnaryOpNot(NodeAstUnaryOp):
    def __init__(self, expr):
        super().__init__(TypeAst.UNARY_OP_NOT)
        self.expr = expr