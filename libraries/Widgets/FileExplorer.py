import tkinter as tk
from tkinter import ttk
import os

from libraries.Models.IconExtractor import FolderIconExtractor


class FileExplorer():
    def __init__(self, parent, root_folder):
        self.parent = parent
        self.root_folder = root_folder
        self.extractor = FolderIconExtractor()
        self.folder_iso = self.extractor.get_folder_icon()
        self.open_folder_iso = self.extractor.get_open_folder_icon()

        # Создаем Treeview как атрибут класса (композиция)
        self.tree = ttk.Treeview(parent)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Настраиваем колонки
        self.tree["columns"] = ("type", "size")
        self.tree.column("#0", width=80)  # колонка с именем
        self.tree.column("type", width=40)
        self.tree.column("size", width=40)

        self.tree.heading("#0", text="Имя файла")
        self.tree.heading("type", text="Тип")
        self.tree.heading("size", text="Размер")

        # ПРИВЯЗЫВАЕМ СОБЫТИЯ (это ключ к функционалу!)
        self.tree.bind("<Double-1>", self.on_double_click)  # двойной клик
        self.tree.bind("<Return>", self.on_enter)  # нажатие Enter
        self.tree.bind("<<TreeviewOpen>>", self.on_folder_open)  # раскрытие папки

        # Загружаем корневую папку
        self.load_folder(root_folder)

    def on_double_click(self, event):
        """Обработка двойного клика по элементу"""
        item_id = self.tree.focus()  # получаем выбранный элемент
        if not item_id:
            return

        item_data = self.tree.item(item_id)
        item_text = item_data['text']
        item_tags = item_data.get('tags', [])

        # Проверяем, папка это или файл
        if 'directory' in item_tags:
            # Это папка - раскрываем/закрываем
            if self.tree.item(item_id, 'open'):
                self.tree.item(item_id, open=False, image=self.folder_iso)
            else:
                self.tree.item(item_id, open=True, image=self.open_folder_iso)
        else:
            # Это файл - открываем его
            self.open_file(self.get_full_path(item_id))

    def on_enter(self, event):
        """Обработка нажатия Enter"""
        self.on_double_click(event)  # просто вызываем ту же логику

    def on_folder_open(self, event):
        """Срабатывает при раскрытии папки"""
        item_id = self.tree.focus()
        if item_id:
            self.load_folder_contents(item_id)

    def load_folder(self, path, parent=''):
        """Загружает содержимое папки в дерево"""
        try:
            if parent == '':
                self.root_folder = path
                self.tree.delete(*self.tree.get_children())
            for item in sorted(os.listdir(path)):
                if item.startswith("."):
                    continue

                full_path = os.path.join(path, item)
                is_dir = os.path.isdir(full_path)

                # Определяем тип и размер
                if is_dir:
                    item_type = "Папка"
                    item_size = ""
                    tags = ('directory',)
                else:
                    item_type = self.get_file_extension(item)
                    item_size = f"{os.path.getsize(full_path)} B"
                    tags = ('file',)

                # Вставляем элемент
                node_id = self.tree.insert(
                    parent, 'end',
                    text=item,
                    values=(item_type, item_size),
                    tags=tags,
                    open=False
                )

                # Добавляем "заглушку" для папок (чтобы был плюсик)
                if is_dir:
                    self.tree.item(node_id, image=self.folder_iso)
                    self.tree.insert(node_id, 'end', text="загрузка...")
            if len(os.listdir(path)) == 0:
                node_id = self.tree.insert(
                    parent, 'end',
                    text="Пусто",
                    values=('-', '-'),
                    tags="",
                    open=False
                )

        except PermissionError:
            pass  # Пропускаем папки без доступа

    def load_folder_contents(self, item_id):
        """Загружает содержимое папки при раскрытии"""
        # Удаляем все дочерние элементы
        for child in self.tree.get_children(item_id):
            self.tree.delete(child)

        # Загружаем реальное содержимое
        full_path = self.get_full_path(item_id)
        self.load_folder(full_path, item_id)

    def get_full_path(self, item_id):
        """Рекурсивно собирает полный путь из дерева"""
        path_parts = []
        current = item_id

        while current:
            path_parts.insert(0, self.tree.item(current, 'text'))
            current = self.tree.parent(current)

        return self.root_folder + '\\' + '\\'.join(path_parts)

    def get_file_extension(self, filename):
        """Возвращает расширение файла"""
        if '.' in filename:
            return filename.split('.')[-1].upper()
        return "Файл"

    def open_file(self, path):
        """Открывает файл для редактирования"""
        self.last_filename = path
        self.parent.event_generate("<<FileOpened>>", when="tail")
