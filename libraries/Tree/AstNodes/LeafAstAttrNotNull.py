from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstAttrNotNull(TreeAstNode):
    def __init__(self):
        super().__init__(TypeAst.ATTR_NOT_NULL)