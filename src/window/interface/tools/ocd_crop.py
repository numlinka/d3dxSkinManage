
# std
import os
import threading

# site
import PIL.Image
import PIL.ImageTk
import PIL.ImageGrab
import ttkbootstrap
import windnd
import pygetwindow

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


class containe ():
    image_tk = None
    action = threading.Lock()


class OCDCrop (object):
    def __init__(self):
        result = containe.action.acquire(timeout=0.01)
        if not result:
            core.window.messagebox.showerror(title="操作已被阻止", message="请勿重复启动该工具")
            return

        self.window = ttkbootstrap.Toplevel()
        self.window.title("强迫症裁图")
        self.window.geometry(f"{TARGET_WIDTH+10}x{TARGET_HEIGHT+10}")
        self.window.resizable(width=False, height=False)

        self.label = ttkbootstrap.Label(self.window, text=TEXT, anchor="center")
        self.label.pack(side="top", fill="both", expand=True)

        try:
            self.window.iconbitmap(default=core.env.file.local.iconbitmap)
            self.window.iconbitmap(bitmap=core.env.file.local.iconbitmap)
        except Exception:
            ...

        self.label.bind("<Double-1>", self.bin_skin)
        windnd.hook_dropfiles(self.label, func=self.bin_drop)
        self.window.protocol('WM_DELETE_WINDOW', self.bin_close)


    def update_image(self, original_image: PIL.Image.Image):
        centre_width = original_image.width // 2 + SKEW_WIDTH
        centre_height = original_image.height // 2 + SKEW_HEIGHT

        left = centre_width - TARGET_WIDTH // 2
        top = centre_height - TARGET_HEIGHT // 2
        right = left + TARGET_WIDTH
        bottom = top + TARGET_HEIGHT

        image_new = original_image.crop((left, top, right, bottom))
        image_new.save(SAVE_TO)

        containe.image_tk = PIL.ImageTk.PhotoImage(image_new)
        self.label.config(image=containe.image_tk)


    def primary_treatment(self, image: PIL.Image.Image):
        left = (image.width - 1920) // 2
        top = image.height - left - 1080
        right = left + 1920
        bottom = top + 1080

        self.update_image(image.crop((left, top, right, bottom)))


    def bin_drop(self, items):
        item = items.pop()
        content = item.decode("gb18030")

        image = PIL.Image.open(content)
        self.primary_treatment(image)


    def bin_skin(self, *_):
        target_window = pygetwindow.getWindowsWithTitle('原神')[0]
        left, top, width, height = target_window.left, target_window.top, target_window.width, target_window.height
        screenshot = PIL.ImageGrab.grab(bbox=(left, top, left+width, top+height))

        self.update_image(screenshot)


    def bin_close(self, *_):
        containe.action.release()
        self.window.destroy()
