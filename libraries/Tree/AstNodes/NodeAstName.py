from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstName(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.NAME_NODE)
        self.lst = lst