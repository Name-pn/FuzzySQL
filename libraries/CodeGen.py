import re
from enum import Enum, auto

from libraries.Environment import Environment
from libraries.FunctionHub import FunctionHub
from libraries.Symbol.LTerminal import LTerminal
from libraries.Symbol.NonTerminal import NonTerminal
from libraries.Symbol.SymbolType import SymbolType
from libraries.Symbol.Terminal import Category, Terminal
from libraries.Tree.TreeCst import TreeCstNode

class CategoryColumn(Enum):
    COMMON = auto()
    FUZZY = auto()

index_to_column = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
}

def broadcast(tree: TreeCstNode, fh: FunctionHub, table: Environment):
    #table = Environment()
    #table.load()
    return broadcast_body(tree, table, fh)

def is_modify_command(tree:TreeCstNode):
    return tree.children[0].symbol == Terminal(Category.MODIFY)

def is_remove_command(tree:TreeCstNode):
    return tree.children[0].symbol == Terminal(Category.REMOVE)

def is_create_command(tree:TreeCstNode):
    return tree.children[0].symbol == Terminal(Category.CREATE)

def is_alter_command(tree:TreeCstNode):
    return tree.children[0].symbol == Terminal(Category.ALTER)

def is_alter_modify_command(tree:TreeCstNode):
    return tree.children[0].symbol == Terminal(Category.ALTER) and tree.children[3].symbol == Terminal(Category.MODIFY)

def is_alter_drop_command(tree:TreeCstNode):
    return tree.children[0].symbol == Terminal(Category.ALTER) and tree.children[3].symbol == Terminal(Category.DROP)

def is_add_command(tree:TreeCstNode):
    return len(tree.children) == 11 and tree.children[0].symbol == Terminal(Category.ADD) and \
           tree.children[1].symbol.ttype == Category.ID and \
           tree.children[2].symbol.ttype == Category.OPEN_BRACKET and \
           tree.children[3].symbol.type == SymbolType.NONTERMINAL and \
           tree.children[4].symbol.ttype == Category.COMMA and \
           tree.children[5].symbol.type == SymbolType.NONTERMINAL and \
           tree.children[6].symbol.ttype == Category.COMMA and \
           tree.children[7].symbol.type == SymbolType.NONTERMINAL and \
           tree.children[8].symbol.ttype == Category.COMMA and \
           tree.children[9].symbol.type == SymbolType.NONTERMINAL and \
           tree.children[10].symbol.ttype == Category.CLOSE_BRACKET

def is_set_command(tree:TreeCstNode):
    return len(tree.children) == 3 and tree.children[0].symbol == Terminal(Category.SET) and \
           tree.children[1].symbol.ttype == Category.ID and tree.children[2].symbol.type == SymbolType.NONTERMINAL

def is_alter_rename_command(tree:TreeCstNode):
    return len(tree.children) == 6 and \
           tree.children[0].symbol == Terminal(Category.ALTER) and \
           tree.children[3].symbol == Terminal(Category.RENAME)

def is_alter_add_command(tree:TreeCstNode):
    return len(tree.children) == 7 and \
           tree.children[0].symbol == Terminal(Category.ALTER) and \
           tree.children[3].symbol == Terminal(Category.ADD)

def is_insert_into_with_columns(tree:TreeCstNode):
    return len(tree.children) > 3 and \
           tree.children[3].symbol == Terminal(Category.OPEN_BRACKET) and \
           tree.children[0].symbol == Terminal(Category.INSERT)

def is_insert_into_without_columns(tree:TreeCstNode):
    return len(tree.children) > 3 and \
           tree.children[3].symbol == Terminal(Category.VALUES) and \
           tree.children[0].symbol == Terminal(Category.INSERT)


def is_update_set(tree: TreeCstNode):
    return len(tree.children) == 5 and \
           tree.children[0].symbol == Terminal(Category.UPDATE)

def is_delete_short(tree: TreeCstNode):
    return len(tree.children) == 3 and \
           tree.children[0].symbol == Terminal(Category.DELETE)

def is_delete(tree: TreeCstNode):
    return len(tree.children) == 5 and \
           tree.children[0].symbol == Terminal(Category.DELETE)

def is_select(tree: TreeCstNode):
    return len(tree.children) == 1 and\
        tree.children[0].symbol == NonTerminal(value="Select")

def is_drop_table(tree: TreeCstNode):
    return len(tree.children) == 3 and \
           tree.children[0].symbol == Terminal(Category.DROP)

def is_fselect(tree: TreeCstNode):
    return len(tree.children) == 1 and\
            tree.children[0].symbol.value == "FSelect"

def output(tree:TreeCstNode):
    print("Node symbol = ", tree.symbol, "Synth = ", tree.synth)

