from libraries.Tree.TreeAst import TreeAstNode, TypeAst


class NodeAstCommands(TreeAstNode):
    def __init__(self, lst):
        super().__init__(TypeAst.COMMANDS)
        self.lst = lst