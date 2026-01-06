from libraries.Symbol.Epsilon import Epsilon
from libraries.Symbol.Symbol import Symbol
from libraries.Symbol.Terminal import Terminal, Category
from libraries.Tree.AstNodes.LeafAstComparison import LeafAstComparison
from libraries.Tree.AstNodes.LeafAstEmpty import LeafAstEmpty
from libraries.Tree.AstNodes.LeafAstNull import LeafAstNull
from libraries.Tree.AstNodes.NodeAstAlterAdd import NodeAstAlterAdd
from libraries.Tree.AstNodes.NodeAstAlterDrop import NodeAstAlterDrop
from libraries.Tree.AstNodes.NodeAstAlterModify import NodeAstAlterModify
from libraries.Tree.AstNodes.NodeAstAlterRename import NodeAstAlterRename
from libraries.Tree.AstNodes.NodeAstAssigment import NodeAstAssigment
from libraries.Tree.AstNodes.NodeAstAssigmentList import NodeAstAssigmentList
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
from libraries.Tree.AstNodes.NodeAstBinOp import NodeAstBinOp
from libraries.Tree.AstNodes.NodeAstColumn import NodeAstColumn
from libraries.Tree.AstNodes.NodeAstColumns import NodeAstColumns
from libraries.Tree.AstNodes.NodeAstCommands import NodeAstCommands
from libraries.Tree.AstNodes.NodeAstCrossJoin import NodeAstCrossJoin
from libraries.Tree.AstNodes.NodeAstDeleteFrom import NodeAstDeleteFrom
from libraries.Tree.AstNodes.NodeAstDeleteFromWhere import NodeAstDeleteFromWhere
from libraries.Tree.AstNodes.NodeAstExprList import NodeAstExprList
from libraries.Tree.AstNodes.NodeAstFullJoin import NodeAstFullJoin
from libraries.Tree.AstNodes.NodeAstFuzzyAdd import NodeAstFuzzyAdd
from libraries.Tree.AstNodes.NodeAstFuzzyColomn import NodeAstFuzzyColomn
from libraries.Tree.AstNodes.NodeAstFuzzyModify import NodeAstFuzzyModify
from libraries.Tree.AstNodes.NodeAstFuzzyRemove import NodeAstFuzzyRemove
from libraries.Tree.AstNodes.NodeAstInnerJoin import NodeAstInnerJoin
from libraries.Tree.AstNodes.NodeAstInsertIntoColumns import NodeAstInsertIntoColumns
from libraries.Tree.AstNodes.NodeAstInsertIntoValues import NodeAstInsertIntoValues
from libraries.Tree.AstNodes.NodeAstInsertValues import NodeAstInsertValues
from libraries.Tree.AstNodes.NodeAstLeftJoin import NodeAstLeftJoin
from libraries.Tree.AstNodes.NodeAstMultiSelect import NodeAstMultiSelect
from libraries.Tree.AstNodes.NodeAstName import NodeAstName
from libraries.Tree.AstNodes.NodeAstOrderEl import NodeAstOrderEl
from libraries.Tree.AstNodes.NodeAstOrderList import NodeAstOrderList
from libraries.Tree.AstNodes.NodeAstOrderType import NodeAstOrderType
from libraries.Tree.AstNodes.NodeAstRightJoin import NodeAstRightJoin
from libraries.Tree.AstNodes.NodeAstSelect import NodeAstSelect
from libraries.Tree.AstNodes.NodeAstSelectFrom import NodeAstSelectFrom
from libraries.Tree.AstNodes.NodeAstSelectWith import NodeAstSelectWith
from libraries.Tree.AstNodes.NodeAstSet import NodeAstSet
from libraries.Tree.AstNodes.NodeAstType import NodeAstType
from libraries.Tree.AstNodes.NodeAstUnaryOp import NodeAstUnaryOp
from libraries.Tree.AstNodes.NodeAstUnaryOpMinus import NodeAstUnaryOpMinus
from libraries.Tree.AstNodes.NodeAstUnaryOpNot import NodeAstUnaryOpNot
from libraries.Tree.AstNodes.NodeAstUnaryOpPlus import NodeAstUnaryOpPlus
from libraries.Tree.AstNodes.NodeAstUpdate import NodeAstUpdate
from libraries.Tree.AstNodes.NodeAstValues import NodeAstValues
from libraries.Tree.AstNodes.NodeAstColumnsID import NodeAstColumnsID
from libraries.Tree.AstNodes.NodeRefList import NodeAstRefList
from libraries.Tree.AstNodes.NodeWhere import NodeAstWhere
from libraries.Tree.TreeAst import TreeAstNode

