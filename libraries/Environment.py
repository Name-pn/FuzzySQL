import pickle
import copy

class Environment():
    def __init__(self):
        self.table = {}
        self.prev = None

    def copy(self):
        return copy.deepcopy(self)

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.table, f)

    def load(self, path = 'conf.pkl'):
        with open(path, 'rb') as f:
            self.table = pickle.load(f)

    def startInit(self):
        self.table.clear()
        self.table['threshold'] = 0.5
        self.table['columnprefix'] = 'fc'
        self.table['valueprefix'] = 'fv'
        self.table['fvtname'] = 'fuzzyvalues'
        self.table['columnsuffix'] = '_f'

    def get(self, key):
        local = self.table.get(key)
        if local is None:
            if self.prev is not None:
                return self.prev.get(key)
            else:
                return None
        else:
            return local

    def put(self, key, value):
        self.table[key] = value

    def addEnv(self):
        newEnv = Environment()
        newEnv.prev = self
        return newEnv