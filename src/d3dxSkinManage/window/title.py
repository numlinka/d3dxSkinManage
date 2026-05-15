# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# site
import ttkbootstrap

# local
import core


class Title (object):
    def __init__(self, master):
        self.master = master

        self.label = ttkbootstrap.Button(self.master, text="X")

        self.label.pack(side="right", padx=10, pady=10)

        self.label.bind("<Button-1>", lambda *_: core.window.mainwindow.destroy())

        self.master.config(cursor="fleur")
        self.master.bind("<Button-1>", self.start_drag)
        self.master.bind("<B1-Motion>", self.on_drag)


    def start_drag(self, event):
        # 鼠标按下事件处理函数
        widget = event.widget
        widget.start_x = event.x
        widget.start_y = event.y


    def on_drag(self, event):
        # 鼠标拖动事件处理函数
        widget = event.widget
        x = core.window.mainwindow.winfo_x() - widget.start_x + event.x
        y = core.window.mainwindow.winfo_y() - widget.start_y + event.y
        core.window.mainwindow.geometry(f"+{x}+{y}")
