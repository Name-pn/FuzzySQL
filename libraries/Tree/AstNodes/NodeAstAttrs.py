from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstAttrs(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.ATTRS)
        self.lst = lst
