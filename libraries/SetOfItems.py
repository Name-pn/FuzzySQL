class SetOfItems():
    def __init__(self):
        self.set = []

    def append(self, pair):
        self.set.append(pair)

    def is_empty(self):
        return len(self.set) == 0

    def __str__(self):
        string = "{"
        for el in self.set:
            string += str(el) + ", "
        string = string[:-2]
        string += "}"
        return string

    def __eq__(self, other):
        if len(self.set) != len(other.set):
            return False
        for el in self.set:
            if not el in other.set:
                return False
        return True