from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstAttrDefault(TreeAstNode):
    def __init__(self, value):
        super().__init__(TypeAst.ATTR_DEFAULT)
        self.value = value