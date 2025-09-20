class TreeNode():
    def __init__(self, symbol, children = None):
        self.symbol = symbol
        self.children = children if children is not None else []

    def __str__(self, level = 0):
        ret = "-" * level + str(self.symbol) + "\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return f"<TreeNode: {self.symbol}>"

    def postOrderVisit(self, action):
        for child in self.children:
            child.postOrderVisit(action)
        self.synth = action(self)