from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class LeafAstAttrUnique(TreeAstNode):
    def __init__(self):
        super().__init__(TypeAst.ATTR_UNIQUE)