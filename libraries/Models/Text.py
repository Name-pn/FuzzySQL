from libraries.Models.Cursor import Cursor
from libraries.Patterns.Observable import Observable

class Text(Observable):
    def __init__(self, array, width, height):
        super().__init__()
        self.array_of_strings = array
        self.max_row_len = self._max_row_len()
        self.max_column_len = len(array)
        self.width = width
        self.height = height

    def update_metrics(self):
        self.max_row_len = self._max_row_len()
        self.max_column_len = len(self.array_of_strings)

    def change_text(self, text_array):
        self.array_of_strings = text_array
        self.max_row_len = self._max_row_len()
        self.max_column_len = len(text_array)
        self.notify(self.get_text())

    def get_text(self):
        res = ""
        for str in self.array_of_strings:
            res += str + "\n"
        return res[:-1]

    def row_len(self, i):
        return len(self.array_of_strings[i])

    def _max_row_len(self):
        res = 0
        for row in self.array_of_strings:
            if len(row) > res:
                res = len(row)
        return res

    def add_char(self, indexes, char):
        i, j = indexes
        self.array_of_strings[i] = self.array_of_strings[i][:j] + char + self.array_of_strings[i][j:]
        self.update_metrics()
        self.notify(self.get_text())

    def delete_char(self, indexes):
        i, j = indexes
        if i == 0 and j == -1:
            return
        if j != -1:
            self.array_of_strings[i] = self.array_of_strings[i][:j] + self.array_of_strings[i][j+1:]
        else:
            string = self.array_of_strings.pop(i)
            self.array_of_strings[i-1] = self.array_of_strings[i-1] + string
        self.update_metrics()
        self.notify(self.get_text())

    def add_newline(self, indexes):
        i, j = indexes
        left, right = self.array_of_strings[i][:j], self.array_of_strings[i][j:]
        self.array_of_strings.insert(i, left)
        self.array_of_strings[i+1] = right
        self.update_metrics()
        self.notify(self.get_text())

    def index_from_pos(self, global_x, global_y):
        return int(global_y // self.height), int(global_x // self.width)

    def symbols_on_cursor(self, cursor: Cursor):
        i, j = cursor.position
        row = self.array_of_strings[i]

        left_char = row[j - 1] if j > 0 else None
        right_char = row[j] if j < len(row) else None
        return left_char, right_char
