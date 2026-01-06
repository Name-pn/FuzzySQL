import pandas as pd

from libraries.Analyzer import Analyzer
from scripts.save_table import table_name


class LALRAnalyzerCST(Analyzer):
    def _create_table(self):
        table = pd.read_pickle(table_name)
        return table
        #return LALRTable(self.gr)