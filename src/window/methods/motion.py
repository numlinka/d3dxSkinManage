# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import tkinter

# site
import ttkbootstrap

# local
import core


class motion_window_by_canvas (object):
    def __init__(self, window: ttkbootstrap.Window, widget: ttkbootstrap.Canvas, tag: str):
        self.window = window
        self.widget = widget
        self.tag = tag
        self.widget.tag_bind(tag, "<Button-1>", self.start_drag)
        self.widget.tag_bind(tag, "<B1-Motion>", self.on_drag)
        self.start_x = 0
        self.start_y = 0


    def start_drag(self, event: ttkbootstrap):
        self.start_x = event.x
        self.start_y = event.y


    def on_drag(self, event):
        x = self.window.winfo_x() - self.start_x + event.x
        y = self.window.winfo_y() - self.start_y + event.y
        self.window.geometry(f"+{x}+{y}")



class motion_treeview_width (object):
    def __init__(self, window: ttkbootstrap.Window, widget_target: ttkbootstrap.Treeview, widget_event: tkinter.Widget):
        self.window = window
        self.widget_target = widget_target
        self.widget_event = widget_event

        self.widget_event.bind("<Button-1>", self.start_drag)
        self.widget_event.bind("<B1-Motion>", self.on_drag)

        self.start_x = 0
        self.column_names = []
        self.column_start_width = []
        self.column_final_width = []


    def start_drag(self, event: tkinter.Event):
        self.start_x, _ = self.window.winfo_pointerxy()
        self.column_names = ["#0"] + list(self.widget_target["columns"])
        self.column_start_width = [self.widget_target.column(x)["width"] for x in self.column_names]


    def on_drag(self, event: tkinter.Event):
        x, _ = self.window.winfo_pointerxy()
        offset = x - self.start_x
        core.log.warn(offset)
        width = self.column_start_width[-1] + offset
        self.widget_target.column(self.column_names[-1], width=width)


class motion_frame_width (object):
    def __init__(self, window: ttkbootstrap.Window, widget_target: ttkbootstrap.Frame, widget_event: tkinter.Widget):
        self.window = window
        self.widget_target = widget_target
        self.widget_event = widget_event

        self.widget_event.bind("<Button-1>", self.start_drag)
        self.widget_event.bind("<B1-Motion>", self.on_drag)

        self.start_x = 0
        self.start_width = 0


    def start_drag(self, event: ttkbootstrap):
        self.start_x, _ = self.window.winfo_pointerxy()
        self.start_width = self.widget_target.winfo_width()


    def on_drag(self, event):
        x, _ = self.window.winfo_pointerxy()
        offset = x - self.start_x
        width = self.start_width + offset
        core.log.warn((offset, width))
        self.widget_target.config(width=width)
