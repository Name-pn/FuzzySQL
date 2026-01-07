from libraries.LALR.LALRTable import LALRTable
from libraries.Grammar.Grammar import Grammar

table_name = "table.pkl"

if __name__ == "__main__":
    grammar_from_txt = Grammar.load("parser_data/grammar.txt")
    table = LALRTable(grammar_from_txt)
    table.to_pickle(table_name)