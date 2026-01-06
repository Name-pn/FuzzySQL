from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstAssigmentList(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.ATTR_DEFAULT)
        self.lst = lst