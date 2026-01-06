from libraries.Environment import Environment
from libraries.Lexer import SQLLexer

expr = "SELECT 25*6/23"
table = Environment()
table.load('../conf.pkl')
sql_lexer = SQLLexer(table)
tokens = sql_lexer.tokenize(expr)
print(tokens)