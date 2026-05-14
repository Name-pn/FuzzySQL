from dataclasses import dataclass

@dataclass()
class Cursor():
    position: tuple[int, int]
    visible: bool = True

    def __eq__(self, other: "Cursor"):
        return self.position[0] == other.position[0] and self.position[1] == other.position[1]

    def __lt__(self, other: "Cursor"):
        i1, j1 = self.position
        i2, j2 = other.position
        if i1 != i2:
            return i1 < i2
        return j1 < j2

    def __le__(self, other: 'Cursor'):
        return self < other or self == other

    def __ge__(self, other: 'Cursor'):
        return not self < other

    def __gt__(self, other: 'Cursor'):
        return not self < other and not self == other

    def __hash__(self):
        return hash(self.position)

    def blink(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

