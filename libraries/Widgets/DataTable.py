from tkinter import ttk
import tkinter as tk

class DataTable():
    def __init__(self, parent):
        self.parent = parent

        self.tree = ttk.Treeview(parent, show='headings', columns=('start'))
        self.tree.heading('start', text="Здесь будет вывод Select-а")
        self.tree.pack(fill=tk.X, expand=False)
        self.tree.column("#0", width=0, minwidth=0, stretch=True)

    def reset(self, columns, rows):
        self.tree.delete(*self.tree.get_children())

        self.tree["displaycolumns"] = []
        self.tree["columns"] = []

        if not columns or not rows:
            if not rows:
                self.tree["columns"] = ['start']
                self.tree["displaycolumns"] = ['start']
                self.tree.heading('start', text="Здесь будет вывод Select")
                self.tree.column('start', stretch=True)
            return

        self.tree["columns"] = columns
        width = self.tree.winfo_width() / len(columns)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=int(width), minwidth=50, stretch=True, anchor=tk.CENTER)  # можно настроить ширину

        self.tree["displaycolumns"] = columns

        for i, row in enumerate(rows):
            item_id = str(i)
            values = row
            item = self.tree.insert("", "end", iid=item_id, text=item_id, values=values)
            #if row[1] == "Папка":
            #    self.tree.item(item, image=self.folder_icon)
           # else:
           #     self.tree.item(item, image=self.file_icon)