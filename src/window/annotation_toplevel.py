# -*- coding: utf-8 -*-

import ctypes

import ttkbootstrap

import core


class AnnotationToplevel (object):
    def __init__(self):
        self.toplevel = ttkbootstrap.Toplevel()
        self.toplevel.overrideredirect(True)
        self.label = ttkbootstrap.Label(self.toplevel, text="这是一个测试描述\n当然他是可以修改的")
        self.label.pack()
        self.withdraw()
        self._sw = self.toplevel.winfo_screenwidth()
        self._sh = self.toplevel.winfo_screenheight()

        try:
            hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            taskbar_height = rect.bottom - rect.top
            self._sh -= taskbar_height

        except Exception:
            core.log.error("未能正确获取 windows 任务栏的高度")


    def update_position(self):
        v = 15
        w = self.toplevel.winfo_width()
        h = self.toplevel.winfo_height()
        x = self.toplevel.winfo_pointerx()
        y = self.toplevel.winfo_pointery()
        _x = x - v - w if x + v + w > self._sw else x + v
        _y = y - v - h if y + v + h > self._sh else y + v
        self.toplevel.geometry(f"+{_x}+{_y}")


    def withdraw(self):
        self.toplevel.withdraw()


    def deiconify(self):
        self.toplevel.deiconify()


    def deiconify_content(self, content):
        self.update_content(content)
        self.deiconify()


    def update_content(self, content):
        self.label.config(text=f"{content}")


    def register(self, control, content: str):
        control.bind("<Motion>", lambda *_: self.update_position())
        control.bind("<Enter>", lambda *_: self.deiconify_content(content))
        control.bind("<Leave>", lambda *_: self.withdraw())
