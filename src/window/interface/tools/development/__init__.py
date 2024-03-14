

import threading

import ttkbootstrap

import core

from . import signal_event
from . import script

TEXT = """
开发者调试工具

警告！你需要对自己的行为负责，自行承担后果
该工具可以略过行为检查直接对 core 模块进行操作
操作不当会导致其他模块故障或损坏数据库
你已经被警告过了
""".strip()


class containe ():
    action = threading.Lock()


class Development (object):

    def __init__(self):
        result = containe.action.acquire(timeout=0.01)
        if not result:
            core.window.messagebox.showerror(title="操作已被阻止", message="请勿重复启动该工具")
            return

        self.window = ttkbootstrap.Toplevel()
        self.window.title("development debug tool")

        try:
            self.window.iconbitmap(default=core.env.file.local.iconbitmap)
            self.window.iconbitmap(bitmap=core.env.file.local.iconbitmap)
        except Exception:
            ...

        self.window.protocol("WM_DELETE_WINDOW", self.bin_close)

        self.notebook = ttkbootstrap.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_warn = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_warn, text="WARN")

        self.frame_signal_event = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_signal_event, text="signal/event")

        self.frame_script = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_script, text="script")

        signal_event.SignalEvent(self.frame_signal_event)
        script.Script(self.frame_script)

        self.label = ttkbootstrap.Label(self.frame_warn, text=TEXT)
        self.label.pack(fill="both", padx=10, pady=10)
        self.window.update()
        core.window.methods.center_window_for_window(self.window, core.window.mainwindow)


    def bin_close(self, *_):
        containe.action.release()
        self.window.destroy()