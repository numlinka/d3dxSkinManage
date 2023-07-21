# -*- coding: utf-8 -*-


import ttkbootstrap

import core

from constant import *
from . import ocd_crop
from . import cache_cleanup

TEXT_OCD_CROP = """
强迫症预览图裁剪工具

你是否因为在截取预览图时位置和大小参差不齐而烦恼
但是现在没有关系
这个工具可以帮助你截取位置和大小一致的图片
为你的强迫症之路舔砖 Java (加瓦)
"""

TEXT_CACHE_CLEANUP = """
缓存清理工具

在 1.5 版本之后会大量使用缓存提高操作速度
但这些缓存不会因为 Mod 的删除而删除
可以通过此工具扫描并清理这些无用的缓存文件
释放硬盘空间
"""


class Tools (object):
    def __init__(self, master, *_):
        self.master = master
        self.install()


    def install(self):
        self.frame_1 = ttkbootstrap.Frame(self.master)
        self.frame_2 = ttkbootstrap.Frame(self.master)
        self.frame_1.pack(side="left", fill="y", padx=10, pady=10)
        self.frame_2.pack(side="left", fill="y", padx=(0, 10), pady=10)

        self.button_ocd_crop = ttkbootstrap.Button(self.frame_1, text=TEXT_OCD_CROP, bootstyle="outline", command=self.bin_open_ocd_crop)
        self.button_ocd_crop.pack(side="top")

        self.button_cache_cleanup = ttkbootstrap.Button(self.frame_2, text=TEXT_CACHE_CLEANUP, bootstyle="outline", command=self.bin_open_cache_cleanup)
        self.button_cache_cleanup.pack(side="top")


    def initial(self):
        ...


    def bin_open_ocd_crop(self, *_):
        ocd_crop.OCDCrop()


    def bin_open_cache_cleanup(self, *_):
        cache_cleanup.CacheCleanup()
