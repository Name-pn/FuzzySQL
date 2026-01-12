from libraries.Environment import Environment
from libraries.LALR.LALRAnalyzerCST import LALRAnalyzerCST
from libraries.Lexer import SQLLexer
from libraries.Grammar.Grammar import Grammar
from libraries.Tree.TreeCst import TreeCstNode
from graphviz import Digraph

def new_name(lst: list):
    last = lst[-1]
    if last[-1] != 'Z':
        lst.append(lst[-1][:-1] + chr(ord(last[-1]) + 1))
    else:
        lst.append(last + "A")
    return lst[-1]

def draw_node(parent: str, graph: Digraph, tree: TreeCstNode, names: list):
    if parent == "":
        first = "A"
        names.append(first)
        graph.node(first, str(tree.symbol))
        for child in tree.children:
            draw_node(first, graph, child, names)
    else:
        local = new_name(names)
        graph.node(local, str(tree.symbol))
        graph.edge(parent, local, constraint="true")
        for child in tree.children:
            draw_node(local, graph, child, names)


def draw(tree: TreeCstNode):
   graph = Digraph('test_table', comment="first test table")
   draw_node("", graph, tree, [])
   graph.render("tree", directory="./artifacts/", format='pdf')


if __name__ == "__main__":
    command = "SELECT * FROM table1; add a(1, 2, 3, 4)"

    table = Environment()
    table.load("./parser_data/conf.pkl")

    grammar_from_txt = Grammar.load("parser_data/grammar.txt")
    lexer = SQLLexer(table)
    parser = LALRAnalyzerCST(grammar_from_txt)

    tokens = lexer.tokenize(command)
    tree = parser.parse(tokens)
    print(tree)
    draw(tree)
