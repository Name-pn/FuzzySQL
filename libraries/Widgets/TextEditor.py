import tkinter as tk
from libraries.Widgets.SkiaText import SkiaText

PADX, PADY = 10, 10
class TextEditor(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent, *args, **kwargs)
        self.skia = SkiaText(master=self, padx=PADX, pady=PADY)
        self.horizontal_scrollbar = tk.Scrollbar(master=self, orient=tk.HORIZONTAL, command=self.skia.xview)
        self.vertical_scrollbar = tk.Scrollbar(master=self, orient=tk.VERTICAL, command=self.skia.yview)
        self.skia.configure(yscrollcommand=self.vertical_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.skia.grid(column=0, row=0, columnspan=1, rowspan=1, padx=PADX, pady=PADY,sticky="nsew")
        self.horizontal_scrollbar.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="ew")
        self.vertical_scrollbar.grid(column=1, row=0, columnspan=1, rowspan=1, sticky="sn")