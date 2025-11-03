import unittest

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from CurrentGr import gr
from libraries.CodeGen import broadcast
from libraries.Environment import Environment
from libraries.FunctionHub import FunctionHub
from libraries.LALR.LALRAnalyzerCST import LALRAnalyzerCST
from libraries.Lexer import SQLLexer

class TesterSyntax(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parser = LALRAnalyzerCST(gr)
        cls.table = Environment()
        cls.table.load()
        cls.lexer = SQLLexer(cls.table)

    def test_add_command(self):
        test_string = "add high_number (999, 1001, 1111, 1200);"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_add_command_false(self):
        test_string = "add high_number (999, 1001, 1111, 1200.1, 55);"
        tokens = self.lexer.tokenize(test_string)
        self.assertRaises(Exception, self.parser.parse, tokens)

    def test_modify(self):
        test_string = "modify high_number (10, 10, 11, 12)"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_modify_false(self):
        test_string = "modify high_number id2 (10, 10, 11, 12)"
        tokens = self.lexer.tokenize(test_string)
        self.assertRaises(Exception, self.parser.parse, tokens)

    def test_remove(self):
        test_string = "remove high_number;"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_set(self):
        test_string = "set threshold 0.2;" \
                      "set columnprefix 'fuzCol'"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_create_table(self):
        test_string = "CREATE TABLE table1 (column1 INTEGER PRIMARY KEY, column2 VARCHAR(10) UNIQUE NULL, column3 FUZZY);"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_modify_table1(self):
        test_string = "ALTER TABLE table1 MODIFY (column1 VARCHAR(10), column2 INTEGER, column3 REAL);"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_modify_table2(self):
        test_string = "ALTER TABLE table1 MODIFY (column1 FUZZY);"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_drop_table_1(self):
        test_string = "ALTER TABLE table1 DROP (column1, column2);"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_drop_table_2(self):
        test_string = "ALTER TABLE table1 DROP (fc:column1);"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_rename(self):
        test_string = "ALTER TABLE table1 RENAME column1 column2;"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_add_table_1(self):
        test_string = "ALTER TABLE table3 ADD (column1 INT UNIQUE NOT NULL, column2 FUZZY, column3 INT);"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_insert(self):
        test_string = "INSERT INTO some_table (fc:fuzzy_column) VALUES (1, 2, 3, 4);"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_update(self):
        test_string = "UPDATE table1 SET fc:fuzzy_column = fv:high_pressure;"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_delete_1(self):
        test_string = "DELETE FROM table1 WHERE fc:fuzzy_column = fv:low;"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_delete_2(self):
        test_string = "DELETE FROM table1;"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_select_0(self):
        test_string = "SELECT 5+6.4 > 10, 5 - 4 + (-3);"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_select_1(self):
        test_string = "SELECT * FROM table1;"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_select_2(self):
        test_string = "SELECT fc:column FROM table1 WHERE fc:column > 6;"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))

    def test_select_3(self):
        test_string = "SELECT id FROM table1 WHERE fc:column = fv:value ORDER BY fc:column ASC WITH 0.3;"
        tokens = self.lexer.tokenize(test_string)
        self.assertTrue(self.parser.parse(tokens))


