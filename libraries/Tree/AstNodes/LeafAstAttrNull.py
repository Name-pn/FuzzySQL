from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstAttrNull(TreeAstNode):
    def __init__(self):
        super().__init__(TypeAst.ATTR_NULL)