def synthAll(tree:TreeCstNode):
    res = ""
    for child in tree.children:
        if isinstance(child.synth, dict):
            res += " " + child.synth['value']
            continue
        if child.synth == ",":
            res += child.synth
            continue
        if child.synth != "":
            res += " " + child.synth
    return res[1:]

def attrStr(arrAttr, column):
    #print(arrAttr)
    res = ""
    for el in arrAttr:
        if re.search("DEFAULT", el):
            res += f"ALTER COLUMN {column} SET " + el + ",\n"
            continue
        if re.search("NOT NULL", el):
            res += f"ALTER COLUMN {column} SET NOT NULL,\n"
            continue
        if re.search("NULL", el):
            res += f"ALTER COLUMN {column} DROP NOT NULL,\n"
            continue
        if re.search("UNIQUE", el):
            res += f"ADD UNIQUE ({column}),\n"
            continue
        if re.search("PRIMARY", el):
            res += f"ADD PRIMARY KEY ({column}),\n"
            continue
    return res

def dictToStrAdd(tree:TreeCstNode, table: Environment):
    tree.synth = uncoverFuzzy(tree.synth, table)
    n = len(tree.synth['id'])
    res = ""
    for i in range(0, n):
        attrsStrVar = listToStr(tree.synth['attrs'][i])
        if attrsStrVar != "":
            res += f"ADD COLUMN {tree.synth['id'][i]} {tree.synth['type'][i].upper()} {attrsStrVar},\n"
        else:
            res += f"ADD COLUMN {tree.synth['id'][i]} {tree.synth['type'][i].upper()},\n"
    return res[:-2]

def dictToStrModify(tree:TreeCstNode, table: Environment, tableName: str, fh:FunctionHub):
    n = len(tree.synth['id'])
    res = ""
    for i in range(0, n):
        if fh.isFuzzy(tableName, tree.synth['id'][i]) and tree.synth['type'][i].upper() == "FUZZY":
            pass
        elif not fh.isFuzzy(tableName, tree.synth['id'][i]) and tree.synth['type'][i].upper() == "FUZZY":
            names = [tree.synth['id'][i] + table.get('columnsuffix') + str(j) for j in range(1, 5)]
            for index, name in enumerate(names):
                if index == 0:
                    res += f"ALTER COLUMN " + name + " TYPE " + "REAL" + ",\n"
                    res += attrStr(tree.synth['attrs'][i], tree.synth['id'][i])
                else:
                    res += f"ADD COLUMN " + name + " REAL"+ ",\n"
        elif fh.isFuzzy(tableName, tree.synth['id'][i]) and not tree.synth['type'][i].upper() == "FUZZY":
            names = [tree.synth['id'][i] + table.get('columnsuffix') + str(i) for i in range(1, 5)]
            for index, name in enumerate(names):
                if index == 0:
                    res += f"ALTER COLUMN " + name + " TYPE " + tree.synth['type'][i] + ",\n"
                    res += attrStr(tree.synth['attrs'][i], tree.synth['id'][i])
                else:
                    res += f"DROP COLUMN " + name + ",\n"
        elif not fh.isFuzzy(tableName, tree.synth['id'][i]) and not tree.synth['type'][i].upper() == "FUZZY":
            res += f"ALTER COLUMN " + tree.synth['id'][i] + " TYPE " + tree.synth['type'][i] + ",\n"
            res += attrStr(tree.synth['attrs'][i], tree.synth['id'][i])
    return res[:-2]

def listToStr(lst):
    res = ""
    for el in lst:
        res += el + " "
    return res[:-1]

def uncoverFuzzyWithoutAttrs(d: dict, table:Environment):
    n = len(d['id'])
    res = dict()
    res['id'] = []
    res['type'] = []
    for i in range(n):
        if d['type'][i] != CategoryColumn.FUZZY:
            res['id'].append(d['id'][i])
            res['type'].append(d['type'][i])
        else:
            for j in range(1, 5):
                res['id'].append(d['id'][i] + table.get('columnsuffix') + str(j))
                res['type'].append("REAL")
    return res

def uncoverFuzzy(d: dict, table:Environment):
    n = len(d['id'])
    res = dict()
    res['id'] = []
    res['type'] = []
    res['attrs'] = []
    for i in range(n):
        if d['type'][i].upper() != "FUZZY":
            res['id'].append(d['id'][i])
            res['type'].append(d['type'][i])
            res['attrs'].append(d['attrs'][i])
        else:
            for j in range(1, 5):
                res['id'].append(d['id'][i] + table.get('columnsuffix') + str(j))
                res['type'].append("REAL")
                res['attrs'].append(d['attrs'][i])
    return res

def dictToStrCreate(tree: TreeCstNode, table:Environment):
    tree.synth = uncoverFuzzy(tree.synth, table)
    n = len(tree.synth['id'])
    res = ""
    for i in range(0, n):
        if tree.synth["attrs"][i]:
            res += tree.synth['id'][i] + " " + tree.synth['type'][i] + " " + listToStr(tree.synth["attrs"][i]) + ", "
        else:
            res += tree.synth['id'][i] + " " + tree.synth['type'][i] + ", "
    return res[:-2]

