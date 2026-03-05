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
        # self._sw = self.toplevel.winfo_screenwidth()
        # self._sh = self.toplevel.winfo_screenheight()
        self.coordinates = methods.get_screen_coordinates()

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


    # def old_update_position(self):
    #     v = 15
    #     w = self.toplevel.winfo_width()
    #     h = self.toplevel.winfo_height()
    #     x = self.toplevel.winfo_pointerx()
    #     y = self.toplevel.winfo_pointery()
    #     _x = x - v - w if x + v + w > self._sw else x + v
    #     _y = y - v - h if y + v + h > self._sh else y + v
    #     self.toplevel.geometry(f"+{_x}+{_y}")


    def update_position(self):
        v = 15
        px = self.toplevel.winfo_pointerx()
        py = self.toplevel.winfo_pointery()
        ww = self.toplevel.winfo_width()
        wh = self.toplevel.winfo_height()

        for screen in self.coordinates:
            if screen[0][0] <= px <= screen[1][0] and screen[0][1] <= py <= screen[1][1]:
                sl, st = screen[0]
                sr, sb = screen[1]
                sb -= self._th
                break

        else:
            ax = px + v
            ay = py + v
            self.toplevel.geometry(f"+{ax}+{ay}")
            return

        xl = 1 if px + v + ww > sr else 0
        yl = 1 if py + v + wh > sb else 0

        if xl == yl == 0:
            ax = px + v
            ay = py + v

        elif xl == 1 and yl == 0:
            ax = sr - ww
            ay = py + v

        elif xl == 0 and yl == 1:
            ax = px + v
            ay = sb - wh

        else:
            if sl + ww + v <= px:
                ax = px - v - ww
                ay = sb - wh if py + v + wh > sb else py + v

            elif st + wh + v <= py:
                ax = sr - ww if px + v + ww > sb else px + v
                ay = py - v - wh

            else:
                ax = px + v
                ay = py + v

        self.toplevel.geometry(f"+{ax}+{ay}")


    def withdraw(self):
        methods.fake_withdraw(self.toplevel)
        # self.toplevel.withdraw()


    def deiconify(self):
        self.coordinates = methods.get_screen_coordinates()
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
