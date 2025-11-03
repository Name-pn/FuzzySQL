from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstAttrPrimaryKey(TreeAstNode):
    def __init__(self):
        super().__init__(TypeAst.ATTR_PRIMARY_KEY)