from libraries.Symbol.Epsilon import Epsilon
from libraries.Symbol.Symbol import Symbol
from libraries.Symbol.Terminal import Terminal, Category
from libraries.Tree.AstNodes.LeafAstNull import LeafAstNull
from libraries.Tree.AstNodes.NodeAstAttrDefault import NodeAstAttrDefault
from libraries.Tree.AstNodes.LeafAstAttrNotNull import LeafAstAttrNotNull
from libraries.Tree.AstNodes.LeafAstAttrNull import LeafAstAttrNull
from libraries.Tree.AstNodes.LeafAstAttrPrimary import LeafAstAttrPrimaryKey
from libraries.Tree.AstNodes.LeafAstAttrUnique import LeafAstAttrUnique
from libraries.Tree.AstNodes.LeafAstNumber import LeafAstNumber
from libraries.Tree.AstNodes.LeafAstRealNumber import LeafAstRealNumber
from libraries.Tree.AstNodes.LeafAstString import LeafAstString
from libraries.Tree.AstNodes.LeafAstType import LeafAstType
from libraries.Tree.AstNodes.NodeAstAttrs import NodeAstAttrs
from libraries.Tree.AstNodes.NodeAstColumn import NodeAstColumn
from libraries.Tree.AstNodes.NodeAstColumns import NodeAstColumns
from libraries.Tree.AstNodes.NodeAstFuzzyAdd import NodeAstFuzzyAdd
from libraries.Tree.AstNodes.NodeAstFuzzyColomn import NodeAstFuzzyColomn
from libraries.Tree.AstNodes.NodeAstFuzzyModify import NodeAstFuzzyModify
from libraries.Tree.AstNodes.NodeAstFuzzyRemove import NodeAstFuzzyRemove
from libraries.Tree.AstNodes.NodeAstInsertValues import NodeAstInsertValues
from libraries.Tree.AstNodes.NodeAstName import NodeAstName
from libraries.Tree.AstNodes.NodeAstType import NodeAstType
from libraries.Tree.AstNodes.NodeAstUnaryOp import NodeAstUnaryOp
from libraries.Tree.AstNodes.NodeAstValues import NodeAstValues
from libraries.Tree.AstNodes.NodeAstColumnsID import NodeAstColumnsID
from libraries.Tree.TreeAst import TreeAstNode

