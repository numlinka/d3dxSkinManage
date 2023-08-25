
import ttkbootstrap

from .dreplace import DReplace
from .gamepath import GanePath
from .custom import Custom
# from .setting import Setting

class Individuation (object):
    def __init__(self, master):
        self.master = master

        BUTTON_WIDTH = 2000

        layout: int = 3

        if layout == 1:
            self.frame_top = ttkbootstrap.Frame(self.master)
            self.frame_bottom = ttkbootstrap.Frame(self.master)
            self.frame_top.pack(side="top", fill="both", expand=True)
            self.frame_bottom.pack(side="bottom", fill="both", expand=True)

            self.labelframe_replace = ttkbootstrap.LabelFrame(self.frame_top, text="3DMigoto 版本")
            self.labelframe_gamepath = ttkbootstrap.LabelFrame(self.frame_top, text="游戏路径")
            self.labelframe_custom = ttkbootstrap.LabelFrame(self.frame_bottom, text="自定义启动项")
            self.labelframe_setting = ttkbootstrap.LabelFrame(self.frame_bottom, text="预留空位")

            self.labelframe_replace.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=(10, 5))
            self.labelframe_gamepath.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=(10, 5))
            self.labelframe_custom.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=(5, 10))
            self.labelframe_setting.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=(5, 10))

        elif layout == 2:
            self.frame_left = ttkbootstrap.Frame(self.master, width=BUTTON_WIDTH)
            self.frame_right = ttkbootstrap.Frame(self.master, width=BUTTON_WIDTH)
            self.frame_left.pack(side="left", fill="both", expand=True)
            self.frame_right.pack(side="right", fill="both", expand=True)

            self.labelframe_replace = ttkbootstrap.LabelFrame(self.frame_left, text="3DMigoto 版本", height=BUTTON_WIDTH)
            self.labelframe_gamepath = ttkbootstrap.LabelFrame(self.frame_right, text="游戏路径", height=BUTTON_WIDTH)
            self.labelframe_custom = ttkbootstrap.LabelFrame(self.frame_left, text="自定义启动项", height=BUTTON_WIDTH)
            self.labelframe_setting = ttkbootstrap.LabelFrame(self.frame_right, text="预留空位", height=BUTTON_WIDTH)

            self.labelframe_replace.pack(side="top", fill="both", expand=True, padx=(10, 5), pady=(10, 5))
            self.labelframe_gamepath.pack(side="top", fill="both", expand=True, padx=(5, 10), pady=(10, 5))
            self.labelframe_custom.pack(side="bottom", fill="both", expand=True, padx=(10, 5), pady=(5, 10))
            self.labelframe_setting.pack(side="bottom", fill="both", expand=True, padx=(5, 10), pady=(5, 10))

        elif layout == 3:
            self.frame_replace = ttkbootstrap.Frame(self.master)
            self.frame_gamepath = ttkbootstrap.Frame(self.master)
            self.frame_custom = ttkbootstrap.Frame(self.master)
            self.frame_setting = ttkbootstrap.Frame(self.master)

            self.labelframe_replace = ttkbootstrap.LabelFrame(self.frame_replace, text="3DMigoto 版本")
            self.labelframe_gamepath = ttkbootstrap.LabelFrame(self.frame_gamepath, text="游戏路径")
            self.labelframe_custom = ttkbootstrap.LabelFrame(self.frame_custom, text="自定义启动项")
            self.labelframe_setting = ttkbootstrap.LabelFrame(self.frame_setting, text="预留空位")

            self.master.grid_rowconfigure(0, weight=1)
            self.master.grid_columnconfigure(0, weight=1)
            self.master.grid_rowconfigure(1, weight=1)
            self.master.grid_columnconfigure(1, weight=1)

            self.frame_replace.grid(column=0, row=0, padx=(10, 5), pady=(10, 5), sticky="nsew")
            self.frame_gamepath.grid(column=1, row=0, padx=(5, 10), pady=(10, 5), sticky="nsew")
            self.frame_custom.grid(column=0, row=1, padx=(10, 5), pady=(5, 10), sticky="nsew")
            self.frame_setting.grid(column=1, row=1, padx=(5, 10), pady=(5, 10), sticky="nsew")

            self.labelframe_replace.pack(fill="both", expand=True)
            self.labelframe_gamepath.pack(fill="both", expand=True)
            self.labelframe_custom.pack(fill="both", expand=True)
            self.labelframe_setting.pack(fill="both", expand=True)

        self.dreplace = DReplace(self.labelframe_replace)
        self.gamepath = GanePath(self.labelframe_gamepath)
        self.custom = Custom(self.labelframe_custom)
        # self.setting = Setting(self.labelframe_setting)
