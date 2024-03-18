
# std
import os
import io
import threading
import collections

# site
import win32api
import win32con
import win32clipboard
import PIL.Image
import PIL.ImageTk
import PIL.ImageGrab
import ttkbootstrap
import windnd
import pyperclip
import pygetwindow
from ttkbootstrap.constants import *

# libs
import core


TARGET_WIDTH = 450
TARGET_HEIGHT = 900

SKEW_WIDTH = 0
SKEW_HEIGHT = 25

USERNAME = os.environ.get('USERNAME')

SAVE_TO = f"C:\\Users\\{USERNAME}\\Desktop\\preview.png"

TEXT = f"""
强迫症预览图裁剪工具
为你的强迫症之路舔砖 Java (加瓦)

请保证游戏以 1920 x 1080 分辨率运行

方法一
使用截图工具截取完整的游戏画面
再将截图拖拽至此
推荐使用 ShareX

方法二
仅窗口化运行可用
保证游戏画面中心部分没有遮挡
双击这里自动截取

裁剪后的图片会保存到桌面
preview.png

目标宽度：{TARGET_WIDTH}
目标高度：{TARGET_HEIGHT}

横向偏移：{SKEW_WIDTH}
纵向偏移: {SKEW_HEIGHT}
"""

SYNOPSIS = """
左键单机 将图片写入剪切板
回到主窗口在预览图区域右键单击即可导入
""".strip()


WINDOW_TITLES = ["原神", "崩坏：星穹铁道", "Genshin Impact", "Honkai: Star Rail", "", "如果想匹配的窗口名称不在其中", "可以尝试手动输入"]



Coordinates = collections.namedtuple("Coordinates", ["x", "y", "width", "height"])
AccurateCoordinates = collections.namedtuple("AccurateCoordinates", ["abs_x", "abs_y", "rel_x", "rel_y", "width", "height"])


class containe ():
    image: PIL.Image.Image = None
    action = threading.Lock()



class ReferenceLine (object):
    def __init__(self):
        self.grey = "grey"
        self.white = "White"
        self.size = 200
        self.base = "base"
        self.cfe_width = 0

        self.window = ttkbootstrap.Toplevel()
        self.window.overrideredirect(True)
        self.window.configure(highlightthickness=0)
        self.window.configure(background=self.grey)
        self.window.attributes("-transparentcolor", self.grey)
        self.window.attributes("-topmost", True)

        self.canvas = ttkbootstrap.Canvas(self.window, width=self.size, height=self.size, background=self.grey)
        self.canvas.pack(fill=BOTH, expand=True, padx=self.cfe_width, pady=self.cfe_width)
        self.canvas.create_rectangle(0, 0, self.size, self.size, fill=self.grey, outline="", tags=self.base)


    def draw(self, ocis: Coordinates, wcis: AccurateCoordinates, tcis: AccurateCoordinates):
        geometry = f"+{ocis.x-self.cfe_width}+{ocis.y-self.cfe_width}"
        self.window.geometry(geometry)
        self.canvas.configure(width=ocis.width, height=ocis.height)

        self.canvas.delete(self.base)
        original_cs = (0, 0, ocis.width-1, ocis.height-1)
        window_cs = (wcis.rel_x, wcis.rel_y, wcis.rel_x+wcis.width-1, wcis.rel_y+wcis.height-1)
        target_cs = (tcis.rel_x, tcis.rel_y, tcis.rel_x+tcis.width-1, tcis.rel_y+tcis.height-1)
        track_cs = (0, 0, wcis.rel_x, wcis.rel_y, tcis.rel_x, tcis.rel_y, 0, 0)
        self.canvas.create_rectangle(*original_cs, fill=self.grey, outline=self.white, tags=self.base)
        self.canvas.create_rectangle(*window_cs, fill=None, outline=self.white, tags=self.base)
        self.canvas.create_rectangle(*target_cs, fill=None, outline=self.white, tags=self.base)
        self.canvas.create_line(*track_cs, fill=self.white, tags=self.base)

        text_size = f"{tcis.width} x {tcis.height}"
        text_site = f"{tcis.rel_x} ( {tcis.abs_x} ) / {tcis.rel_y} ( {tcis.abs_y} )"
        self.canvas.create_text(tcis.rel_x+5, tcis.rel_y+5, text=text_size, anchor=NW, fill=self.white)
        self.canvas.create_text(tcis.rel_x+5, tcis.rel_y-5, text=text_site, anchor=SW, fill=self.white)

        self.window.update()


    def deiconify(self):
        self.window.deiconify()


    def withdraw(self):
        self.window.withdraw()


    def close(self):
        self.window.destroy()





