import dataclasses

from libraries.Models.Cursor import Cursor
from libraries.Models.CursorManager import CursorManager
from libraries.Models.Text import Text


@dataclasses.dataclass
class TextController():
    text: Text
    cursors_manager: CursorManager

    def insert(self, char):
        cursors_lst = sorted(self.cursors_manager.set)
        last_i = -1
        shift = 0
        for cursor in cursors_lst:
            if cursor.position[0] != last_i:
                last_i = cursor.position[0]
                shift = 0
            else:
                shift += 1
            pos_i, pos_j = cursor.position
            pos_j += shift
            self.text.add_char((pos_i, pos_j), char)
        self.cursors_manager.move_right()

    def delete_right(self):
        self.cursors_manager.move_right()
        self.delete()

    def delete(self):
        cursors_lst = sorted(self.cursors_manager.set, reverse=True)
        num = 0
        for cursor in cursors_lst:
            if cursor.position[1] == 0 and cursor.position[0] != 0:
                num += 1
        shift = num
        indexes_arr = []
        for cursor in cursors_lst:
            pos_i, pos_j = cursor.position
            if pos_i == 0 and pos_j == 0:
                indexes_arr.append((0, 0))
            elif pos_j == 0:
                indexes_arr.append((pos_i - shift, self.text.row_len(pos_i-1)))
                shift -= 1
            else:
                indexes_arr.append((pos_i, pos_j - 1))
            pos_j -= 1
            self.text.delete_char((pos_i, pos_j))
        self.cursors_manager.clear_all()
        for index_i, index_j in indexes_arr:
            self.cursors_manager.add(Cursor((index_i, index_j)))


    def new_lines(self):
        cursors_lst = sorted(self.cursors_manager.set, reverse=True)
        shift = len(cursors_lst) - 1
        string_arr = []
        for cursor in cursors_lst:
            i, j = cursor.position
            self.text.add_newline(cursor.position)
            string_arr.append(i + 1 + shift)
            shift -= 1
        self.cursors_manager.clear_all()
        for index in string_arr:
            self.cursors_manager.add(Cursor((index, 0)))