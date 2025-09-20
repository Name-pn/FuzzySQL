import pandas as pd

from libraries.Analyzer import Analyzer
from libraries.SLR.SLRTable import SLRTable

class SLRAnalyzer(Analyzer):
    def _create_table(self):
        return SLRTable(self.gr)
