# Licensed under the GPL 3.0 License.
# d3dxSkinManage by numlinka.

# std
import tkinter

# site
import ttkbootstrap
from ttkbootstrap.constants import *


class ScrollFrame (ttkbootstrap.Frame):
    def __init__(self, master, horizontal_scroller: bool = None, vertical_scroller: bool = None,
                 scb_pad: int = 0, auto_bind_scroll: bool = True, **kw):
        """
        A frame that contains a canvas and scrollbars for scrolling its contents.
        包含画布和用于滚动其内容的滚动条的框架.

        ```TEXT
        master:
            The master widget.
            父控件.

        horizontal_scroller:
            Whether to show the horizontal scrollbar. When None, adapt based on content.
            是否显示水平滚动条. 为 None 时根据内容自适应.

        vertical_scroller:
            Whether to show the vertical scrollbar. When None, adapt based on content.
            是否显示垂直滚动条. 为 None 时根据内容自适应.

        scb_pad:
            The amount of padding between the canvas and the scrollbars.
            画布和滚动条之间的间距.

        auto_bind_scroll:
            Whether to automatically bind scroll events.
            Will not bind to those widget that have mousewheel events themselves.
            是否自动绑定滚动事件.
            不会绑定到那些本身具有鼠标滚轮事件的控件.

        **kw:
            Additional keyword arguments to pass to the ttk.Frame constructor.
            附加关键字参数传递到 ttk.Frame 构造函数.
        ```
        """


        self._layout_attribute_name = [
            "pack", "pack_configure", "pack_forget", "pack_info", "pack_propagate", "pack_slaves",
            "grid", "grid_anchor", "grid_bbox", "grid_columnconfigure", "grid_configure", "grid_forget", "grid_info",
            "grid_location", "grid_propagate", "grid_remove", "grid_rowconfigure", "grid_size", "grid_slaves",
            "place", "place_configure", "place_forget", "place_info", "place_slaves"
        ]

        self._bind_widgets_class_name_whitelist = [
            "Labelframe", "Frame", "Label", "Button", "Checkbutton", "Entry",
            "TLabelframe", "TFrame", "TLabel", "TButton", "TCheckbutton", "TEntry"
            ]

        superiors = super()

        self.w_master_frame = ttkbootstrap.Frame(master)
        self.w_canvas = ttkbootstrap.Canvas(self.w_master_frame, width=0, height=0)
        superiors.__init__(self.w_canvas, **kw)
        self.w_horz_scb = ttkbootstrap.Scrollbar(self.w_master_frame, orient=HORIZONTAL, command=self.w_canvas.xview)
        self.w_vert_scb = ttkbootstrap.Scrollbar(self.w_master_frame, orient=VERTICAL, command=self.w_canvas.yview)

        self.v_horz_scb = horizontal_scroller
        self.v_vert_scb = vertical_scroller
        self.v_scb_pad = scb_pad
        self.v_auto_scl = auto_bind_scroll
        self._v_widget_amount = -1
        self._can_scroll = False

        self.w_canvas.configure(scrollregion=self.w_canvas.bbox(ALL))
        self.w_canvas.configure(yscrollcommand=self.w_vert_scb.set)
        self.w_canvas.configure(xscrollcommand=self.w_horz_scb.set)

        self.w_canvas.bind("<Configure>", self.bin_update, True)
        self.w_canvas.bind("<MouseWheel>", self.bin_event_mousewheel, True)
        self.bind("<Configure>", self.sbin_event_variety, True)
        self.bind("<MouseWheel>", self.bin_event_mousewheel, True)


        self.w_canvas.grid(row=0, column=0, sticky=NSEW)
        self.w_master_frame.columnconfigure(0, weight=1)
        self.w_master_frame.rowconfigure(0, weight=1)

        self.w_canvas.create_window((0, 0), window=self, anchor=NW)

        self.sbin_redirect_layout()
        self.bin_update()


    def sbin_redirect_layout(self, *_):
        """## 替换布局方法

        ```TEXT
        Layout method that redirects to an external frame.
        重定向到外部 Frame 的布局方法.
        ```
        """
        for attr_name in self._layout_attribute_name:
            setattr(self, attr_name, getattr(self.w_master_frame, attr_name))


    def sbin_reduction_layout(self, *_):
        """## 还原布局方法

        无特殊情况不要使用.
        """
        superiors = super()

        for attr_name in self._layout_attribute_name:
            setattr(self, attr_name, getattr(superiors, attr_name))


    def sbin_event_variety(self, event: tkinter.Event):
        """## 控件变动事件"""
        now_widget_list = self.winfo_children()
        now_widget_amount = len(now_widget_list)
        if now_widget_amount != self._v_widget_amount:
            self._v_widget_amount = now_widget_amount

            if self.v_auto_scl:
                self.bin_child_widgets_bind()

        self.bin_update()


    def bin_event_mousewheel(self, event: tkinter.Event):
        """## 鼠标滚轮事件"""
        if not self._can_scroll: return
        if event.delta > 0:
            self.w_canvas.yview_scroll(-1, "units")
        else:
            self.w_canvas.yview_scroll(1, "units")


    def bin_update_scrollregion(self, *_):
        """## 更新滚动区域"""
        self.w_canvas.configure(scrollregion=self.w_canvas.bbox(ALL))


    def bin_update_scb_need(self, *_):
        """## 更新滚动条需要"""
        self.w_canvas.update_idletasks()
        canvas_w = self.w_canvas.winfo_width()
        canvas_h = self.w_canvas.winfo_height()

        site = self.w_canvas.bbox(ALL)
        if site is None:
            bbox_w, bbox_h = 0, 0

        else:
            _, _, bbox_w, bbox_h = site

        if self.v_horz_scb is True or (self.v_horz_scb is None and bbox_w > canvas_w):
            self.w_horz_scb.grid(row=1, column=0, sticky=EW, pady=(self.v_scb_pad, 0))

        else:
            self.w_horz_scb.grid_forget()

        if self.v_vert_scb is True or (self.v_vert_scb is None and bbox_h > canvas_h):
            self.w_vert_scb.grid(row=0, column=1, sticky=NS, padx=(self.v_scb_pad, 0))

        else:
            self.w_vert_scb.grid_forget()

        # 当 Frame 高度小于 Canvas 高度时 禁用滚动事件
        self._can_scroll = True if bbox_h > canvas_h else False


    def bin_update(self, *_):
        """## 更新整体状态"""
        self.bin_update_scrollregion()
        self.bin_update_scb_need()


    def bin_auto_resize(self, *_):
        """## 自动调整尺寸"""
        site = self.w_canvas.bbox(ALL)
        if site is None:
            return

        _, _, bbox_w, bbox_h = site
        self.w_canvas.config(width=bbox_w, height=bbox_h)


    def bin_allow_scrolling(self, *widgets: tkinter.Widget):
        """## 允许控件滚动事件

        ```TEXT
        Bind scroll events to controls
        为控件绑定滚动事件
        ```
        """
        for widget in widgets:
            widget.bind("<MouseWheel>", self.bin_event_mousewheel, True)


    def bin_child_widgets_bind(self, widget: tkinter.Widget = ..., recursion: bool = True):
        """为控件的子控件绑定滚动事件"""
        if widget is Ellipsis: widget = self
        child_widget_list = widget.winfo_children()

        for child_widget in child_widget_list:
            if child_widget.winfo_class() in self._bind_widgets_class_name_whitelist:
                if not child_widget.bind("<MouseWheel>"):
                    self.bin_allow_scrolling(child_widget)

                if recursion:
                    self.bin_child_widgets_bind(child_widget, recursion)

            else:
                continue
