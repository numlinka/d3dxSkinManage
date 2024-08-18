# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import webbrowser

# site
import ttkbootstrap

# local
import core

# self
from . import suggestions


class Status (object):
    def __init__(self, master):
        self.master = master

        self.sizegrip = ttkbootstrap.Sizegrip(self.master)
        self.label_username = ttkbootstrap.Label(self.master, text="* /")
        self.label_mark = ttkbootstrap.Label(self.master, text="[S]")
        self.label_status = ttkbootstrap.Label(self.master, text="-")
        self.progressbar_step = ttkbootstrap.Progressbar(self.master)

        # self.Label_logout = ttkbootstrap.Label(self.master, text="[ 注销 ]", foreground="#00FFFF", cursor="hand2")
        # self.Label_logout.pack(side="right", padx=10, pady=5 )

        self.sizegrip.pack(side="right", fill="y")

        self.label_help = ttkbootstrap.Label(self.master, text="[ 帮助 ]", cursor="hand2")
        self.label_suggestions = ttkbootstrap.Label(self.master, text="[ 优化建议 ]", cursor="hand2")
        self.label_help.pack(side="right", padx=10, pady=5 )
        self.label_suggestions.pack(side="right", padx=(10, 0), pady=5 )

        self.label_username.pack(side="left", padx=5, pady=5)
        self.label_mark.pack(side="left", padx=5, pady=5)
        self.label_status.pack(side="left", padx=5, pady=5)
        self.progressbar_step.pack(side="left", padx=5, pady=5)

        self.label_help.bind("<Button-1>", self.bin_open_help)
        self.label_suggestions.bind("<Button-1>", self.bin_open_suggestions)


    def bin_open_help(self, *args):
        webbrowser.open(core.env.Link.help)


    def bin_open_suggestions(self, *_):
        suggestions.Suggestions()


    def set_userName(self, userName):
        self.label_username["text"] = f"* {userName}"


    def set_mark(self, mark):
        self.label_mark["text"] = f"[{mark}]"


    def set_progress(self, value: int):
        if not isinstance(value, int): return
        self.progressbar_step.config(value=value)


    def set_status(self, status, LEVEL: int = 0):
        if not isinstance(LEVEL, int): LEVEL = 0
        color = ["", "red", "orange"][LEVEL]
        self.label_status["text"] = status
        self.label_status["foreground"] = color