class PreviewImage (object):
    def __init__(self):
        self.window = ttkbootstrap.Toplevel("强迫症截图工具 - 预览")
        self.window.protocol("WM_DELETE_WINDOW", self.withdraw)

        self.wll = ttkbootstrap.Label(self.window, text="预览区", anchor=CENTER, cursor="plus")
        self.wll.pack(side=TOP, fill=BOTH, expand=True)
        self.wll.bind("<Button-1>", self.writeclipboard)
        self.withdraw()

        core.window.annotation_toplevel.register(self.wll, SYNOPSIS, 2)


    def update(self):
        x, y = containe.image.size
        self.window.geometry(f"{x+4}x{y+4}")
        self.image = PIL.ImageTk.PhotoImage(containe.image)
        self.wll.config(image=self.image)
        self.window.deiconify()


    def withdraw(self, *_):
        self.window.withdraw()


    def writeclipboard(self, *_):
        image_byte_array = io.BytesIO()
        containe.image.save(image_byte_array, format="DIB")
        image_bytes = image_byte_array.getvalue()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_DIB, image_bytes)
        win32clipboard.CloseClipboard()


    def close(self):
        self.window.destroy()





class OCDCrop (object):
    def __init__(self):
        result = containe.action.acquire(timeout=0.01)
        if not result:
            core.window.messagebox.showerror(title="操作已被阻止", message="请勿重复启动该工具")
            return

        self.window = ttkbootstrap.Toplevel()
        core.window.methods.fake_withdraw(self.window)
        # self.position_window = ttkbootstrap.Toplevel()
        self.window.title("强迫症截图工具")
        self.window.resizable(width=False, height=False)
        self.window.attributes("-topmost", True)

        self.window_reference = ReferenceLine()
        self.window_preview = PreviewImage()

        self.wfe_parametric = ttkbootstrap.Frame(self.window)
        self.wfe_control = ttkbootstrap.Frame(self.window)
        self.wfe_parametric.pack(side=LEFT, fill=Y, padx=(5, 5), pady=5)
        # self.wfe_control.pack(side=RIGHT, fill=Y, padx=(0, 5), pady=5)

        self.v_window_name = ttkbootstrap.StringVar(value="原神")
        self.v_recoup_x = ttkbootstrap.IntVar(value=32)
        self.v_recoup_y = ttkbootstrap.IntVar(value=64)
        self.v_window_width = ttkbootstrap.IntVar(value=1920)
        self.v_window_height = ttkbootstrap.IntVar(value=1080)
        self.v_target_width = ttkbootstrap.IntVar(value=TARGET_WIDTH)
        self.v_target_height = ttkbootstrap.IntVar(value=TARGET_HEIGHT)
        self.v_offset_x = ttkbootstrap.IntVar(value=SKEW_WIDTH)
        self.v_offset_y = ttkbootstrap.IntVar(value=SKEW_HEIGHT)

        self.wll_window_name = ttkbootstrap.Label(self.wfe_parametric, text="窗口名称：")
        self.wll_recoup_size = ttkbootstrap.Label(self.wfe_parametric, text="最大补偿：")
        self.wll_window_size = ttkbootstrap.Label(self.wfe_parametric, text="窗口大小：")
        self.wll_target_size = ttkbootstrap.Label(self.wfe_parametric, text="目标大小：")
        self.wll_offset_size = ttkbootstrap.Label(self.wfe_parametric, text="坐标偏移：")

        self.wet_window_name = ttkbootstrap.Combobox(self.wfe_parametric, textvariable=self.v_window_name, values=WINDOW_TITLES)
        self.wet_recoup_x = ttkbootstrap.Entry(self.wfe_parametric, textvariable=self.v_recoup_x)
        self.wet_recoup_y = ttkbootstrap.Entry(self.wfe_parametric, textvariable=self.v_recoup_y)
        self.wet_window_w = ttkbootstrap.Entry(self.wfe_parametric, textvariable=self.v_window_width)
        self.wet_window_h = ttkbootstrap.Entry(self.wfe_parametric, textvariable=self.v_window_height)
        self.wet_target_w = ttkbootstrap.Entry(self.wfe_parametric, textvariable=self.v_target_width)
        self.wet_target_h = ttkbootstrap.Entry(self.wfe_parametric, textvariable=self.v_target_height)
        self.wet_offset_x = ttkbootstrap.Entry(self.wfe_parametric, textvariable=self.v_offset_x)
        self.wet_offset_y = ttkbootstrap.Entry(self.wfe_parametric, textvariable=self.v_offset_y)

        self.wll_window_name.grid(row=0, column=0, sticky=E, pady=(0, 0))
        self.wll_recoup_size.grid(row=1, column=0, sticky=E, pady=(5, 0))
        self.wll_window_size.grid(row=2, column=0, sticky=E, pady=(5, 0))
        self.wll_target_size.grid(row=3, column=0, sticky=E, pady=(5, 0))
        self.wll_offset_size.grid(row=4, column=0, sticky=E, pady=(5, 0))

        self.wet_window_name.grid(row=0, column=1, sticky=EW, padx=(5, 0), pady=(0, 0), columnspan=2)
        self.wet_recoup_x.grid(row=1, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.wet_recoup_y.grid(row=1, column=2, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.wet_window_w.grid(row=2, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.wet_window_h.grid(row=2, column=2, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.wet_target_w.grid(row=3, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.wet_target_h.grid(row=3, column=2, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.wet_offset_x.grid(row=4, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.wet_offset_y.grid(row=4, column=2, sticky=EW, padx=(5, 0), pady=(5, 0))

        self.wbn_reference = ttkbootstrap.Button(self.wfe_parametric, text="显示/更新参考线", bootstyle=(SUCCESS, OUTLINE), command=self.bin_reference)
        self.wbn_withdraw = ttkbootstrap.Button(self.wfe_parametric, text="隐藏参考线", bootstyle=(SUCCESS, OUTLINE), command=self.bin_withdraw)
        self.wbn_default = ttkbootstrap.Button(self.wfe_parametric, text="默认设置", bootstyle=(SUCCESS, OUTLINE), command=self.bin_default)
        self.wbn_clipboard = ttkbootstrap.Button(self.wfe_parametric, text="从剪贴板获取", bootstyle=(SUCCESS, OUTLINE), command=self.bin_clipboard)
        self.wbn_screenshot = ttkbootstrap.Button(self.wfe_parametric, text="截图", bootstyle=(SUCCESS, OUTLINE), command=self.bin_screenshot)

        self.wbn_reference.grid(row=0, column=3, sticky=EW, padx=(5, 0), pady=(0, 0))
        self.wbn_withdraw.grid(row=1, column=3, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.wbn_default.grid(row=2, column=3, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.wbn_clipboard.grid(row=3, column=3, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.wbn_screenshot.grid(row=4, column=3, sticky=EW, padx=(5, 0), pady=(5, 0))

        try:
            self.window.iconbitmap(default=core.env.file.local.iconbitmap)
            self.window.iconbitmap(bitmap=core.env.file.local.iconbitmap)
        except Exception:
            ...

        # self.wll_image.bind("<Double-1>", self.bin_skin)
        windnd.hook_dropfiles(self.window, func=self.bin_drop)
        self.window.protocol('WM_DELETE_WINDOW', self.bin_close)
        self.window.update()
        core.window.methods.center_window_for_window(self.window, core.window.mainwindow)

        self.bin_load_setting()


    def examine(self, *_):
        v_window_name = self.v_window_name.get()
        if not v_window_name:
            core.window.messagebox.showerror(title="错误", message="窗口名称不能为空", parent=self.window)
            raise ValueError("窗口名称不能为空")

        cannot_be_zero = {
            "横向最大补偿距离": self.v_recoup_x,
            "纵向最大补偿距离": self.v_recoup_y,
            "窗口宽度": self.v_window_width,
            "窗口高度": self.v_window_height,
            "目标宽度": self.v_target_width,
            "目标高度": self.v_target_height
        }
        others = {
            "横向偏移": self.v_offset_x,
            "纵向偏移": self.v_offset_y
        }

        for name, variable in cannot_be_zero.items():
            try:
                value = variable.get()

            except Exception as _:
                msg = f"{name} 参数不合法"
                core.window.messagebox.showerror(title="错误", message=msg, parent=self.window)
                raise ValueError

            if value < 0:
                msg = f"{name} 不能小于 0"
                core.window.messagebox.showerror(title="错误", message=msg, parent=self.window)
                raise ValueError(msg)

        for name, variable in others.items():
            try:
                value = variable.get()

            except Exception as _:
                msg = f"{name} 参数不合法"
                core.window.messagebox.showerror(title="错误", message=msg, parent=self.window)
                raise ValueError(msg)


    def calculate_main_screen_vertex_coordinates(self) -> tuple[int, int]:
        screen_amount = win32api.GetSystemMetrics(win32con.SM_CMONITORS)
        if screen_amount <= 1:
            return 0, 0

        display_monitors = win32api.EnumDisplayMonitors(None, None)
        vertex_x, vertex_y = 0, 0

        for monitor in display_monitors:
            nw_x, nw_y, se_x, se_y = monitor[-1]
            vertex_x = min(vertex_x, nw_x)
            vertex_y = min(vertex_y, nw_y)
            continue

            win32api.GetMonitorInfo(monitor[0])

        return abs(vertex_x), abs(vertex_y)


    def calculate_original_window_coordinates(self) -> Coordinates:
        window_title = self.v_window_name.get()

        try:
            target_window = pygetwindow.getWindowsWithTitle(window_title)[0]

        except Exception:
            msg = f"找不到窗口 {window_title}"
            core.window.messagebox.showerror(title="错误", message=msg, parent=self.window)
            raise ValueError(msg)

        coordinates = Coordinates(target_window.left, target_window.top, target_window.width, target_window.height)
        return coordinates


    def calculate_window_coordinates(self, ocis: Coordinates, width: int, height: int, recoup_x, recoup_y):
        offset_x = (ocis.width - width) // 2
        offset_y = (ocis.height - height) // 2
        rel_x = offset_x
        rel_y = ocis.height - offset_x - height

        if abs(offset_x) > recoup_x or abs(rel_y) > recoup_y:
            rel_y = offset_y

        abs_x = ocis.x + rel_x
        abs_y = ocis.y + rel_y
        coordinates = AccurateCoordinates(abs_x, abs_y, rel_x, rel_y, width, height)
        return coordinates


    def calculate_target_coordinates(self,
            ocis: Coordinates, wcis: AccurateCoordinates,
            target_width: int, target_height: int, offset_x: int = 0, offset_y: int = 0
            ) -> AccurateCoordinates:
        relative_window_x = (wcis.width - target_width) // 2 + offset_x
        relative_window_y = (wcis.height - target_height) // 2 + offset_y
        rel_x = relative_window_x + wcis.rel_x
        rel_y = relative_window_y + wcis.rel_y
        abs_x = rel_x + ocis.x
        abs_y = rel_y + ocis.y
        coordinates = AccurateCoordinates(abs_x, abs_y, rel_x, rel_y, target_width, target_height)
        return coordinates


    def calculate_coordinates(self, original_image: PIL.Image.Image = ...) -> tuple[Coordinates, AccurateCoordinates, AccurateCoordinates]:
        self.examine()
        if original_image is Ellipsis:
            ocis = self.calculate_original_window_coordinates()

        else:
            ocis = Coordinates(0, 0, original_image.width, original_image.height)

        vr_x = self.v_recoup_x.get()
        vr_y = self.v_recoup_y.get()
        vw_w = self.v_window_width.get()
        vw_h = self.v_window_height.get()
        vt_w = self.v_target_width.get()
        vt_h = self.v_target_height.get()
        vo_x = self.v_offset_x.get()
        vo_y = self.v_offset_y.get()

        wcis = self.calculate_window_coordinates(ocis, vw_w, vw_h, vr_x, vr_y)
        tcis = self.calculate_target_coordinates(ocis, wcis, vt_w, vt_h, vo_x, vo_y)
        return ocis, wcis, tcis


    def execution(self, orimage: PIL.Image.Image = ...):
        if orimage is Ellipsis:
            ocis, wcis, tcis = self.calculate_coordinates()
            self.window_reference.draw(ocis, wcis, tcis)
            nw_x = ocis.x
            nw_y = ocis.y
            se_x = nw_x + ocis.width
            se_y = nw_y + ocis.height
            site = (nw_x, nw_y, se_x, se_y)
            orimage = PIL.ImageGrab.grab(bbox=site, all_screens=True)

        else:
            ocis, wcis, tcis = self.calculate_coordinates(orimage)

        site = (tcis.rel_x, tcis.rel_y, tcis.rel_x+tcis.width, tcis.rel_y+tcis.height)
        result = orimage.crop(site)
        containe.image = result
        self.window_preview.update()


    def bin_reference(self, *_):
        coordinates = self.calculate_coordinates()
        self.window_reference.draw(*coordinates)
        self.window_reference.deiconify()


    def bin_withdraw(self, *_):
        self.window_reference.withdraw()


    def bin_default(self, *_):
        self.v_window_name.set("原神")
        self.v_recoup_x.set(32)
        self.v_recoup_y.set(64)
        self.v_window_width.set(1920)
        self.v_window_height.set(1080)
        self.v_target_width.set(TARGET_WIDTH)
        self.v_target_height.set(TARGET_HEIGHT)
        self.v_offset_x.set(SKEW_WIDTH)
        self.v_offset_y.set(SKEW_HEIGHT)
        self.bin_withdraw()


    def bin_load_setting(self, *_):
        if core.env.configuration.ocd_window_name is None: return
        self.v_window_name.set(core.env.configuration.ocd_window_name)
        self.v_recoup_x.set(core.env.configuration.ocd_recoup_x)
        self.v_recoup_y.set(core.env.configuration.ocd_recoup_y)
        self.v_window_width.set(core.env.configuration.ocd_window_width)
        self.v_window_height.set(core.env.configuration.ocd_window_height)
        self.v_target_width.set(core.env.configuration.ocd_target_width)
        self.v_target_height.set(core.env.configuration.ocd_target_height)
        self.v_offset_x.set(core.env.configuration.ocd_offset_x)
        self.v_offset_y.set(core.env.configuration.ocd_offset_y)


    def bin_save_settings(self, *_):
        core.env.configuration.ocd_window_name = self.v_window_name.get()
        core.env.configuration.ocd_recoup_x = self.v_recoup_x.get()
        core.env.configuration.ocd_recoup_y = self.v_recoup_y.get()
        core.env.configuration.ocd_window_width = self.v_window_width.get()
        core.env.configuration.ocd_window_height = self.v_window_height.get()
        core.env.configuration.ocd_target_width = self.v_target_width.get()
        core.env.configuration.ocd_target_height = self.v_target_height.get()
        core.env.configuration.ocd_offset_x = self.v_offset_x.get()
        core.env.configuration.ocd_offset_y = self.v_offset_y.get()


    def bin_screenshot(self, *_):
        self.execution()
        self.bin_save_settings()


    def bin_clipboard(self, *_):
        image = PIL.ImageGrab.grabclipboard()
        if image is None:
            core.window.messagebox.showerror(title="错误", message="剪切板内容不是图片", parent=self.window)
            return
        self.execution(image)


    def bin_drop(self, items):
        item = items.pop()
        content = item.decode("gb18030")
        image = PIL.Image.open(content)
        if image is None: return
        self.execution(image)


    def bin_close(self, *_):
        containe.action.release()
        self.window_reference.close()
        self.window_preview.close()
        self.window.destroy()
