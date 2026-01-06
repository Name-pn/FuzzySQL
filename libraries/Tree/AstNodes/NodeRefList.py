from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstRefList(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.REF_LIST)
        self.lst = lst