from threading import Timer

from libraries.Patterns.Observer import Observer


class Saver(Observer):
    def __init__(self, filename, text, time=3):
        if filename:
            self.filename = filename
        else:
            self.filename = "./tmp.txt"
        self.old_text = text
        self.save_timer = None
        self.time = time

    def update(self, payload):
        self._shedule_save(payload)

    def _shedule_save(self, payload):
        if self.save_timer:
            self.save_timer.cancel()
        if self.old_text != payload:
            self.old_text = payload
            self.save_timer = Timer(self.time, self._save)
            self.save_timer.start()

    def _save(self):
        self.save_timer = None
        with open(self.filename, 'w', encoding="utf-8") as file:
            file.write(self.old_text)