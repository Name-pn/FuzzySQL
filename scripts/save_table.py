from libraries.LALR.LALRTable import LALRTable
from libraries.SLR.SLRTable import SLRTable
from libraries.Grammar.Grammar import Grammar

table_name = "./parser_data/table.pkl" #_test

if __name__ == "__main__":
    grammar_from_txt = Grammar.load("parser_data/grammar.txt") #parser_data/grammar_test.txt
    table = LALRTable(grammar_from_txt)
    #table = SLRTable(grammar_from_txt)
    table.to_pickle(table_name)