class MixinAST():
    def __init__(self):
        self.parse_stack = []

    def _on_reduce6(self):
        length = 5
        id = self.parse_stack[-5]
        a = self.parse_stack[-4]
        b = self.parse_stack[-3]
        c = self.parse_stack[-2]
        d = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstFuzzyAdd(id, a, b, c, d)
        self.parse_stack.append(new_node)

    def _on_reduce7(self):
        length = 5
        id = self.parse_stack[-5]
        a = self.parse_stack[-4]
        b = self.parse_stack[-3]
        c = self.parse_stack[-2]
        d = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstFuzzyModify(id, a, b, c, d)
        self.parse_stack.append(new_node)

    def _on_reduce8(self):
        length = 1
        id = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstFuzzyRemove(id)
        self.parse_stack.append(new_node)

    def _on_reduce9(self):
        length = 2
        id = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstFuzzyRemove(id)
        self.parse_stack.append(new_node)

    def _on_reduce9(self):
        length = 2
        id = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstFuzzyRemove(id)
        self.parse_stack.append(new_node)

    def _on_reduce68(self):
        length = 2
        value = self.parse_stack[-1]
        plus_and_minus = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstUnaryOp(plus_and_minus.lexem, value)
        self.parse_stack.append(new_node)

    def _on_reduce69(self):
        pass

    def _on_reduce70(self):
        pass

    def _on_reduce71(self):
        pass

    def _on_reduce72(self):
        pass

    def _on_reduce73(self):
        pass

    def _on_reduce74(self):
        length = 2
        id = self.parse_stack[-1]
        name = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstName(name.lst.append(id))
        self.parse_stack.append(new_node)

    def _on_reduce75(self):
        length = 1
        id = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstName([id])
        self.parse_stack.append(new_node)

    def _on_reduce76(self):
        length = 2
        columns = self.parse_stack[-1]
        el = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstColumns(columns.lst.append(el))
        self.parse_stack.append(new_node)

    def _on_reduce77(self):
        length = 1
        column = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstColumns([column])
        self.parse_stack.append(new_node)

    def _on_reduce78(self):
        length = 3
        id = self.parse_stack[-3]
        type = self.parse_stack[-2]
        attrs = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstColumn(id, type, attrs)
        self.parse_stack.append(new_node)

    def _on_reduce79(self):
        length = 1
        type_leaf = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstType(type_leaf)
        self.parse_stack.append(new_node)

    def _on_reduce80(self):
        length = 2
        type_leaf = self.parse_stack[-2]
        num_leaf = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstType(type_leaf, num_leaf)
        self.parse_stack.append(new_node)

    def _on_reduce81(self):
        length = 3
        type_leaf = self.parse_stack[-3]
        num_leaf = self.parse_stack[-2]
        num_leaf_2 = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstType(type_leaf, num_leaf, num_leaf_2)
        self.parse_stack.append(new_node)

    def _on_reduce82(self):
        new_node = NodeAstAttrs([])
        self.parse_stack.append(new_node)

    def _on_reduce83(self):
        old_lst = self.parse_stack[-1].lst
        new_el = self.parse_stack[-2]
        del self.parse_stack[-2:]
        new_node = NodeAstAttrs(old_lst.append(new_el))
        self.parse_stack.append(new_node)

    def _on_reduce84(self):
        new_node = LeafAstAttrUnique()
        self.parse_stack.append(new_node)

    def _on_reduce85(self):
        new_node = LeafAstAttrNull()
        self.parse_stack.append(new_node)

    def _on_reduce86(self):
        new_node = LeafAstAttrNotNull()
        self.parse_stack.append(new_node)

    def _on_reduce87(self):
        new_node = LeafAstAttrPrimaryKey()
        self.parse_stack.append(new_node)

    def _on_reduce88(self):
        value = self.parse_stack[-1]
        del self.parse_stack[-1:]
        new_node = NodeAstAttrDefault(value)
        self.parse_stack.append(new_node)

    def _on_reduce89(self):
        pass

    def _on_reduce90(self):
        pass

    def _on_reduce91(self):
        pass

    def _on_reduce92(self):
        pass

    def _on_reduce93(self):
        lst_node = self.parse_stack[-1]
        new_value = self.parse_stack[-2]
        del self.parse_stack[-2:]
        new_node = NodeAstValues(lst_node.lst.append(new_value))
        self.parse_stack.append(new_node)

    def _on_reduce94(self):
        first_val = self.parse_stack[-1]
        del self.parse_stack[-1:]
        new_node = NodeAstValues([first_val])
        self.parse_stack.append(new_node)

    def _on_reduce95(self):
        pass

    def _on_reduce96(self):
        pass

    def _on_reduce97(self):
        id = self.parse_stack[-1]
        del self.parse_stack[-1:]
        new_node = NodeAstFuzzyColomn(id)
        self.parse_stack.append(new_node)

    def _on_reduce98(self):
        pass

    def _on_reduce99(self):
        pass

    def _on_reduce100(self):
        id = self.parse_stack[-1]
        del self.parse_stack[-1:]
        new_node = NodeAstColumnsID([id])
        self.parse_stack.append(new_node)

    def _on_reduce101(self):
        lst = self.parse_stack[-1].lst
        el = self.parse_stack[-2]
        del self.parse_stack[-2:]
        new_node = NodeAstColumnsID(lst.append(el))
        self.parse_stack.append(new_node)

    def _on_reduce102(self):
        pass

    def _on_reduce103(self):
        value = self.parse_stack[-1]
        del self.parse_stack[-1:]
        new_node = NodeAstInsertValues([value])
        self.parse_stack.append(new_node)

    def _on_reduce104(self):
        lst = self.parse_stack[-1].lst
        value = self.parse_stack[-2]
        del self.parse_stack[-2:]
        new_node = NodeAstInsertValues(lst.append(value))
        self.parse_stack.append(new_node)

    def _on_reduce105(self):
        lst = self.parse_stack[-1].lst
        value = self.parse_stack[-2]
        del self.parse_stack[-2:]
        new_node = NodeAstInsertValues(lst.append(value))
        self.parse_stack.append(new_node)

    def _on_reduce(self, state, symbol):
        pass
        # production = self.gr[self.table.loc[state, symbol].value]
        # head = production.head
        # length = len(production.body)
        # node = TreeCstNode(head)
        # if production.body[0] == Epsilon():
        #     length = 0
        # if length > 0:
        #     node.children = self.parse_stack[-length:]
        #     del self.parse_stack[-length:]
        # self.parse_stack.append(node)

    def _on_shift(self, state, symbol):
        if not isinstance(symbol, Terminal):
            raise Exception("Передан не терминальный символ")
        match symbol.ttype:
            case Category.TYPE:
                self.parse_stack.append(LeafAstType(symbol.lexem))
            case Category.NUMBER:
                self.parse_stack.append(LeafAstNumber(symbol.lexem))
            case Category.REAL_NUMBER:
                self.parse_stack.append(LeafAstRealNumber(symbol.lexem))
            case Category.STRING:
                self.parse_stack.append(LeafAstString(symbol.lexem))
            case Category.ID:
                self.parse_stack.append(LeafAstString(symbol.lexem))
            case Category.NULL:
                self.parse_stack.append(LeafAstNull())


