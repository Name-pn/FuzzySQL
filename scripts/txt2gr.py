from libraries.Grammar.Grammar import Grammar
from CurrentGr import gr

if __name__ == "__main__":
    gr2 = Grammar.load("../parser_data/grammar.txt")
    print(gr2 == gr)


