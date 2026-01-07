import pandas as pd

from libraries.Environment import Environment
from libraries.LALR.LALRAnalyzerCST import LALRAnalyzerCST
from libraries.Lexer import SQLLexer
from libraries.Grammar.Grammar import Grammar

if __name__ == "__main__":
    command = "SELECT * FROM table1;"

    table = Environment()
    table.load("conf.pkl")

    lexer = SQLLexer(table)
    grammar_from_txt = Grammar.load("parser_data/grammar.txt")
    parser = LALRAnalyzerCST(grammar_from_txt)

    tokens = lexer.tokenize(command)
    tree = parser.parse(tokens)

    pd.set_option('display.width', 400)
    pd.set_option('display.max_columns', None)

    table: pd.DataFrame = parser.history.copy()
    table = table.drop("Номер", axis=1)
    print(table)