class TesterBroadcast(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parser = LALRAnalyzerCST(gr)
        cls.table = Environment()
        cls.table.load()
        cls.lexer = SQLLexer(cls.table)
        conn = psycopg2.connect(host="localhost", port=5433,
                                dbname="postgres", user="postgres",
                                password="1111", connect_timeout=10, sslmode="prefer")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        common_cursor = conn.cursor()
        cls.fh = FunctionHub(common_cursor, cls.table)

    def test_add_command(self):
        test_string = "add high_number (999, 1001, 1111, 1200);"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth, f"INSERT INTO {self.table.get('fvtname')}(name, a, b, c, d) VALUES ('high_number', 999, 1001, 1111, 1200);\n")

    def test_modify(self):
        test_string = "modify high_number (10, 12, 14, 16.05)"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth, f"UPDATE {self.table.get('fvtname')} SET name = \'high_number\', a = 10, b = 12, c = 14, d = 16.05 WHERE name = \'high_number\'")

    def test_remove(self):
        test_string = "remove high_number;"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth, f"DELETE FROM {self.table.get('fvtname')} WHERE name = \'high_number\';\n")

    def test_set(self):
        test_string = "set threshold 0.5;" \
                      "set columnprefix 'fc'"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth, f"")

    def test_create_table(self):
        test_string = "CREATE TABLE table1 (column1 INTEGER PRIMARY KEY, column2 VARCHAR(10) UNIQUE NULL, column3 FUZZY);"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth, f"CREATE TABLE table1 ( column1 INTEGER PRIMARY KEY, column2 VARCHAR ( 10 ) UNIQUE NULL, column3_f1 REAL, column3_f2 REAL, column3_f3 REAL, column3_f4 REAL );\n")

    def test_modify_table1(self):
        test_string = "ALTER TABLE table1 MODIFY (column1 VARCHAR(10), column2 INTEGER, column3 REAL);"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth, f"ALTER TABLE table1 DROP CONSTRAINT table1_column3_key,\n"
                                     f"ALTER COLUMN column1 TYPE VARCHAR ( 10 ),\n"
                                     f"ALTER COLUMN column2 TYPE INTEGER,\n"
                                     f"ALTER COLUMN column3 TYPE REAL;\n")

    def test_modify_table2(self):
        test_string = "ALTER TABLE table1 MODIFY (column1 FUZZY);"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        # self.assertFalse(self.parser.parse(tokens))
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth, f"ALTER TABLE table1 DROP CONSTRAINT table1_column3_key,\n"
                                     f"ALTER COLUMN {'column1'+self.table.get('columnsuffix')+'1'} TYPE REAL,\n"
                                     f"ADD COLUMN {'column1'+self.table.get('columnsuffix')+'2'} REAL,\n"
                                     f"ADD COLUMN {'column1'+self.table.get('columnsuffix')+'3'} REAL,\n"
                                     f"ADD COLUMN {'column1'+self.table.get('columnsuffix')+'4'} REAL;\n")

    def test_modify_table3(self):
        test_string = "ALTER TABLE table1 MODIFY (column1 VARCHAR(10) NULL, column2 INTEGER NOT NULL, column3 REAL DEFAULT 3.3 UNIQUE);"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth, f"ALTER TABLE table1 DROP CONSTRAINT table1_column3_key,\n"
                                     f"ALTER COLUMN column1 TYPE VARCHAR ( 10 ),\n"
                                     f"ALTER COLUMN column1 DROP NOT NULL,\n"
                                     f"ALTER COLUMN column2 TYPE INTEGER,\n"
                                     f"ALTER COLUMN column2 SET NOT NULL,\n"
                                     f"ALTER COLUMN column3 TYPE REAL,\n"
                                     f"ALTER COLUMN column3 SET DEFAULT 3.3,\n"
                                     f"ADD UNIQUE (column3);\n")

    def test_isFuzzy(self):
        self.assertTrue(self.fh.isFuzzy("table2", "column1"))

    def test_drop_table_1(self):
        test_string = "ALTER TABLE table1 DROP (column1, column2);"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"ALTER TABLE table1 DROP COLUMN column1,\n"
                         f"DROP COLUMN column2;\n")

    def test_drop_table_2(self):
        test_string = "ALTER TABLE table2 DROP (fc:column1);"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"ALTER TABLE table2 DROP COLUMN {'column1' + self.table.get('columnsuffix') + '1'},\n"
                         f"DROP COLUMN {'column1' + self.table.get('columnsuffix') + '2'},\n"
                         f"DROP COLUMN {'column1' + self.table.get('columnsuffix') + '3'},\n"
                         f"DROP COLUMN {'column1' + self.table.get('columnsuffix') + '4'};\n")

    def test_drop_table_3(self):
        test_string = "ALTER TABLE table3 DROP (fc:column1, column2, fc:column3);"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"ALTER TABLE table3 DROP COLUMN {'column1' + self.table.get('columnsuffix') + '1'},\n"
                         f"DROP COLUMN {'column1' + self.table.get('columnsuffix') + '2'},\n"
                         f"DROP COLUMN {'column1' + self.table.get('columnsuffix') + '3'},\n"
                         f"DROP COLUMN {'column1' + self.table.get('columnsuffix') + '4'},\n"
                         f"DROP COLUMN column2,\n"
                         f"DROP COLUMN {'column3' + self.table.get('columnsuffix') + '1'},\n"
                         f"DROP COLUMN {'column3' + self.table.get('columnsuffix') + '2'},\n"
                         f"DROP COLUMN {'column3' + self.table.get('columnsuffix') + '3'},\n"
                         f"DROP COLUMN {'column3' + self.table.get('columnsuffix') + '4'};\n")

    #todo Неплохо бы сделать списком, а не по одному значению
    def test_rename_table_1(self):
        test_string = "ALTER TABLE table3 RENAME column1 column2;"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"ALTER TABLE table3 RENAME COLUMN column1 TO column2;\n")

    def test_add_table_1(self):
        test_string = "ALTER TABLE table3 ADD (column1 INT UNIQUE NOT NULL, column2 FUZZY);"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"ALTER TABLE table3 ADD COLUMN column1 INT UNIQUE NOT NULL,\n"
                         f"ADD COLUMN {'column2' + self.table.get('columnsuffix') + '1'} REAL,\n"
                         f"ADD COLUMN {'column2' + self.table.get('columnsuffix') + '2'} REAL,\n"
                         f"ADD COLUMN {'column2' + self.table.get('columnsuffix') + '3'} REAL,\n"
                         f"ADD COLUMN {'column2' + self.table.get('columnsuffix') + '4'} REAL;\n")

    def test_insert_1(self):
        test_string = "INSERT INTO some_table (fc:fuzzy_column) VALUES (1, 2, 3, 4);"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"INSERT INTO some_table (fuzzy_column{self.table.get('columnsuffix') + '1'}, "
                         f"fuzzy_column{self.table.get('columnsuffix') + '2'}, "
                         f"fuzzy_column{self.table.get('columnsuffix') + '3'}, "
                         f"fuzzy_column{self.table.get('columnsuffix') + '4'})\n"
                         f"VALUES (1, 2, 3, 4);\n")

    def test_insert_2(self):
        test_string = "INSERT INTO some_table (fc:fuzzy_column, columnx) VALUES (1, 2, 3, 4, 'str'), (5, 6, 7, 8, 'str2');"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"INSERT INTO some_table (fuzzy_column{self.table.get('columnsuffix') + '1'}, "
                         f"fuzzy_column{self.table.get('columnsuffix') + '2'}, "
                         f"fuzzy_column{self.table.get('columnsuffix') + '3'}, "
                         f"fuzzy_column{self.table.get('columnsuffix') + '4'}, "
                         f"columnx)\n"
                         f"VALUES (1, 2, 3, 4, 'str'),\n"
                         f"(5, 6, 7, 8, 'str2');\n")

    def test_insert_3(self):
        test_string = "INSERT INTO some_table VALUES (1, 2, 3, 4, 'str'), (5, 6, 7, 8, 'str2');"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"INSERT INTO some_table VALUES (1, 2, 3, 4, 'str'),\n"
                         f"(5, 6, 7, 8, 'str2');\n")

    def test_update_1(self):
        test_string = "UPDATE table1 SET fc:fcolumn = fv:high;"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"UPDATE table1 SET fcolumn_f1 = (SELECT a FROM fuzzyvalues WHERE name = 'high'),\n"
                         f"fcolumn_f2 = (SELECT b FROM fuzzyvalues WHERE name = 'high'),\n"
                         f"fcolumn_f3 = (SELECT c FROM fuzzyvalues WHERE name = 'high'),\n"
                         f"fcolumn_f4 = (SELECT d FROM fuzzyvalues WHERE name = 'high');\n")

    def test_update_2(self):
        test_string = "UPDATE table1 SET fc:fcolumn = fv:high, column2 = 5;"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"UPDATE table1 SET fcolumn_f1 = (SELECT a FROM fuzzyvalues WHERE name = 'high'),\n"
                         f"fcolumn_f2 = (SELECT b FROM fuzzyvalues WHERE name = 'high'),\n"
                         f"fcolumn_f3 = (SELECT c FROM fuzzyvalues WHERE name = 'high'),\n"
                         f"fcolumn_f4 = (SELECT d FROM fuzzyvalues WHERE name = 'high'),\n"
                         f"column2 = 5;\n")

    def test_update_3(self):
        test_string = "UPDATE table1 SET fc:fuzzy_column = fv:medium_temperature WHERE name = \'medium_temperature\';"
        tokens = self.lexer.tokenize(test_string)
        tree = self.parser.parse(tokens)
        tree.postOrderVisit(lambda tree: broadcast(tree, self.fh))
        self.assertEqual(tree.synth,
                         f"UPDATE table1 SET fuzzy_column_f1 = (SELECT a FROM fuzzyvalues WHERE name = 'medium_temperature'),\n"
                         f"fuzzy_column_f2 = (SELECT b FROM fuzzyvalues WHERE name = 'medium_temperature'),\n"
                         f"fuzzy_column_f3 = (SELECT c FROM fuzzyvalues WHERE name = 'medium_temperature'),\n"
                         f"fuzzy_column_f4 = (SELECT d FROM fuzzyvalues WHERE name = 'medium_temperature')\n"
                         f"WHERE name = \'medium_temperature\';\n")



    

if __name__ == "__main__":
    unittest.main()