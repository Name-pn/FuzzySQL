from psycopg2.extensions import cursor, connection

from CurrentGr import gr
from libraries.CodeGen import broadcast
from libraries.Environment import Environment
from libraries.Lexer import SQLLexer
from libraries.FunctionHub import FunctionHub
import pandas as pd
from libraries.LALR.LALRAnalyzer import LALRAnalyzer

class ExtensionCursor(cursor):
    def __init__(self, *args, **kwargs):
        self.parser = LALRAnalyzer(gr)
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
                print("Success syntax analize")
            else:
                # Показать все строки
                pd.set_option('display.max_rows', None)
                # Ширина отображения (в символах)
                pd.set_option('display.width', 250)
                # Показать все столбцы
                pd.set_option('display.max_columns', None)
                print(self.parser.history)
                print("Syntax error")
            tree = self.parser.build_tree(tokens)
        except Exception as e:
            print(e.args)

        if flag:
            self.fh.addFuzzyTable()
            tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
            print(tree.synth)
            #if tree.synth:
            #    super().execute(tree.synth)
