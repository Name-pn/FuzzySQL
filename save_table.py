from CurrentGr import gr
from libraries.LALR.LALRTable import LALRTable

table_name = "table.pkl"

if __name__ == "__main__":
    print(gr)
    table = LALRTable(gr)
    table.to_pickle(table_name)