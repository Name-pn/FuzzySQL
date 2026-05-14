from libraries.Patterns.Observer import Observer


class Observable():
    def __init__(self):
        self.observers: list[Observer] = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers = [el for el in self.observers if el != observer]

    def notify(self, payload):
        for el in self.observers:
            el.update(payload)