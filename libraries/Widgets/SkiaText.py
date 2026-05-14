import tkinter as tk

from libraries.Controllers.SyntaxHighlighter import SyntaxHighlighter, SyntaxTheme
from libraries.Controllers.TextController import TextController
from libraries.Lexer import SQLLexer
from libraries.Models.Text import Text
from libraries.Models.Cursor import Cursor
from libraries.Models.CursorManager import CursorManager
from PIL import Image, ImageTk

import skia

def get_color(token):
    if token:
        theme = SyntaxTheme.get_style(token.ttype)
        if theme:
            return skia.Color(*theme.color)
    return skia.ColorBLACK

class SkiaText(tk.Label):
    def __init__(self, *args, padx, pady, **kwargs):
        super().__init__(*args, **kwargs)
        self.padx = padx
        self.pady = pady
        self.config(width=50, height=50)

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
        self.text = Text(array=[""], width=self.letter_width, height=self.letter_height)
        self.cursor_manager = CursorManager(self.text)
        self.cursor_manager.add(Cursor((0, 0)))
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<Button-1>", self.on_left_click)
        self.bind("<FocusOut>", self.focus_out)
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<Configure>", self.on_resize)
        self.blink_time = 500
        self.run_blinking = False
        self.blink_ids = []
        self.stroke_width = 3
        self.xview_pos = 0.0
        self.yview_pos = 0.0
        self.controller = TextController(text=self.text, cursors_manager=self.cursor_manager)
        self.lexer = SQLLexer()
        self.syntax_highlighter = SyntaxHighlighter(self.lexer)
        self.text.subscribe(self.syntax_highlighter)
        self.visible_letters_width = 0
        self.visible_letters_height = 0
        self._gen_set_viewport(self.text.array_of_strings, 0, 0)

    def set_env(self, env):
        self.env = env
        self.text.unsubscribe(self.syntax_highlighter)
        self.lexer = SQLLexer(env)
        self.syntax_highlighter = SyntaxHighlighter(self.lexer)
        self.text.subscribe(self.syntax_highlighter)
        self.visible_letters_width = 0
        self.visible_letters_height = 0
        self._gen_set_viewport(self.text.array_of_strings, 0, 0)

    def xview(self, *args):
        if self.text.max_row_len == 0:
            return (0, 1)
        max_scroll = 1 - self.visible_letters_width / self.text.max_row_len
        self.xview_pos = max(min(max_scroll, self.xview_pos), 0)
        if not args:
            return (self.xview_pos,
                    self.xview_pos +
                    min(1.0, self.visible_letters_width / self.text.max_row_len))
        command = args[0]
        if command == "moveto":
            self.xview_pos = float(args[1])
        elif command == "scroll":
            number = int(args[1])
            what = args[2]
            delta = 0
            if what == "units":
                delta = number / self.text.max_row_len
            elif what == "pages":
                delta = number * self.visible_letters_width / self.text.max_row_len
            self.xview_pos = min(max_scroll, max(self.xview_pos + delta, 0))
        self.full_update_with_scrolls()


    def yview(self, *args):
        if self.text.max_column_len == 0:
            return (0, 1)
        max_scroll = 1 - self.visible_letters_height / self.text.max_column_len
        self.yview_pos = max(0, min(max_scroll, self.yview_pos))
        if not args:
            return (self.yview_pos,
                    self.yview_pos +
                    min(1.0, self.visible_letters_height / self.text.max_column_len))
        command = args[0]
        if command == "moveto":
            self.yview_pos = float(args[1])
        elif command == "scroll":
            number = int(args[1])
            what = args[2]
            delta = 0
            if what == "units":
                delta = number / self.text.max_column_len
            elif what == "pages":
                delta = number * self.visible_letters_height / self.text.max_column_len
            self.yview_pos = min(max_scroll, max(self.yview_pos + delta, 0))
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
        width_pixels = event.width-self.padx*2
        height_pixels = event.height-self.pady*2
        self.surface = skia.Surface(width_pixels, height_pixels)
        self.visible_letters_width = width_pixels / self.letter_width
        self.visible_letters_height = height_pixels / self.letter_height
        self.canvas = self.surface.getCanvas()
        self.update_scrolls()
        self.full_update_with_scrolls()

    def _draw_text(self, text, pos = None):
        if pos is None:
            raise Exception("Стартовая позиция не передана")
        x0, y0 = pos[0], pos[1] - self.font_metrics.fAscent
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorBLACK)
        (i0, i1), (j0, j1) = self._get_indexes_of_viewport()
        for index_i, string in enumerate(text):
            for index_j, char in enumerate(string):
                token = self.syntax_highlighter.get_token_at_position(index_i + i0, index_j + j0)
                color = get_color(token)
                paint.setColor(color)
                self.canvas.drawString(char, x0, y0, self.font, paint)
                x0 += self.letter_width
            x0 = pos[0]
            y0 += self.letter_height

    def _draw_cursors(self):
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorBLUE, StrokeWidth=self.stroke_width, Style=skia.Paint.kStroke_Style)
        path = skia.Path()
        range = self._get_indexes_of_viewport()
        visible_cursors = self.cursor_manager.get_visible_cursors(range)
        for cursor in visible_cursors:
            if cursor.visible:
                i, j = cursor.position
                iy_px, jx_px = self.letter_height*i, self.letter_width*j
                x_shift_px = self.xview_pos * self.text.max_row_len * self.letter_width
                y_shift_px = self.yview_pos * self.text.max_column_len * self.letter_height
                jx_px = jx_px - x_shift_px
                iy_px = iy_px - y_shift_px
                path.moveTo(jx_px, iy_px)
                path.lineTo(jx_px, iy_px + self.font_metrics.fDescent - self.font_metrics.fAscent)
                self.canvas.drawPath(path, paint)

    def _draw_skia_image_from_text_and_pos(self, text, pos):
        self.canvas.clear(skia.ColorWHITE)
        self._draw_text(text, pos)
        if self.run_blinking:
            self._draw_cursors()
        return self.surface.makeImageSnapshot()

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
        local_x = event.x - self.padx
        local_y = event.y - self.pady
        global_x = local_x + self.xview_pos * self.text.max_row_len * self.letter_width
        global_y = local_y + self.yview_pos * self.text.max_column_len * self.letter_height
        if event.state & 4:
            new_cursor = Cursor(position=self.text.index_from_pos(global_x, global_y))
            self.cursor_manager.add(new_cursor)
        else:
            self.cursor_manager.clear_all()
            cursor = Cursor(position=self.text.index_from_pos(global_x, global_y))
            self.cursor_manager.add(cursor)
        self.full_update_with_scrolls()


    def blink_show(self):
        self.blink_ids = []
        for cursor in self.cursor_manager.set:
            cursor.show()
        if self.run_blinking:
            self.blink_ids = [self.after(self.blink_time, self.blink_hide)]
        self.cursors_update()

    def blink_hide(self):
        self.blink_ids = []
        for cursor in self.cursor_manager.set:
            cursor.hide()
        if self.run_blinking:
            self.blink_ids = [self.after(self.blink_time, self.blink_show)]
        self.cursors_update()

    def focus_in(self, event):
        if not self.run_blinking:
            self.blink_ids = [self.after(self.blink_time, self.blink_show)]
        self.full_update_with_scrolls()
        self.run_blinking = True

    def focus_out(self, event):
        self.run_blinking = False
        for id in self.blink_ids:
            self.after_cancel(id)
        self.blink_ids = []
        self.full_update_with_scrolls()

    def on_key_press(self, event):
        if event.char == '\r':
            self.controller.new_lines()
        elif event.char == '\b':
            self.controller.delete()
        elif event.char.isprintable() and event.char != "":
            self.controller.insert(event.char)
        elif event.keysym == 'Delete':
            self.controller.delete_right()
        elif event.keysym == "Right":
            self.cursor_manager.move_right()
        elif event.keysym == "Left":
            self.cursor_manager.move_left()
        elif event.keysym == "Up":
            self.cursor_manager.move_up()
        elif event.keysym == "Down":
            self.cursor_manager.move_down()

        self.full_update_with_scrolls()

    def offsets(self):
        x_offset_letters = self.xview_pos * self.text.max_row_len
        x0_pixels = -(x_offset_letters % 1) * self.letter_width
        y_offset_letters = self.yview_pos * self.text.max_column_len
        y0_pixels = -(y_offset_letters % 1) * self.letter_height
        return (x_offset_letters, y_offset_letters), (x0_pixels, y0_pixels)

    def _get_indexes_of_viewport(self, letter_offsets = None):
        if letter_offsets is None:
            letter_offsets, _ = self.offsets()
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
        return [string[j0:j1+1] for string in self.text.array_of_strings[i0:i1+1]]


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
        range = self._get_indexes_of_viewport()
        for cursor in self.cursor_manager.get_visible_cursors(range):
             i, j = cursor.position
             global_x, global_y = self.letter_width * j, self.letter_height * i - self.font_metrics.fAscent
             x_shift, y_shift = self.xview_pos * self.text.max_row_len * self.letter_width, self.yview_pos * self.text.max_column_len * self.letter_height
             x, y = global_x - x_shift, global_y - y_shift
             rect = skia.Rect(l=x - self.letter_width, t=y + self.font_metrics.fAscent, r=x + self.letter_width,
                         b=y + self.font_metrics.fDescent)
             self.canvas.drawRect(rect, paint_background)
             paint = skia.Paint(AntiAlias=True, Color=skia.ColorBLACK)
             chars = self.text.symbols_on_cursor(cursor)
             if chars[0]:
                char = chars[0]
                token = self.syntax_highlighter.get_token_at_position(i, j-1)
                color = get_color(token)
                paint.setColor(color)
                self.canvas.drawString(char, x-self.letter_width, y, self.font, paint)
             if chars[1]:
                char = chars[1]
                token = self.syntax_highlighter.get_token_at_position(i, j)
                color = get_color(token)
                paint.setColor(color)
                self.canvas.drawString(char, x, y, self.font, paint)

        self._draw_cursors()
        self.update_image()


    def get_text(self):
        return self.text.get_text()