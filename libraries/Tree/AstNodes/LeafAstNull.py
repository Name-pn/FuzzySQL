from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstNull(TreeAstNode):
    def __init__(self):
        super().__init__(TypeAst.NULL)