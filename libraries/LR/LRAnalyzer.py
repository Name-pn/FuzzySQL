from libraries.Analyzer import Analyzer
from libraries.LR.LRTable import LRTable

class LRAnalyzer(Analyzer):
    def _create_table(self):
        return LRTable(self.gr)
