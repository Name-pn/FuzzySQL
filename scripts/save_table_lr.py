from libraries.LR.LRTable import LRTable
from libraries.Grammar.Grammar import Grammar

table_name = "./parser_data/table_test.pkl"

if __name__ == "__main__":
    grammar_from_txt = Grammar.load("parser_data/grammar_test.txt")
    table = LRTable(grammar_from_txt)
    table.to_pickle(table_name)