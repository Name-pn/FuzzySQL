import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Тест колонок")
    columns = ["test1", 'test2']
    tree = ttk.Treeview(master=root, columns=columns)
    tree["displaycolumns"] = []
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=75, minwidth=50, stretch=True, anchor=tk.CENTER)  # можно настроить ширину
    tree.pack(fill=tk.BOTH, expand=True)
    root.mainloop()