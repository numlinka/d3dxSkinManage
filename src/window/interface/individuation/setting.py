# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# site
import ttkbootstrap


LOG_LEVEL = {
    "ALL": ~ 0x7F,
    "TRACE": ~ 0x40,
    "DEBUG": ~ 0x20,
    "INFO": 0x00,
    "WARN": 0x20,
    "SEVERE": 0x30,
    "ERROR": 0x40,
    "FATAL": 0x60,
    "OFF": 0x7F
}

ANNOTATION_LEVEL = {
    "全部": 3,
    "较多": 2,
    "较少": 1,
    "关闭": 0
}

class Setting (object):
    def __init__(self, master):
        self.master = master

        BUTTON_WIDTH = 20


        self.frame_theme = ttkbootstrap.Frame(self.master)
        self.label_theme = ttkbootstrap.Label(self.frame_theme, text="主题风格")
        self.combobox_theme = ttkbootstrap.Combobox(self.frame_theme)

        self.frame_theme.pack(side="top", fill="x", padx=10, pady=(10, 10))
        self.label_theme.pack(side="left", padx=(0, 5))
        self.combobox_theme.pack(side="right")

        self.frame_log_level = ttkbootstrap.Frame(self.master)
        self.label_log_level = ttkbootstrap.Label(self.frame_log_level, text="日志等级")
        self.combobox_log_level = ttkbootstrap.Combobox(self.frame_log_level, values=[x for x in LOG_LEVEL])

        self.frame_log_level.pack(side="top", fill="x", padx=10, pady=(0, 10))
        self.label_log_level.pack(side="left", padx=(0, 5))
        self.combobox_log_level.pack(side="right")

        self.frame_annotation_level = ttkbootstrap.Frame(self.master)
        self.label_annotation_level = ttkbootstrap.Label(self.frame_annotation_level, text="描述提示词数量")
        self.combobox_annotation_level = ttkbootstrap.Combobox(self.frame_annotation_level, values=[x for x in ANNOTATION_LEVEL])

        self.frame_annotation_level.pack(side="top", fill="x", padx=10, pady=(0, 10))
        self.label_annotation_level.pack(side="left", padx=(0, 5))
        self.combobox_annotation_level.pack(side="right")