def dictToStrDrop(tree: TreeCstNode, table:Environment):
    res = ""
    d = tree.synth
    for type, id in zip(d["type"], d["id"]):
        if type is CategoryColumn.COMMON:
            res += "DROP COLUMN " + id + ",\n"
        else:
            names = [id + table.get('columnsuffix') + str(i) for i in range(1, 5)]
            for name in names:
                res += "DROP COLUMN " + name + ",\n"
    return res[:-2]

def dictToStrInsert(tree: TreeCstNode, table:Environment):
    tree.synth = uncoverFuzzyWithoutAttrs(tree.synth, table)
    res = ""
    for el in tree.synth['id']:
        res += el + ", "
    return res[:-2]

def simplify(tree: TreeCstNode):
    while True:
        if len(tree.children) == 1:
            tree = tree.children[0]
        elif len(tree.children) > 1:
            for i in range(len(tree.children)):
                tree.children[i] = simplify(tree.children[i])
            break
        elif len(tree.children) == 0:
            break
    return tree

def is_paranthesis_node(tree: TreeCstNode):
    n = len(tree.children)
    if tree.symbol == NonTerminal(value="Factor") and \
        n == 3 and tree.children[0].symbol == Terminal(Category.OPEN_BRACKET):
        return True
    else:
        return False

def is_fuzzy_value_node(tree: TreeCstNode):
    n = len(tree.children)
    if tree.symbol == NonTerminal(value="FValue") and \
            n == 3 and tree.children[0].symbol == Terminal(Category.FUZZY_VALUE):
        return True
    else:
        return False

def is_fuzzy_value(tree: TreeCstNode):
    tree = simplify(tree)
    while True:
        if is_paranthesis_node(tree):
            tree = tree.children[1]
        else:
            break
    return is_fuzzy_value_node(tree)

def get_fuzzy_value(tree: TreeCstNode):
    tree = simplify(tree)
    while True:
        if is_paranthesis_node(tree):
            tree = tree.children[1]
        else:
            break
    return tree.children[2].synth

def get_query_ft3(id, name, table):
    select_a = f"(select a from {table.get('fvtname')} where name = \'{name}\')"
    select_b = f"(select b from {table.get('fvtname')} where name = \'{name}\')"
    select_c = f"(select c from {table.get('fvtname')} where name = \'{name}\')"
    select_d = f"(select d from {table.get('fvtname')} where name = \'{name}\')"
    return f"case\n" \
           f"when {id} <= {select_a} then 0\n" \
           f"when {id} <= {select_b} then ({id} - {select_a}) / ({select_b} - {select_a})\n" \
           f"when {id} <= {select_c} then 1\n" \
           f"when {id} <= {select_d} then ({select_d} - {id}) / ({select_d} - {select_c})\n" \
           f"else 0\n" \
           f"end\n"

