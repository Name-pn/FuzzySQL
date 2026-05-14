import pandas as pd

from libraries.Environment import Environment
#from libraries.Symbol.Terminal import tokenSpecificationTest
from libraries.LALR.LALRAnalyzerCST import LALRAnalyzerCST
from libraries.LR.LRAnalyzer import LRAnalyzer
from libraries.Lexer import SQLLexer, DefaultLexer
from libraries.Grammar.Grammar import Grammar

if __name__ == "__main__":
    command = "ADD a(5, 4.5, 5, 5.0);"

    table = Environment()
    table.load("./parser_data/conf.pkl")

    lexer = SQLLexer(table)
    grammar_from_txt = Grammar.load("parser_data/grammar.txt")
    parser = LALRAnalyzerCST(grammar_from_txt)

    tokens = lexer.tokenize(command)
    try:
        tree = parser.parse(tokens)
    except Exception as e:
        print(e.__str__())

    pd.set_option('display.width', 400)
    pd.set_option('display.max_columns', None)

    table: pd.DataFrame = parser.history.copy()
    table = table.drop("Номер", axis=1)
    print(table)


