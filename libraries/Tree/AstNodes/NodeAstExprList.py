from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstExprList(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.EXPR_LIST)
        self.lst = lst