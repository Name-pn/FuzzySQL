# import tkinter as tk
# from tkinter import ttk
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Тест колонок")
#     columns = ["test1", 'test2']
#     tree = ttk.Treeview(master=root, columns=columns)
#     tree["displaycolumns"] = []
#     for col in columns:
#         tree.heading(col, text=col)
#         tree.column(col, width=75, minwidth=50, stretch=True, anchor=tk.CENTER)  # можно настроить ширину
#     tree.pack(fill=tk.BOTH, expand=True)
#     root.mainloop()

from antlr4 import *
from pympler import asizeof

from parser_data.old.gen.SqlLexer import SqlLexer
from parser_data.old.gen.SqlParser import SqlParser



# Простой запрос
from libraries.Environment import Environment
from libraries.Lexer import SQLLexer
from libraries.Symbol.SymbolType import SymbolType#SymbolType, sample
from libraries.Symbol.Terminal import TokenType

test_input = "SELECT * FROM users WHERE a > 5;"

input_stream = InputStream(test_input)
lexer = SqlLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = SqlParser(stream)

# Попробуй распарсить
tree = parser.start()  # или s() — твоё стартовое правило

# Если нет ошибок — всё работает
print("Парсинг успешен!")

table = Environment()
table.load("./parser_data/conf.pkl")
lexer2 = SQLLexer(table)
tokens = lexer2.tokenize("""
--comment
SELECT * FROM table2;
""")
print(tokens)

import sys
print("tokens size", asizeof.asizeof(tokens))
print("size lexer ", sys.getsizeof(lexer2))
print("size of SymbolType ", sys.getsizeof(SymbolType.__class__))
print("size of venum SymbolType ", asizeof.asizeof(SymbolType.TERMINAL))
print("size of TerminalType ", sys.getsizeof(TokenType.__class__))