from libraries.Models.Cursor import Cursor
from libraries.Patterns.Observer import Observer


class CursorManager(Observer):
    def __init__(self, text):
        super().__init__()
        self.set = set()
        self.text = text

    def reset(self, new_cursors):
        self.set = new_cursors

    def validate(self):
        new_set = set()
        for cursor in self.set:
            i, j = cursor.position
            if i >= self.text.max_column_len:
                i = self.text.max_column_len - 1
            if j > len(self.text.array_of_strings[i]):
                j = len(self.text.array_of_strings[i])
            new_set.add(Cursor(position=(i, j), visible=cursor.visible))
        self.set = new_set


    def get_visible_cursors(self, range):
        self.validate()
        new_set = set()
        (i1, i2), (j1, j2) = range
        for cursor in self.set:
            if i1 <= cursor.position[0] and i2 + 1 > cursor.position[0] \
                and j1 <= cursor.position[1] and j2 + 1 > cursor.position[1]:
                new_set.add(cursor)
        return new_set

    def add(self, cursor:Cursor):
        if len(self.set) > 0:
            old = next(iter(self.set))
            cursor.visible = old.visible
        self.set.add(cursor)

    def remove(self, cursor:Cursor):
        self.set.remove(cursor)

    def clear_all(self):
        self.set = set()

    def move_left(self):
        for cursor in self.set:
            self._move_left(cursor)

    def move_right(self):
        for cursor in self.set:
            self._move_right(cursor)

    def move_up(self):
        for cursor in self.set:
            self._move_up(cursor)

    def move_down(self):
        for cursor in self.set:
            self._move_down(cursor)

    def _move_left(self, cursor):
        i, j = cursor.position
        if j > 0:
            j = j - 1
        elif i > 0:
            i = i - 1
            j = self.text.row_len(i)
        cursor.position = (i, j)

    def _move_right(self, cursor):
        i, j = cursor.position
        if j < self.text.row_len(i):
            j += 1
        elif i + 1 < self.text.max_column_len:
            i = i + 1
            j = 0
        cursor.position = (i, j)

    def _move_up(self, cursor):
        i, j = cursor.position
        if i > 0:
            i = i - 1
            if j > self.text.row_len(i):
                j = self.text.row_len(i)
        else:
            j = 0
        cursor.position = (i, j)

    def _move_down(self, cursor):
        i, j = cursor.position
        if i+1 < self.text.max_column_len:
            i = i + 1
            if j > self.text.row_len(i):
                j = self.text.row_len(i)
        else:
            j = self.text.row_len(i)
        cursor.position = (i, j)