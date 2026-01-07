import pandas as pd

from libraries.Environment import Environment
from libraries.LALR.LALRAnalyzerCST import LALRAnalyzerCST
from libraries.Lexer import SQLLexer
from libraries.Grammar.Grammar import Grammar

if __name__ == "__main__":
    command = "SELECT * FROM table1;"

    table = Environment()
    table.load("conf.pkl")

    grammar_from_txt = Grammar.load("parser_data/grammar.txt")
    lexer = SQLLexer(table)
    parser = LALRAnalyzerCST(grammar_from_txt)

    tokens = lexer.tokenize(command)
    tree = parser.parse(tokens)

    print(tree)


