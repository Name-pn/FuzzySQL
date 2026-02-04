import re

import psycopg2
import skia
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from threading import Timer

from libraries.Environment import Environment
from libraries.Extension import ExtensionCursor
from libraries.FunctionHub import FunctionHub

class Cursor():
    def __init__(self, pos_x, pos_y, width, height, fAscent = 0, pos0 = None):
        self.pos0 = pos0
        if self.pos0 is None:
            self.pos0 = (0, 0)
        self.x = pos_x + self.pos0[0]
        self.y = pos_y - fAscent + self.pos0[1]
        self.width = width
        self.height = height
        self.fAscent = fAscent
        self.i = int((self.y + fAscent - self.pos0[1]) // height)
        self.j = int((self.x - self.pos0[0]) // width)
        self.visible = True

    def blink(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def validate(self, text):
        if self.i < 0:
            self.i = 0
            self.y = -self.fAscent
        if self.j < 0:
            self.j = 0
            self.x = 0
        if self.i >= len(text):
            self.i = len(text) - 1
            self.y = self.height*self.i-self.fAscent
        if self.j > len(text[self.i]):
            self.j = len(text[self.i])
            self.x = self.width*self.j

    def indexes(self):
        return (self.i, self.j)

    def coords(self):
        return (self.x, self.y)

    def move_left(self, text):
        if self.j > 0:
            self.j = self.j - 1
            self.x = self.x - self.width
        else:
            if self.i > 0:
                self.i = self.i - 1
                self.y = self.y - self.height
                if self.i >= 0:
                    self.j = len(text[self.i])
                    self.x = self.j * self.width


    def move_right(self, text):
        if len(text[self.i]) == self.j:
            if len(text) > self.i + 1:
                self.i = self.i + 1
                self.y = self.y + self.height
                self.x = 0
                self.j = 0
        else:
            self.j = self.j + 1
            self.x = self.x + self.width

    def move_up(self, text):
        if self.i > 0:
            self.i = self.i - 1
            self.y = self.y - self.height
            if self.j > len(text[self.i]):
                self.j = len(text[self.i])
                self.x = self.j * self.width
        else:
            self.j = 0
            self.x = 0

    def move_down(self, text):
        if self.i+1 < len(text):
            self.i = self.i + 1
            self.y = self.y + self.height
            if self.j > len(text[self.i]):
                self.j = len(text[self.i])
                self.x = self.j * self.width
        else:
            self.j = len(text[self.i])
            self.x = len(text[self.i]) * self.width

    @classmethod
    def cursor_from_click(self, x, y, width, height, fAscent, start_pos = None):
        if start_pos is None:
            j, i = int(x // width), int(y // height)
            return Cursor(j*width, i*height, width, height, fAscent)
        else:
            j, i = int((x - start_pos[0]) // width), int((y - start_pos[1]) // height)
            return Cursor(j * width, i * height, width, height, fAscent, pos0 = start_pos) #, pos0=start_pos

class Observer():
    def update(self, payload):
        raise NotImplementedError()

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


class Observable():
    observers: list[Observer] = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers = [el for el in self.observers if el != observer]

    def notify(self, payload):
        for el in self.observers:
            el.update(payload)

def create_circle_icon(color, diameter=20):
    """Создает круглую иконку заданного цвета"""
    image = Image.new('RGBA', (diameter, diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Рисуем круг
    draw.ellipse((0, 0, diameter - 1, diameter - 1), fill=color, outline="black")

    # Конвертируем в PhotoImage для Tkinter
    return ImageTk.PhotoImage(image)

class SkiaTextEditor(tk.Label, Observable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=50, height=50)
        self.text = [""]
        self.surface = skia.Surface(256, 256)
        self.canvas = self.surface.getCanvas()
        fontname = 'Consolas'
        try:
            typeface = skia.Typeface(fontname)
            self.font = skia.Font(typeface, 16)
        except:
            print(f"Шрифт {fontname} не найден в системе\n")
        self.font_metrics = self.font.getMetrics()

        self.letter_width = self.font.measureText("A")
        self.letter_height = abs(self.font_metrics.fAscent - self.font_metrics.fDescent)
        self.cursors = [Cursor(0, 0, self.letter_width, self.letter_height, self.font_metrics.fAscent)]
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<Button-1>", self.on_left_click)
        self.bind("<FocusOut>", self.focus_out)
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<Configure>", self.on_resize)
        self.blink_time = 500
        self.run_blinking = False
        self.blink_ids = []
        self.stroke_width = 3
        self._gen_set_image()

        self.xview_pos = 0.0
        self.yview_pos = 0.0

    def max_letters_in_string(self):
        res = 0.001
        for string in self.text:
            if len(string) > res:
                res = len(string)
        return res

    def max_letters_in_column(self):
        return len(self.text)

    def xview(self, *args):
        max_scroll = 1 - self.visible_letters_width / self.max_letters_in_string()
        self.xview_pos = max(min(max_scroll, self.xview_pos), 0)
        if not args:
            return (self.xview_pos,
                    self.xview_pos +
                    min(1.0, self.visible_letters_width / self.max_letters_in_string()))
        command = args[0]
        if command == "moveto":
            self.xview_pos = float(args[1])
        elif command == "scroll":
            number = int(args[1])
            what = args[2]
            delta = 0
            if what == "units":
                delta = number / self.max_letters_in_string()
            elif what == "pages":
                delta = number * self.visible_letters_width / self.max_letters_in_string()
            self.xview_pos = min(max_scroll, max(self.xview_pos + delta, 0))
        self.cursors = []
        self.full_update_with_scrolls()


    def yview(self, *args):
        max_scroll = 1 - self.visible_letters_height / self.max_letters_in_column()
        self.yview_pos = max(0, min(max_scroll, self.yview_pos))
        if not args:
            return (self.yview_pos,
                    self.yview_pos +
                    min(1.0, self.visible_letters_height / self.max_letters_in_column()))
        command = args[0]
        if command == "moveto":
            self.yview_pos = float(args[1])
        elif command == "scroll":
            number = int(args[1])
            what = args[2]
            delta = 0
            if what == "units":
                delta = number / self.max_letters_in_column()
            elif what == "pages":
                delta = number * self.visible_letters_height / self.max_letters_in_column()
            self.yview_pos = min(max_scroll, max(self.yview_pos + delta, 0))
        self.cursors = []
        self.full_update_with_scrolls()


    def xscroll_command(self, command):
        if command:
            pos = self.xview()
            command(*pos)

    def yscroll_command(self, command):
        if command:
            pos = self.yview()
            command(*pos)

    def configure(self, yscrollcommand=None, xscrollcommand=None, *args, **kwargs):
        super().configure(*args, **kwargs)
        self.xscroll = xscrollcommand
        self.yscroll = yscrollcommand

    def on_resize(self, event):
        width_pixels = event.width-PADX*2
        height_pixels = event.height-PADY*2
        self.surface = skia.Surface(width_pixels, height_pixels)
        self.visible_letters_width = width_pixels / self.letter_width
        self.visible_letters_height = height_pixels / self.letter_height
        self.canvas = self.surface.getCanvas()
        self.update_scrolls()
        self.full_update_with_scrolls()

    def _draw_text(self, text = None, pos = None):
        if text is None:
            x, y = 0, -self.font_metrics.fAscent
            paint = skia.Paint(AntiAlias=True, Color=skia.ColorBLACK)
            for str in self.text:
                for char in str:
                    self.canvas.drawString(char, x, y, self.font, paint)
                    x += self.letter_width
                x = 0
                y += self.letter_height
        else:
            if pos is None:
                raise Exception("Стартовая позиция не передана")
            x0, y0 = pos[0], pos[1] - self.font_metrics.fAscent
            paint = skia.Paint(AntiAlias=True, Color=skia.ColorBLACK)
            for str in text:
                for char in str:
                    self.canvas.drawString(char, x0, y0, self.font, paint)
                    x0 += self.letter_width
                x0 = pos[0]
                y0 += self.letter_height

    def _draw_cursors(self):
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorBLUE, StrokeWidth=self.stroke_width, Style=skia.Paint.kStroke_Style)
        path = skia.Path()
        for cursor in self.cursors:
            if cursor.visible:
                path.moveTo(cursor.x, cursor.y + self.font_metrics.fAscent)
                path.lineTo(cursor.x, cursor.y + self.font_metrics.fDescent)
                self.canvas.drawPath(path, paint)

    def _draw_full_skia_image(self, size:tuple[int, int] = (256, 256)):
        self.canvas.clear(skia.ColorWHITE)
        self._draw_text()
        if self.run_blinking:
            self._draw_cursors()
        return self.surface.makeImageSnapshot()

    def _draw_skia_image_from_text_and_pos(self, text, pos):
        self.canvas.clear(skia.ColorWHITE)
        self._draw_text(text, pos)
        if self.run_blinking:
            self._draw_cursors()
        return self.surface.makeImageSnapshot()

    def _gen_set_image(self):
        skia_image = self._draw_full_skia_image()
        pil_image = Image.fromarray(skia_image.convert(colorType=skia.kRGBA_8888_ColorType,
                                                       alphaType=skia.kUnpremul_AlphaType))
        photo = ImageTk.PhotoImage(pil_image)
        self.config(image=photo)
        self.image = photo

    def _gen_set_viewport(self, text, x0, y0):
        skia_image = self._draw_skia_image_from_text_and_pos(text, (x0, y0))
        pil_image = Image.fromarray(skia_image.convert(colorType=skia.kRGBA_8888_ColorType,
                                                       alphaType=skia.kUnpremul_AlphaType))
        photo = ImageTk.PhotoImage(pil_image)
        self.config(image=photo)
        self.image = photo

    def update_image(self):
        skia_image = self.surface.makeImageSnapshot()
        pil_image = Image.fromarray(skia_image.convert(colorType=skia.kRGBA_8888_ColorType,
                                                       alphaType=skia.kUnpremul_AlphaType))
        photo = ImageTk.PhotoImage(pil_image)
        self.config(image=photo)
        self.image = photo


    def on_left_click(self, event):
        self.focus_set()
        x = event.x - PADX
        y = event.y - PADY
        letters, pixels = self.offsets()
        text = self.viewport_text(letters)
        cursor = Cursor.cursor_from_click(x, y, self.letter_width, self.letter_height, self.font_metrics.fAscent, start_pos=(pixels))
        cursor.validate(text)
        self.cursors = [cursor]

        self.full_update_with_scrolls(letters, pixels)
        #self.full_update()

    def blink(self):
        self.blink_ids = []
        for cursor in self.cursors:
            cursor.blink()
        if self.run_blinking:
            self.blink_ids = [self.after(self.blink_time, self.blink)]
        self.cursors_update()

    def focus_in(self, event):
        self.focus_set()
        self.run_blinking = True
        self.after(self.blink_time, self.blink)
        self.full_update_with_scrolls()

    def focus_out(self, event):
        self.run_blinking = False
        for id in self.blink_ids:
            self.after_cancel(id)
        self.blink_ids = []
        self.full_update_with_scrolls()

    def on_key_press(self, event):
        if event.char == '\r':
            for i_cursor, cursor in enumerate(self.cursors):
                i, j = cursor.indexes()
                left, right = self.text[i][:j], self.text[i][j:]
                self.text.insert(i+1, right)
                self.text[i] = left
                cursor.move_right(self.text)
                #self.cursors[i_cursor] = Cursor(0, cursor.y + self.letter_height + cursor.fAscent, cursor.width, cursor.height, cursor.fAscent)
            self.notify(self.get_text())
        elif event.char == '\b':
            for i_cursor, cursor in enumerate(self.cursors):
                i, j = cursor.indexes()
                if j != 0:
                    self.text[i] = self.text[i][:j-1] + self.text[i][j:]
                    cursor.move_left(self.text)
                else:
                    if i > 0:
                        n = len(self.text[i])
                        self.text[i-1] = self.text[i-1] + self.text[i]
                        del self.text[i]
                        for i in range(n + 1):
                            cursor.move_left(self.text)

                # if cursor.x >= self.letter_width:
                #     self.cursors[i_cursor] = Cursor(cursor.x - self.letter_width, cursor.y + cursor.fAscent, cursor.width, cursor.height, cursor.fAscent)
                # else:
                #     self.cursors[i_cursor] = Cursor(cursor.x + self.letter_width * len(self.text[i]), cursor.y - self.letter_height + cursor.fAscent, cursor.width, cursor.height, cursor.fAscent)
            self.notify(self.get_text())
        elif event.char.isprintable() and event.char != "":
            for i_cursor, cursor in enumerate(self.cursors):
                i, j = cursor.indexes()
                self.text[i] = self.text[i][:j] + event.char + self.text[i][j:]
                cursor.move_right(self.text)
                #self.cursors[i_cursor] = Cursor(cursor.x + self.letter_width, cursor.y+ cursor.fAscent, cursor.width, cursor.height, cursor.fAscent)
            self.notify(self.get_text())
        elif event.keysym == "Right":
            for i_cursor, cursor in enumerate(self.cursors):
                cursor.move_right(self.text)
        elif event.keysym == "Left":
            for i_cursor, cursor in enumerate(self.cursors):
                cursor.move_left(self.text)
        elif event.keysym == "Up":
            for i_cursor, cursor in enumerate(self.cursors):
                cursor.move_up(self.text)
        elif event.keysym == "Down":
            for i_cursor, cursor in enumerate(self.cursors):
                cursor.move_down(self.text)

        self.full_update_with_scrolls()

    # def full_update(self, text: list[str]=None):
    #     if not text is None:
    #         self.text = text
    #     self._gen_set_image()
    #     self.update_scrolls()

    def offsets(self):
        x_offset_letters = self.xview_pos * self.max_letters_in_string()
        x0_pixels = -(x_offset_letters % 1) * self.letter_width
        y_offset_letters = self.yview_pos * self.max_letters_in_column()
        y0_pixels = -(y_offset_letters % 1) * self.letter_height
        return (x_offset_letters, y_offset_letters), (x0_pixels, y0_pixels)

    def _get_indexes_of_viewport(self, letter_offsets):
        x_offset_letters = letter_offsets[0]
        j0 = int(x_offset_letters)
        j1 = int(x_offset_letters + self.visible_letters_width)
        y_offset_letters = letter_offsets[1]
        i0 = int(y_offset_letters)
        i1 = int(y_offset_letters + self.visible_letters_height)
        return ((i0, i1), (j0, j1))

    def viewport_text(self, offsets_letters = None):
        if offsets_letters is None:
            offsets_letters, offsets_pixels = self.offsets()
        (i0, i1), (j0, j1) = self._get_indexes_of_viewport(offsets_letters)
        return [string[j0:j1+1] for string in self.text[i0:i1+1]]


    def full_update_with_scrolls(self, offsets_letters = None, offsets_pixels = None):
        if not offsets_letters and not offsets_pixels:
            offsets_letters, offsets_pixels = self.offsets()
        x0_pixels = offsets_pixels[0]
        y0_pixels = offsets_pixels[1]
        viewport_text = self.viewport_text(offsets_letters)
        self._gen_set_viewport(viewport_text, x0_pixels, y0_pixels)
        self.update_scrolls()


    def update_scrolls(self):
        self.xscroll_command(self.xscroll)
        self.yscroll_command(self.yscroll)

    def cursors_update(self):
        paint_background = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for cursor in self.cursors:
            i, j = cursor.indexes()
            x, y = cursor.coords()
            text = self.viewport_text()
            rect = skia.Rect(l=x - self.letter_width, t=y + self.font_metrics.fAscent, r=x + self.letter_width, b=y + self.font_metrics.fDescent)
            self.canvas.drawRect(rect, paint_background)
            paint = skia.Paint(AntiAlias=True, Color=skia.ColorBLACK)
            if len(text[i]) > j:
                char = text[i][j]
                self.canvas.drawString(char, x, y, self.font, paint)
            if j - 1 >= 0:
                char = text[i][j-1]
                self.canvas.drawString(char, x-self.letter_width, y, self.font, paint)

        self._draw_cursors()
        self.update_image()


    def get_text(self):
        result = ""
        for str in self.text:
            result += str + "\n"
        return result

class TextEditor(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent, *args, **kwargs)
        self.skia = SkiaTextEditor(master=self)
        self.horizontal_scrollbar = tk.Scrollbar(master=self, orient=tk.HORIZONTAL, command=self.skia.xview)
        self.vertical_scrollbar = tk.Scrollbar(master=self, orient=tk.VERTICAL, command=self.skia.yview)
        self.skia.configure(yscrollcommand=self.vertical_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.skia.grid(column=0, row=0, columnspan=1, rowspan=1, padx=PADX, pady=PADY,sticky="nsew")
        self.horizontal_scrollbar.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="ew")
        self.vertical_scrollbar.grid(column=1, row=0, columnspan=1, rowspan=1, sticky="sn")

class App():
    filepath = None

    def __init__(self, root):
        self.root = root
        self.file_chooser_btn = tk.Button(self.root, text="Выбрать файл", command=self.choose_file)
        self.file_chooser_btn.pack(pady=10)

        self.update_btn = tk.Button(self.root, text="Запустить скрипт", command=self.run)
        self.update_btn.pack(pady=10)

        self.gray_icon = create_circle_icon("gray")
        self.green_icon = create_circle_icon("green")
        self.red_icon = create_circle_icon("red")
        self.white_icon = create_circle_icon("white")

        self.status_label = tk.Label(self.root, text="Нет соединения с БД", compound="left", image=self.white_icon)
        self.status_label.pack(pady=10)

        try:
            self.connect()
            self.status_label.config(image=self.gray_icon, text="Соединено с БД")
        except Exception as e:
            print(e.__str__())

        self.label = TextEditor(parent=self.root, borderwidth=3, relief=tk.SOLID)
        self.label.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<FocusOut>", self._focus_out)
        self.root.bind("<FocusIn>", self._focus_in)
        self.window_is_active = True
        self.saver = Saver(filename=self.filepath, text=self.label.skia.get_text())
        self.label.skia.subscribe(self.saver)

    def connect(self):
        self.table = Environment()
        self.table.load("./parser_data/conf.pkl")
        conn = psycopg2.connect(host="localhost", port=5433,
                                dbname="postgres", user="postgres",
                                password="1111", connect_timeout=10, sslmode="prefer")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.common_cursor = conn.cursor()
        conn.cursor_factory = ExtensionCursor
        self.db_cursor: ExtensionCursor = conn.cursor()
        self.fh = FunctionHub(self.common_cursor, self.table)
        self.db_cursor.set_fh(self.fh)
        self.db_cursor.set_table(self.table)

    def run(self):
        try:
            self.db_cursor.execute(self.label.skia.get_text())
            self.status_label.config(image=self.green_icon, text="Запрос исполнен")
        except Exception as e:
            self.status_label.config(image=self.red_icon, text="Ошибка выполнения запроса")
            print(e.__str__())

    def choose_file(self):
        self.filepath = filedialog.askopenfilename(title="Выберите файл с SQL запросом", filetypes=
        [("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if self.filepath != "":
            with open(self.filepath, "r", encoding="utf-8") as file:
                query = file.read()
            text = re.split("\n", query)
            self.label.skia.text = text
            self.label.skia.full_update_with_scrolls()
            self.label.skia.unsubscribe(self.saver)
            self.saver = Saver(self.filepath, text)
            self.label.skia.subscribe(self.saver)

    def _focus_out(self, event):
        foc = self.root.focus_get()
        if foc is None:
            self.label.skia.focus_out(event)


    def _focus_in(self, event):
        pass


if __name__ == "__main__":
    PADX, PADY = 10, 10
    root = tk.Tk()
    root.title("Skia в Tkinter")
    app = App(root)
    root.mainloop()