from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from tkinter import filedialog
import tkinter as tk
import re
import os

from libraries.Environment import Environment
from libraries.Extension import ExtensionCursor
from libraries.FunctionHub import FunctionHub
from libraries.Patterns.Saver import Saver
from libraries.Widgets.DataTable import DataTable
from PIL import Image, ImageTk, ImageDraw

from libraries.Widgets.FileExplorer import FileExplorer
from libraries.Widgets.TextEditor import TextEditor


def create_circle_icon(color, diameter=20):
    """Создает круглую иконку заданного цвета"""
    image = Image.new('RGBA', (diameter, diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Рисуем круг
    draw.ellipse((0, 0, diameter - 1, diameter - 1), fill=color, outline="black")

    # Конвертируем в PhotoImage для Tkinter
    return ImageTk.PhotoImage(image)

class App():
    filepath = None
    root_folder = None

    def __init__(self, root):
        self.root = root
        self.root_folder = os.getcwd()

        self.gray_icon = create_circle_icon("gray")
        self.green_icon = create_circle_icon("green")
        self.red_icon = create_circle_icon("red")
        self.white_icon = create_circle_icon("white")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, expand=False, fill=tk.X)
        self.status_label = tk.Label(self.top_frame, text="Нет соединения с БД", compound="left", image=self.white_icon)
        self.status_label.pack(pady=10, side=tk.LEFT)

        self.data_table_frame = tk.Frame(self.top_frame, width=250, relief=tk.SOLID, borderwidth=1)
        self.data_table_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.data_table = DataTable(self.data_table_frame)

        try:
            self.connect()
            self.status_label.config(image=self.gray_icon, text="Соединено с БД")
        except Exception as e:
            print(e.__str__())

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.label = TextEditor(parent=self.bottom_frame, borderwidth=1, relief=tk.SOLID)
        self.label.skia.set_env(self.table)

        # Создаем фрейм для FileExplorer (левый)
        self.explorer_frame = tk.Frame(self.bottom_frame, width=250, relief=tk.SOLID, borderwidth=1)
        self.explorer_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)  # слева, заполняет по вертикали
        self.explorer_frame.pack_propagate(False)  # фиксируем ширину

        # Создаем FileExplorer внутри левого фрейма
        self.explorer = FileExplorer(self.explorer_frame, self.root_folder)
        self.label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor='e')

        self.explorer_frame.bind("<<FileOpened>>", self.open_file)
        self.root.bind("<FocusOut>", self._focus_out)
        self.root.bind("<FocusIn>", self._focus_in)
        self.window_is_active = True
        self.saver = Saver(filename=self.filepath, text=self.label.skia.get_text())
        self.label.skia.text.subscribe(self.saver)

    def open_file(self, event):
        self._choose_file_body(self.explorer.last_filename)

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
            if self.db_cursor.description:
                columns = [desc[0] for desc in self.db_cursor.description]
                rows = self.db_cursor.fetchall()
                self.data_table.reset(columns, rows)
            self.status_label.config(image=self.green_icon, text="Запрос исполнен")
        except Exception as e:
            self.status_label.config(image=self.red_icon, text="Ошибка выполнения запроса")
            print(e.__str__())

    def _choose_file_body(self, filepath):
        if filepath != '':
            with open(filepath, "r", encoding="utf-8") as file:
                query = file.read()
            text = re.split("\n", query)
            self.label.skia.text.unsubscribe(self.saver)
            self.label.skia.text.change_text(text)
            self.label.skia.full_update_with_scrolls()
            self.saver = Saver(filepath, text)
            self.label.skia.text.subscribe(self.saver)

    def choose_folder(self):
        self.root_folder = filedialog.askdirectory(title="Выберите корневую папку")
        if self.root_folder != "":
            self.explorer.load_folder(self.root_folder)

    def _focus_out(self, event):
        foc = self.root.focus_get()
        if foc is None:
            self.label.skia.focus_out(event)


    def _focus_in(self, event):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("FSQL-интерфейс")
    menubar = tk.Menu(root)
    root['menu'] = menubar
    app = App(root)
    menubar.add("command", label="Выбрать директорию", command=app.choose_folder)
    menubar.add("command", label="Исполнить", command=app.run)
    root.mainloop()