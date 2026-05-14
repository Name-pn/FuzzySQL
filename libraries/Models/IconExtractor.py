import icoextract
import tkinter as tk
from PIL import Image, ImageTk
import io

class FolderIconExtractor:
    def __init__(self):
        # Путь к системному файлу с иконками папок
        # Для Windows 10/11 иконки папок находятся в imageres.dll [citation:4]
        self.icon_path = r"C:\Windows\SystemResources\imageres.dll.mun"

        # Извлекаем иконку папки (индекс 4 обычно соответствует папке)
        self.extractor = icoextract.IconExtractor(self.icon_path)

    def get_folder_icon(self):
        icon = self.extractor.get_icon(4)
        image = Image.open(icon)
        image = image.resize((16, 16), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        return photo

    def get_open_folder_icon(self):
        icon = self.extractor.get_icon(2)
        image = Image.open(icon)
        image = image.resize((16, 16), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        return photo