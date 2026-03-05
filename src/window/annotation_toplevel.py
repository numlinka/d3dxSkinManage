# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import ctypes

# site
import ttkbootstrap

# local
import core

# self
from . import methods


class AnnotationToplevel (object):
    def __init__(self):
        self.toplevel = ttkbootstrap.Toplevel()
        self.toplevel.overrideredirect(True)
        self.frame = ttkbootstrap.Frame(self.toplevel, borderwidth=2, relief="solid")
        self.frame.pack()
        self.label = ttkbootstrap.Label(self.frame, text="这是一个测试描述\n当然他是可以修改的", )
        self.label.pack(padx=4, pady=4)
        self.withdraw()
        self._sw = self.toplevel.winfo_screenwidth()
        self._sh = self.toplevel.winfo_screenheight()

        try:
            hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            taskbar_height = rect.bottom - rect.top
            # self._sh -= taskbar_height
            self._th = taskbar_height

        except Exception:
            self._th = 0
            core.log.error("未能正确获取 windows 任务栏的高度")


    def old_update_position(self):
        v = 15
        w = self.toplevel.winfo_width()
        h = self.toplevel.winfo_height()
        x = self.toplevel.winfo_pointerx()
        y = self.toplevel.winfo_pointery()
        _x = x - v - w if x + v + w > self._sw else x + v
        _y = y - v - h if y + v + h > self._sh else y + v
        self.toplevel.geometry(f"+{_x}+{_y}")


    def update_position(self):
        v = 15
        sw = self.toplevel.winfo_screenwidth()
        sh = self.toplevel.winfo_screenheight() - self._th
        px = self.toplevel.winfo_pointerx()
        py = self.toplevel.winfo_pointery()
        ww = self.toplevel.winfo_width()
        wh = self.toplevel.winfo_height()

        xl = 1 if px + v + ww > sw else 0
        yl = 1 if py + v + wh > sh else 0

        if xl == yl == 0:
            ax = px + v
            ay = py + v

        elif xl == 1 and yl == 0:
            ax = sw - ww
            ay = py + v

        elif xl == 0 and yl == 1:
            ax = px + v
            ay = sh - wh

        else:
            if ww + v <= px:
                ax = px - v - ww
                ay = sh - wh if py + v + wh > sh else py + v

            elif wh + v <= py:
                ax = sw - ww if px + v + ww > sh else px + v
                ay = py - v - wh

            else:
                ax = px + v
                ay = py + v

        self.toplevel.geometry(f"+{ax}+{ay}")


    def withdraw(self):
        methods.fake_withdraw(self.toplevel)
        # self.toplevel.withdraw()


    def deiconify(self):
        self.toplevel.deiconify()


    def deiconify_content(self, content: str, level: int = 3):
        if level > core.env.configuration.annotation_level:
            return

        self.update_content(content)
        self.deiconify()


    def update_content(self, content):
        self.label.config(text=f"{content}")


    def register(self, control, content: str, level: int = 3):
        control.bind("<Motion>", lambda *_: self.update_position(), "+")
        control.bind("<Enter>", lambda *_: self.deiconify_content(content, level), "+")
        control.bind("<Leave>", lambda *_: self.withdraw(), "+")