class MixinAST():
    def __init__(self):
        self.parse_stack = []

    def _on_reduce0(self):
        pass
    def _on_reduce1(self):
        pass

    def _on_reduce2(self):
        pass

    def _on_reduce3(self):
        length = 1
        command = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstCommands([command])
        self.parse_stack.append(new_node)

    def _on_reduce4(self):
        length = 1
        command = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstCommands([command])
        self.parse_stack.append(new_node)
    def _on_reduce5(self):
        length = 2
        command = self.parse_stack[-2]
        s = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstCommands(s.lst.append(command))
        self.parse_stack.append(new_node)
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

    def _on_reduce10(self):
        length = 2
        lst = self.parse_stack[-1]
        id = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstAlterAdd(id, lst)
        self.parse_stack.append(new_node)
    def _on_reduce11(self):
        length = 2
        lst = self.parse_stack[-1]
        id = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstAlterModify(id, lst)
        self.parse_stack.append(new_node)
    def _on_reduce12(self):
        length = 2
        lst = self.parse_stack[-1]
        id = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstAlterDrop(id, lst)
        self.parse_stack.append(new_node)
    def _on_reduce13(self):
        length = 3
        old_id = self.parse_stack[-2]
        new_id = self.parse_stack[-1]
        table_id = self.parse_stack[-3]
        del self.parse_stack[-length:]
        new_node = NodeAstAlterRename(table_id, old_id, new_id)
        self.parse_stack.append(new_node)
    def _on_reduce14(self):
        length = 2
        id = self.parse_stack[-2]
        val = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstSet(id, val)
        self.parse_stack.append(new_node)
    def _on_reduce15(self):
        length = 3
        lstValues = self.parse_stack[-1]
        lstColumns = self.parse_stack[-2]
        id = self.parse_stack[-3]
        del self.parse_stack[-length:]
        new_node = NodeAstInsertIntoColumns(id, lstColumns, lstValues)
        self.parse_stack.append(new_node)
    def _on_reduce16(self):
        length = 2
        insertLst = self.parse_stack[-1]
        id = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstInsertIntoValues(id, insertLst)
        self.parse_stack.append(new_node)
    def _on_reduce17(self):
        length = 3
        where = self.parse_stack[-1]
        AList = self.parse_stack[-2]
        id = self.parse_stack[-3]
        del self.parse_stack[-length:]
        new_node = NodeAstUpdate(id, AList, where)
        self.parse_stack.append(new_node)
    def _on_reduce18(self):
        length = 2
        expr = self.parse_stack[-1]
        id = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstAssigment(id, expr)
        self.parse_stack.append(new_node)
    def _on_reduce19(self):
        length = 1
        el = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstAssigmentList([el])
        self.parse_stack.append(new_node)
    def _on_reduce20(self):
        length = 2
        lst = self.parse_stack[-1]
        el = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstAssigmentList(lst.lst.append(el))
        self.parse_stack.append(new_node)
    def _on_reduce21(self):
        length = 1
        id = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstDeleteFrom(id)
        self.parse_stack.append(new_node)

    def _on_reduce22(self):
        length = 2
        expr = self.parse_stack[-1]
        id = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstDeleteFromWhere(id, expr)
        self.parse_stack.append(new_node)
    def _on_reduce23(self):
        pass
    def _on_reduce24(self):
        length = 3
        sOrder = self.parse_stack[-1]
        sWhere = self.parse_stack[-2]
        sFrom = self.parse_stack[-3]
        del self.parse_stack[-length:]
        new_node = NodeAstMultiSelect(sFrom, sWhere, sOrder)
        self.parse_stack.append(new_node)
    def _on_reduce25(self):
        length = 5
        sWith = self.parse_stack[-1]
        sOrder = self.parse_stack[-2]
        sWhere = self.parse_stack[-3]
        sFrom = self.parse_stack[-4]
        eList = self.parse_stack[-5]
        del self.parse_stack[-length:]
        new_node = NodeAstSelect(eList, sFrom, sWhere, sOrder, sWith)
        self.parse_stack.append(new_node)
    def _on_reduce26(self):
        new_node = LeafAstEmpty()
        self.parse_stack.append(new_node)
    def _on_reduce27(self):
        length = 1
        num = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstSelectWith(num)
        self.parse_stack.append(new_node)
    def _on_reduce28(self):
        new_node = LeafAstEmpty()
        self.parse_stack.append(new_node)

    def _on_reduce29(self):
        pass
    def _on_reduce30(self):
        length = 2
        orderLst = self.parse_stack[-1]
        orderEl = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstOrderList(orderLst.lst.append(orderEl))
        self.parse_stack.append(new_node)

    def _on_reduce31(self):
        length = 1
        orderEl = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstOrderList([orderEl])
        self.parse_stack.append(new_node)
    def _on_reduce32(self):
        length = 2
        order = self.parse_stack[-1]
        expr = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstOrderEl(expr, order)
        self.parse_stack.append(new_node)
    def _on_reduce33(self):
        new_node = NodeAstOrderType()
        self.parse_stack.append(new_node)
    def _on_reduce34(self):
        new_node = NodeAstOrderType(True)
        self.parse_stack.append(new_node)
    def _on_reduce35(self):
        new_node = NodeAstOrderType(False)
        self.parse_stack.append(new_node)
    def _on_reduce36(self):
        new_node = LeafAstEmpty()
        self.parse_stack.append(new_node)
    def _on_reduce37(self):
        length = 1
        refs = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstSelectFrom(refs)
        self.parse_stack.append(new_node)
    def _on_reduce38(self):
        new_node = LeafAstEmpty()
        self.parse_stack.append(new_node)
    def _on_reduce39(self):
        length = 1
        expr = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstWhere(expr)
        self.parse_stack.append(new_node)
    def _on_reduce40(self):
        length = 2
        ref = self.parse_stack[-1]
        refs = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstRefList(refs.lst.append(ref))
        self.parse_stack.append(new_node)
    def _on_reduce41(self):
        length = 1
        ref = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstRefList([ref])
        self.parse_stack.append(new_node)
    def _on_reduce42(self):
        length = 2
        ref = self.parse_stack[-1]
        name = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstCrossJoin(ref, name)
        self.parse_stack.append(new_node)

    def _on_reduce43(self):
        pass
    def _on_reduce44(self):
        length = 2
        ref = self.parse_stack[-1]
        name = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstInnerJoin(ref, name)
        self.parse_stack.append(new_node)
    def _on_reduce45(self):
        length = 2
        ref = self.parse_stack[-1]
        name = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstLeftJoin(ref, name)
        self.parse_stack.append(new_node)
    def _on_reduce46(self):
        length = 2
        ref = self.parse_stack[-1]
        name = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstRightJoin(ref, name)
        self.parse_stack.append(new_node)
    def _on_reduce47(self):
        length = 2
        ref = self.parse_stack[-1]
        name = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstFullJoin(ref, name)
        self.parse_stack.append(new_node)

    def _on_reduce48(self):
        pass

    def _on_reduce49(self):
        pass
    def _on_reduce50(self):
        length = 2
        exprList = self.parse_stack[-1]
        expr = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstExprList(exprList.lst.append(expr))
        self.parse_stack.append(new_node)
    def _on_reduce51(self):
        length = 1
        expr = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstExprList([expr])
        self.parse_stack.append(new_node)

    def _on_reduce52(self):
        length = 2
        expr2 = self.parse_stack[-1]
        expr1 = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstBinOp(expr1, "or", expr2)
        self.parse_stack.append(new_node)
    def _on_reduce53(self):
        pass

    def _on_reduce54(self):
        length = 2
        expr2 = self.parse_stack[-1]
        expr1 = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstBinOp(expr1, "and", expr2)
        self.parse_stack.append(new_node)
    def _on_reduce55(self):
        pass
    def _on_reduce56(self):
        length = 1
        expr = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstUnaryOpNot(expr)
        self.parse_stack.append(new_node)

    def _on_reduce57(self):
        pass
    def _on_reduce58(self):
        length = 3
        expr2 = self.parse_stack[-1]
        comp = self.parse_stack[-2]
        expr1 = self.parse_stack[-3]
        del self.parse_stack[-length:]
        new_node = NodeAstBinOp(expr1, comp.op, expr2)
        self.parse_stack.append(new_node)
    def _on_reduce59(self):
        length = 2
        expr2 = self.parse_stack[-1]
        expr1 = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstBinOp(expr1, "=", expr2)
        self.parse_stack.append(new_node)
    def _on_reduce60(self):
        pass
    def _on_reduce61(self):
        length = 2
        expr2 = self.parse_stack[-1]
        expr1 = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstBinOp(expr1, "+", expr2)
        self.parse_stack.append(new_node)
    def _on_reduce62(self):
        pass
    def _on_reduce63(self):
        length = 2
        expr2 = self.parse_stack[-1]
        expr1 = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstBinOp(expr1, "/", expr2)
        self.parse_stack.append(new_node)
    def _on_reduce64(self):
        length = 2
        expr2 = self.parse_stack[-1]
        expr1 = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstBinOp(expr1, "*", expr2)
        self.parse_stack.append(new_node)
    def _on_reduce65(self):
        pass
    def _on_reduce66(self):
        length = 2
        expr2 = self.parse_stack[-1]
        expr1 = self.parse_stack[-2]
        del self.parse_stack[-length:]
        new_node = NodeAstBinOp(expr1, "^", expr2)
        self.parse_stack.append(new_node)
    def _on_reduce67(self):
        pass
    def _on_reduce68(self):
        length = 1
        value = self.parse_stack[-1]
        del self.parse_stack[-length:]
        new_node = NodeAstUnaryOpPlus(value)
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

    def _on_reduce106(self):
        expr = self.parse_stack[-1]
        del self.parse_stack[-1:]
        new_node = NodeAstUnaryOpMinus(expr)
        self.parse_stack.append(new_node)

    def _on_reduce107(self):
        expr1 = self.parse_stack[-2]
        expr2 = self.parse_stack[-1]
        del self.parse_stack[-2:]
        new_node = NodeAstBinOp(expr1, '-', expr2)
        self.parse_stack.append(new_node)

    def _on_reduce108(self):
        expr1 = self.parse_stack[-2]
        expr2 = self.parse_stack[-1]
        del self.parse_stack[-2:]
        new_node = NodeAstBinOp(expr1, '%', expr2)
        self.parse_stack.append(new_node)

    def _on_reduce(self, state, symbol):
        index = self.table.loc[state, symbol].value
        method_name = "_on_reduce" + str(index)
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method()
        else:
            raise Exception(f"Не найдена свертка {index}")

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
            case Category.COMPARISON:
                self.parse_stack.append(LeafAstComparison(symbol.lexem))


