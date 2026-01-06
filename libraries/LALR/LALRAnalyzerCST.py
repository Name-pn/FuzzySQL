import pandas as pd

from libraries.Analyzer import Analyzer
from libraries.TreeMixins.MixinCST import MixinCST
from scripts.save_table import table_name


class LALRAnalyzerCST(MixinCST, Analyzer):
    def __init__(self, gr):
        MixinCST.__init__(self)
        Analyzer.__init__(self, gr)

    def _create_table(self):
        table = pd.read_pickle(table_name)
        return table
        #return LALRTable(self.gr)

    def parse(self, tokens):
        self.parse_stack.clear()
        self.recognize(tokens)
        if len(self.parse_stack) != 1:
            raise Exception("В стеке не 1 нода")
        return self.parse_stack[0]