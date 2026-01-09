import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from libraries.Environment import Environment
from libraries.Extension import ExtensionCursor
from libraries.FunctionHub import FunctionHub

from libraries.Grammar.CurrentGr import gr

conn = psycopg2.connect(host="localhost", port=5433,
                            dbname="postgres", user="postgres",
                            password="1111", connect_timeout=10, sslmode="prefer")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
common_cursor = conn.cursor()
conn.cursor_factory = ExtensionCursor
cursor = conn.cursor()
table = Environment()
table.load()
fh = FunctionHub(common_cursor, table)
cursor.set_fh(fh)
cursor.set_table(table)
print(gr)
# parser = LALRAnalyzer(gr)
test_string = "UPDATE table1 SET fc:fuzzy_column = fv:medium_temperature WHERE name = \'medium_temperature\';" #"add high_number (999, 1001, 1111, 1200);" \
              #"modify high_number (10, 10, 11, 12);" \
              #"remove high_number;"#"ALTER TABLE table1 MODIFY (column1 VARCHAR(10) NULL, column2 INTEGER NOT NULL, column3 REAL DEFAULT NULL UNIQUE);"
cursor.execute(test_string)
table.save()
              #"add medium_value (120, 140, 160, 200);" \
              #        "add low_value (10, 50, 70, 100);" \
              #"modify low_value(90, 120, 140, 180.0);" \
              #"remove low_value"
#"add high_number (999, 1001, 1111, 1200);" \
#              "CREATE TABLE table1(column1 INTEGER PRIMARY KEY, column2 VARCHAR(10));"
# table = Environment()
# table.load()
# lexer = SQLLexer(table)
# tokens = lexer.tokenize(test_string)
# print(parser.parse(tokens))
# pd.set_option('display.width', 400)
# pd.set_option('display.max_columns', None)
# print(parser.history)
# tree = parser.build_tree(tokens)
# print(tree)
# if tree is not None:
#     tree.postOrderVisit(lambda tree: broadcast(tree, ))
#     print("Broadcast: \'", tree.synth, "\'")
#     #tree.postOrderVisit(output)
#     table.save()