def broadcast_body(tree: TreeCstNode, table: Environment, fh: FunctionHub):
    match tree.symbol.type:
        case SymbolType.TERMINAL:
            if isinstance(tree.symbol, LTerminal):
                if tree.symbol.ttype == Category.STRING:
                    return tree.symbol.lexem[:]#[1:-1]
                return tree.symbol.lexem
            if tree.symbol == Terminal(Category.SEPARATOR):
                return ";"
            if tree.symbol == Terminal(Category.MULTIPLICATION):
                return "*"
            if tree.symbol == Terminal(Category.EQUAL):
                return "="
            if tree.symbol == Terminal(Category.COMMA):
                return ","
            if tree.symbol == Terminal(Category.OPEN_BRACKET):
                return "("
            if tree.symbol == Terminal(Category.CLOSE_BRACKET):
                return ")"
            return tree.symbol.value.upper()
        case SymbolType.NONTERMINAL:
            match tree.symbol:
                case NonTerminal(value="Command"):
                    if is_modify_command(tree):
                        return f"UPDATE {table.get('fvtname')} SET name = \'{tree.children[1].synth}\', a = {tree.children[3].synth}" \
                               f", b = {tree.children[5].synth}, c = {tree.children[7].synth}, d = {tree.children[9].synth} " \
                               f"WHERE name = \'{tree.children[1].synth}\'"
                    if is_remove_command(tree):
                        return f"DELETE FROM {table.get('fvtname')} WHERE name = \'{tree.children[1].synth}\'"
                    if is_add_command(tree):
                        return f"INSERT INTO {table.get('fvtname')}(name, a, b, c, d) VALUES (\'{tree.children[1].synth}\', " \
                               f"{tree.children[3].synth}, {tree.children[5].synth}, {tree.children[7].synth}, {tree.children[9].synth})"
                    if is_set_command(tree):
                        table.put(tree.children[1].synth, tree.children[2].synth)
                        return ""
                    if is_create_command(tree):
                        columns = dictToStrCreate(tree.children[4], table)
                        tree.children[4].synth = columns
                        return synthAll(tree)
                    if is_alter_modify_command(tree):
                        columns = dictToStrModify(tree.children[5], table, tree.children[2].synth, fh)
                        removeStr = fh.removeConstrains(tree.children[2].synth)
                        return tree.children[0].synth + " " + tree.children[1].synth + " " + tree.children[2].synth + " " + removeStr + columns
                    if is_alter_drop_command(tree):
                        columns = dictToStrDrop(tree.children[5], table)
                        return tree.children[0].synth + " " + tree.children[1].synth + " " + tree.children[2].synth + " " + columns
                    if is_alter_rename_command(tree):
                        return tree.children[0].synth + " " +\
                               tree.children[1].synth + " " +\
                               tree.children[2].synth + " RENAME COLUMN " +\
                               tree.children[4].synth + " TO " + tree.children[5].synth
                    if is_alter_add_command(tree):
                        columns = dictToStrAdd(tree.children[5], table)
                        return tree.children[0].synth + " " +\
                               tree.children[1].synth + " " +\
                               tree.children[2].synth + " " +\
                               columns
                    if is_insert_into_with_columns(tree):
                        columns = dictToStrInsert(tree.children[4], table)
                        return tree.children[0].synth + " " +\
                               tree.children[1].synth + " " +\
                               tree.children[2].synth + " " +\
                               tree.children[3].synth +\
                               columns + tree.children[5].synth +\
                               "\n" + tree.children[6].synth + " " + \
                               tree.children[7].synth
                    if is_insert_into_without_columns(tree):
                        return tree.children[0].synth + " " +\
                               tree.children[1].synth + " " +\
                               tree.children[2].synth + " " +\
                               tree.children[3].synth + " " +\
                               tree.children[4].synth
                    if is_update_set(tree):
                        if tree.children[4].synth != "":
                            res = tree.children[0].synth + " " + tree.children[1].synth + " " +\
                                  tree.children[2].synth + " " + tree.children[3].synth + "\n" +\
                                  tree.children[4].synth
                        else:
                            res = tree.children[0].synth + " " + tree.children[1].synth + " " + \
                                  tree.children[2].synth + " " + tree.children[3].synth
                        return res
                    if is_delete_short(tree):
                        return synthAll(tree)
                    if is_delete(tree):
                        return tree.children[0].synth + " " + tree.children[1].synth + " " + \
                                   tree.children[2].synth + " " + tree.children[3].synth + " " + tree.children[4].synth['value']
                    if is_select(tree):
                        return tree.children[0].synth
                    if is_drop_table(tree):
                        return synthAll(tree)
                    if is_fselect(tree):
                        return synthAll(tree)
                case NonTerminal(value="Select"):
                    return synthAll(tree)
                case NonTerminal(value="S"):
                    res = ""
                    for index, child in enumerate(tree.children):
                        if len(tree.children) == 1:
                            res += tree.children[index].synth
                        if index == 0:
                            continue
                        if child.symbol == Terminal(Category.SEPARATOR):
                            if tree.children[index-1].synth == "":
                                continue
                            else:
                                res += tree.children[index-1].synth + tree.children[index].synth + "\n"
                        else:
                            res += tree.children[index].synth
                    return res
                case NonTerminal(value="InsertValue"):
                    return tree.children[0].synth + \
                           tree.children[1].synth + \
                           tree.children[2].synth
                case NonTerminal(value="InsertValues"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) == 3:
                        return tree.children[0].synth + \
                               tree.children[1].synth + "\n" +\
                               tree.children[2].synth
                case NonTerminal(value="AssigmentList"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) > 1:
                        return tree.children[0].synth + tree.children[1].synth + "\n" + tree.children[2].synth
                case NonTerminal(value="Assigment"):
                    res = ""
                    tree.children[0].synth = uncoverFuzzyWithoutAttrs(tree.children[0].synth, table)
                    if len(tree.children[0].synth['id']) == 1:
                        tree.children[0].synth = tree.children[0].synth['id'][0]
                        return synthAll(tree)
                    elif len(tree.children[0].synth['id']) > 1:
                        if is_fuzzy_value(tree.children[2]):
                            value = get_fuzzy_value(tree.children[2])
                            for i in range(len(tree.children[0].synth['id'])): #+ tree.children[2].synth
                                res += tree.children[0].synth['id'][i] + " " + tree.children[1].synth + " " + \
                                       f"(SELECT {index_to_column[i]} FROM {table.get('fvtname')} WHERE name = '{value}'),\n"
                        else:
                            raise Exception("Fuzzy column cant be equal scalar value")

                        return res[:-2]

                case NonTerminal(value="Column"):
                    res = dict()
                    res['id'] = []
                    res['type'] = []
                    res['attrs'] = []
                    res['id'].append(tree.children[0].synth)
                    res['type'] = [tree.children[1].synth]
                    res['attrs'] = [tree.children[2].synth]
                    return res
                case NonTerminal(value="ColumnID"):
                    if tree.children[0].symbol == NonTerminal(value="FColumn"):
                        # 0 тип значит нечеткий столбец
                        return {
                            "type": [CategoryColumn.FUZZY],
                            "id": [tree.children[0].children[2].symbol.lexem],
                        }
                    elif tree.children[0].symbol == Terminal(Category.ID):
                        # 1 тип значит айди
                        return {
                            "type": [CategoryColumn.COMMON],
                            "id": [tree.children[0].symbol.lexem],
                        }
                case NonTerminal(value="ColumnsID"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) == 3:
                        one = tree.children[0].synth
                        other = tree.children[2].synth
                        res = dict()
                        res['type'] = one['type'] + other['type']
                        res['id'] = one['id'] + other['id']
                        return res
                case NonTerminal(value="Columns"):
                    res = dict()
                    res['id'] = []
                    res['type'] = []
                    res['attrs'] = []
                    if len(tree.children) == 1:
                        res['id'] += tree.children[0].synth['id']
                        res['type'] += tree.children[0].synth['type']
                        res['attrs'] += tree.children[0].synth['attrs']
                    if len(tree.children) == 3:
                        res['id'] += tree.children[0].synth['id']
                        res['type'] += tree.children[0].synth['type']
                        res['attrs'] += tree.children[0].synth['attrs']
                        res['id'] += tree.children[2].synth['id']
                        res['type'] += tree.children[2].synth['type']
                        res['attrs'] += tree.children[2].synth['attrs']
                    return res
                case NonTerminal(value="Attrs"):
                    if len(tree.children) == 0:
                        return []
                    if len(tree.children) == 1:
                        return [tree.children[0].synth]
                    if len(tree.children) == 2:
                        return [tree.children[0].synth] + tree.children[1].synth
                case NonTerminal(value="FColumn"):
                    return {
                        "type": "fc",
                        "value": tree.children[2].synth,
                    }
                    #return tree.children[2].synth
                case NonTerminal(value="FValue"):
                    return {
                        "type": "fv",
                        "value": tree.children[2].synth,
                    }
                    # return tree.children[2].synth
                case NonTerminal(value="Expr"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) == 3:
                        if tree.children[0].synth["type"] != "common" and tree.children[2].synth["type"] != "common":
                            raise Exception("Оператор or для fv/fc не определен")
                        else:
                            return {
                                "type": "common",
                                "value": tree.children[0].synth['value'] + " " +
                                         tree.children[1].synth + " " + tree.children[2].synth['value']
                            }
                case NonTerminal(value="T1"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) == 3:
                        if tree.children[0].synth["type"] != "common" and tree.children[2].synth["type"] != "common":
                            raise Exception("Оператор and для fv/fc не определен")
                        else:
                            return {
                                "type": "common",
                                "value": tree.children[0].synth['value'] + " " +
                                         tree.children[1].synth + " " + tree.children[2].synth['value']
                            }
                case NonTerminal(value="T2"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) == 2:
                        if tree.children[1].synth["type"] != "common":
                            raise Exception("Оператор not для fv/fc не определен")
                        else:
                            return {
                                "type": "common",
                                "value": tree.children[0].synth + tree.children[1].synth['value']
                            }
                case NonTerminal(value="T3"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) == 3:
                        if tree.children[1].symbol == Terminal(Category.EQUAL):
                            if tree.children[0].synth['type'] == "common" and tree.children[2].synth['type'] == "common":
                                return {
                                    "type": "common",
                                    "value": tree.children[0].synth['value'] + " " + tree.children[1].synth +
                                             " " + tree.children[2].synth['value']
                                }
                            elif tree.children[0].synth['type'] == "fv" and tree.children[2].synth['type'] == "fc":
                                left, right = tree.children[0].synth["value"], tree.children[2].synth['value']
                                env = table
                                return {
                                    "type": "common",
                                    "value": f"((SELECT d-{env.get('threshold')}*(d-c) FROM {env.get('fvtname')} WHERE name=\'{left}\')"\
                                            f"\n>= {env.get('threshold')}*({right}{env.get('columnsuffix')}2-{right}{env.get('columnsuffix')}1)+{right}{env.get('columnsuffix')}1"\
                                            f"\nAND (SELECT (b-a)*{env.get('threshold')}+a FROM {env.get('fvtname')} WHERE name=\'{left}\')"\
                                            f"\n<= {right}{env.get('columnsuffix')}4-({right}{env.get('columnsuffix')}4-{right}{env.get('columnsuffix')}3)*{env.get('threshold')})"
                                }
                            elif tree.children[0].synth['type'] == "fc" and tree.children[2].synth['type'] == "fv":
                                left, right = tree.children[0].synth["value"], tree.children[2].synth['value']
                                env = table
                                return {
                                    "type": "common",
                                    "value": f"({left}{env.get('columnsuffix')}4-{env.get('threshold')}*({left}{env.get('columnsuffix')}4-{left}{env.get('columnsuffix')}3)" \
                                             f"\n>=(SELECT {env.get('threshold')}*(b-a)+a FROM {env.get('fvtname')} WHERE name=\'{right}\')" \
                                             f"\nAND {env.get('threshold')}*({left}{env.get('columnsuffix')}2-{left}{env.get('columnsuffix')}1)+{left}{env.get('columnsuffix')}1" \
                                             f"\n<= (SELECT d-(d-c)*{env.get('threshold')} FROM {env.get('fvtname')} WHERE name=\'{right}\'))"
                                }
                            else:
                                raise Exception("fv/fv или fc/fc или common/fv/fc сочетание")
                        elif tree.children[1].symbol == Terminal(Category.COMPARISON):
                            if tree.children[0].synth["type"] == "common" and tree.children[2].synth["type"] == "common":
                                return {
                                    "type": "common",
                                    "value": tree.children[0].synth['value'] + tree.children[1].synth +
                                             tree.children[2].synth['value']
                                }
                            elif tree.children[0].synth["type"] == tree.children[2].synth["type"] and \
                                (tree.children[0].synth["type"] == "fv" or tree.children[0].synth["type"] == "fc"):
                                raise Exception("Попытка применения оператора сравнения для fv/fv fc/fc сочетаний")
                            elif tree.children[0].synth["type"] == "fc" and tree.children[2].synth["type"] == "fv":
                                left, right = tree.children[0].synth["value"], tree.children[2].synth["value"]
                                env = table
                                if tree.children[1].synth == "<=":
                                    return {
                                        "type": "common",
                                        "value": f"({left}{env.get('columnsuffix')}1+{env.get('threshold')}*({left}{env.get('columnsuffix')}2-{left}{env.get('columnsuffix')}1)"
                                                 f"\n<(SELECT d-{env.get('threshold')}*(d-c) FROM {env.get('fvtname')} WHERE name=\'{right}\'))",
                                    }
                                elif tree.children[1].synth == ">=":
                                    return {
                                        "type": "common",
                                        "value": f"({left}{env.get('columnsuffix')}4+{env.get('threshold')}*({left}{env.get('columnsuffix')}4-{left}{env.get('columnsuffix')}3)"
                                                 f"\n>(SELECT a+{env.get('threshold')}*(b-a) FROM {env.get('fvtname')} WHERE name=\'{right}\'))",
                                    }
                                elif tree.children[1].synth == "<":
                                    return {
                                        "type": "common",
                                        "value": f"({left}{env.get('columnsuffix')}4-{env.get('threshold')}*({left}{env.get('columnsuffix')}4-{left}{env.get('columnsuffix')}3)"
                                                 f"\n<(SELECT a+{env.get('threshold')}*(b-a) FROM {env.get('fvtname')} WHERE name=\'{right}\'))",
                                    }
                                elif tree.children[1].synth == ">":
                                    return {
                                        "type": "common",
                                        "value": f"({left}{env.get('columnsuffix')}1+{env.get('threshold')}*({left}{env.get('columnsuffix')}2-{left}{env.get('columnsuffix')}1)"
                                                 f"\n>(SELECT d-{env.get('threshold')}*(d-c) FROM {env.get('fvtname')} WHERE name=\'{right}\'))",
                                    }
                                elif tree.children[1].synth == "<<":
                                    return {
                                        "type": "common",
                                        "value": f"({left}{env.get('columnsuffix')}1+{env.get('threshold')}*({left}{env.get('columnsuffix')}2-{left}{env.get('columnsuffix')}1)"
                                                 f"\n<=(SELECT {env.get('threshold')}*(b-a)+a FROM {env.get('fvtname')} WHERE name=\'{right}\')"
                                                 f"\n AND {left}{env.get('columnsuffix')}4 - {env.get('threshold')}*({left}{env.get('columnsuffix')}4-{left}{env.get('columnsuffix')}3)"
                                                 f"\n >= (SELECT d-(d-c)*{env.get('threshold')} FROM {env.get('fvtname')} WHERE name=\'{right}\'))",
                                    }
                                elif tree.children[1].synth == ">>":
                                    return {
                                        "type": "common",
                                        "value": f"((SELECT {env.get('threshold')}*(b-a)+a FROM {env.get('fvtname')} WHERE name=\'{right}\')"
                                                 f"\n<={left}{env.get('columnsuffix')}1+{env.get('threshold')}*({left}{env.get('columnsuffix')}2-{left}{env.get('columnsuffix')}1)"
                                                 f"\n AND (SELECT d-(d-c)*{env.get('threshold')} FROM {env.get('fvtname')} WHERE name=\'{right}\')"
                                                 f"\n >= {left}{env.get('columnsuffix')}4 - {env.get('threshold')}*({left}{env.get('columnsuffix')}4-{left}{env.get('columnsuffix')}3))",
                                    }
                                elif tree.children[1].synth == "!=":
                                    return {
                                        "type": "common",
                                        "value": f"({left}{env.get('columnsuffix')}4-{env.get('threshold')}*({left}{env.get('columnsuffix')}4-{left}{env.get('columnsuffix')}3)"
                                            f"\n<(SELECT {env.get('threshold')}*(b-a)+a FROM {env.get('fvtname')} WHERE name=\'{right}\')"
                                            f"\n OR {env.get('threshold')}*({left}{env.get('columnsuffix')}2-{left}{env.get('columnsuffix')}1)+{left}{env.get('columnsuffix')}1"
                                            f"\n > (SELECT d-(d-c)*{env.get('threshold')} FROM {env.get('fvtname')} WHERE name=\'{right}\'))"
                                    }
                            elif tree.children[0].synth["type"] == "fv" and tree.children[2].synth["type"] == "fc":
                                left, right = tree.children[0].synth["value"], tree.children[2].synth["value"]
                                env = table
                                if tree.children[1].synth == "<=":
                                    return {
                                        "type": "common",
                                        "value": f"((SELECT a-{env.get('threshold')}*(b-a) FROM {env.get('fvtname')} WHERE name=\'{left}\')"
                                                 f"\n<{right}{env.get('columnsuffix')}4-{env.get('threshold')}*({right}{env.get('columnsuffix')}4-{right}{env.get('columnsuffix')}3))",
                                    }
                                elif tree.children[1].synth == ">=":
                                    return {
                                        "type": "common",
                                        "value": f"((SELECT d-{env.get('threshold')}*(d-c) FROM {env.get('fvtname')} WHERE name=\'{left}\')"
                                                 f"\n>{right}{env.get('columnsuffix')}1+{env.get('threshold')}*({right}{env.get('columnsuffix')}2-{right}{env.get('columnsuffix')}1))",
                                    }
                                elif tree.children[1].synth == "<":
                                    return {
                                        "type": "common",
                                        "value": f"((SELECT d-{env.get('threshold')}*(d-c) FROM {env.get('fvtname')} WHERE name=\'{left}\')"
                                                 f"\n<{right}{env.get('columnsuffix')}1+{env.get('threshold')}*({right}{env.get('columnsuffix')}2-{right}{env.get('columnsuffix')}1))",
                                    }
                                elif tree.children[1].synth == ">":
                                    return {
                                        "type": "common",
                                        "value": f"((SELECT a+{env.get('threshold')}*(b-a) FROM {env.get('fvtname')} WHERE name=\'{left}\')"
                                                 f"\n>{right}{env.get('columnsuffix')}4-{env.get('threshold')}*({right}{env.get('columnsuffix')}4-{right}{env.get('columnsuffix')}3))",
                                    }
                                elif tree.children[1].synth == "<<":
                                    return {
                                        "type": "common",
                                        "value": f"((SELECT a+{env.get('threshold')}*(b-a) FROM {env.get('fvtname')} WHERE name=\'{left}\')"
                                                 f"\n <= {env.get('threshold')}*({right}{env.get('columnsuffix')}2-{right}{env.get('columnsuffix')}1)+{right}{env.get('columnsuffix')}1"
                                                 f"\n AND (SELECT d-(d-c)*{env.get('threshold')} FROM {env.get('fvtname')} WHERE name=\'{left}\')"
                                                 f"\n >= {right}{env.get('columnsuffix')}4-({right}{env.get('columnsuffix')}4-{right}{env.get('columnsuffix')}3)*{env.get('threshold')})",
                                    }
                                elif tree.children[1].synth == ">>":
                                    return {
                                        "type": "common",
                                        "value": f"({env.get('threshold')}*({right}{env.get('columnsuffix')}2-{right}{env.get('columnsuffix')}1)+{right}{env.get('columnsuffix')}1"
                                                 f"\n <= (SELECT a+{env.get('threshold')}*(b-a) FROM {env.get('fvtname')} WHERE name=\'{left}\')"
                                                 f"\n AND {right}{env.get('columnsuffix')}4-({right}{env.get('columnsuffix')}4-{right}{env.get('columnsuffix')}3)*{env.get('threshold')}"
                                                 f"\n >= (SELECT d-(d-c)*{env.get('threshold')} FROM {env.get('fvtname')} WHERE name=\'{left}\'))",
                                    }
                                elif tree.children[1].synth == "!=":
                                    return {
                                        "type": "common",
                                        "value": f"((SELECT d-{env.get('threshold')}*(d-c) FROM {env.get('fvtname')} WHERE name=\'{left}\')"
                                        f"\n < {env.get('threshold')}*({right}{env.get('columnsuffix')}2-{right}{env.get('columnsuffix')}1)+{right}{env.get('columnsuffix')}1"
                                        f"\n OR (SELECT (b-a)*{env.get('threshold')}+a FROM {env.get('fvtname')} WHERE name=\'{left}\')"
                                        f"\n > {right}{env.get('columnsuffix')}4-({right}{env.get('columnsuffix')}4-{right}{env.get('columnsuffix')}3)*{env.get('threshold')})"
                                    }
                        else:
                            return {
                                "type": "common",
                                "value": tree.children[0].synth['value'] + tree.children[1].synth +
                                         tree.children[2].synth['value']
                            }
                case NonTerminal(value="T4"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) == 3:
                        if tree.children[2].synth["type"] != "common" or tree.children[0].synth["type"] != "common":
                            raise Exception("Оператор сложения для fv/fc не определен")
                        else:
                            return {
                                "type": "common",
                                "value": tree.children[0].synth['value'] + tree.children[1].synth +
                                         tree.children[2].synth['value']
                            }
                case NonTerminal(value="T5"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) == 3:
                        if tree.children[2].synth["type"] != "common" or tree.children[0].synth["type"] != "common":
                            raise Exception("Оператор умножения/деления для fv/fc не определен")
                        else:
                            return {
                                "type": "common",
                                "value": tree.children[0].synth['value'] + tree.children[1].synth +
                                         tree.children[2].synth['value']
                            }
                case NonTerminal(value="T6"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) == 3:
                        if tree.children[2].synth["type"] != "common" or tree.children[0].synth["type"] != "common":
                            raise Exception("Экспонентный оператор для fv/fc не определен")
                        else:
                            return {
                                "type": "common",
                                "value": tree.children[0].synth['value'] + tree.children[1].synth + tree.children[2].synth['value']
                            }
                case NonTerminal(value="Unary"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    elif len(tree.children) == 2:
                        if tree.children[1].synth['type'] != "common":
                            raise Exception("Унарный оператор для fv/fc не определен")
                        else:
                            return {
                                "type": "common",
                                "value": tree.children[0].synth + tree.children[1].synth["value"]
                            }
                case NonTerminal(value="Factor"):
                    if len(tree.children) == 1:
                        if isinstance(tree.children[0].synth, str):
                            return {
                                "type": "common",
                                "value": tree.children[0].synth,
                            }
                        else:
                            return tree.children[0].synth
                    else:
                        d = tree.children[1].synth.copy()
                        d["value"] = synthAll(tree)
                        return d
                case NonTerminal(value="FFactor"):
                    return tree.children[1]
                case NonTerminal(value="FT3"):
                    if tree.children[1].symbol == Terminal(Category.EQUAL):
                        if tree.children[0].symbol.value == NonTerminal("FValue").value:
                            id = tree.children[2].synth
                            name = tree.children[0].synth['value']
                            return get_query_ft3(id, name, table)
                        else:
                            id = tree.children[0].synth
                            name = tree.children[2].synth['value']
                            return get_query_ft3(id, name, table)
                case NonTerminal(value="FT2"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    else:
                        return "(1 - " + tree.children[1].synth + ")"
                case NonTerminal(value="FT1"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    else:
                        return "least(" + tree.children[0].synth + ", " + tree.children[2].synth + ")"
                case NonTerminal(value="FExpr"):
                    if len(tree.children) == 1:
                        return tree.children[0].synth
                    else:
                        return "GREATEST(" + tree.children[0].synth + ", " + tree.children[2].synth + ")"
                case NonTerminal(value="FSelectWhere"):
                    if len(tree.children) == 1:
                        return ""
                    else:
                        return tree.children[1].synth
                case NonTerminal(value="FSelect"):
                    if len(tree.children) == 5:
                        add = ""
                        order_add = ""
                        if tree.children[4].synth:
                            order_add = tree.children[4].synth
                        else:
                            order_add = "order by mf desc"
                        if tree.children[3].synth:
                            add = ", " + tree.children[3].synth + " as mf"
                        return "SELECT " + tree.children[1].synth + add + " " + tree.children[2].synth + " " \
                               + order_add + " "
                    else:
                        add = ""
                        order_add = ""
                        if tree.children[4].synth:
                            order_add = tree.children[4].synth
                        else:
                            order_add = "order by mf desc"
                        if tree.children[3].synth:
                            add = ", " + tree.children[3].synth + " as mf"

                        return "SELECT " + tree.children[1].synth + add + " " + tree.children[2].synth + " " \
                               + order_add + " " + tree.children[5].synth
                case _:
                    return synthAll(tree)