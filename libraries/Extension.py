from psycopg2.extensions import cursor

from libraries.CodeGen import broadcast
from libraries.Grammar.Grammar import Grammar
from libraries.Lexer import SQLLexer
import pandas as pd
from libraries.LALR.LALRAnalyzerCST import LALRAnalyzerCST

class ExtensionCursor(cursor):
    def __init__(self, *args, **kwargs):
        grammar = Grammar.load("./parser_data/grammar.txt")
        self.parser = LALRAnalyzerCST(grammar)
        self.fh = None
        self.table = None
        super().__init__(*args, **kwargs)

    def set_fh(self, fh):
        self.fh = fh

    def set_table(self, table):
        self.table = table

    def execute(self, query, vars=None):
        if self.fh is None or self.table is None:
            print(f"FunctionHub или Environment в курсоре не инициализированы")
            return
        lexer = SQLLexer(self.table)
        tokens = lexer.tokenize(query)
        flag = self.parser.parse(tokens)
        try:
            if flag:
                pass
                #print("Success syntax analize")
            else:
                # Показать все строки
                pd.set_option('display.max_rows', None)
                # Ширина отображения (в символах)
                pd.set_option('display.width', 250)
                # Показать все столбцы
                pd.set_option('display.max_columns', None)
                print(self.parser.history)
                print("Syntax error")
            tree = self.parser.parse(tokens)
        except Exception as e:
            print(e.args)

        if flag:
            self.fh.addFuzzyTable()
            tree.postOrderVisit(lambda tree: broadcast(tree, self.fh, self.table))
            #print(tree.synth)
            if tree.synth:
                return super().execute(tree.synth)
            #if tree.synth:

