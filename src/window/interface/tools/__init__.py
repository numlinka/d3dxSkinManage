# -*- coding: utf-8 -*-


import ttkbootstrap

import core

from constant import *
from . import ocd_crop

TEXT = """
强迫症预览图裁剪工具

你是否因为在截取预览图时位置和大小参差不齐而烦恼
但是现在没有关系
这个工具可以帮助你截取位置和大小一致的图片
为你的强迫症之路舔砖 Java (加瓦)
"""


class Tools (object):
    def __init__(self, master, *_):
        self.master = master
        self.install()


    def install(self):
        self.frame = ttkbootstrap.Frame(self.master)
        self.frame.pack(side="top", fill="x", padx=10, pady=10)

        self.button_ocd_crop = ttkbootstrap.Button(self.frame, text=TEXT, bootstyle="outline", command=self.bin_open_ocd_crop)
        self.button_ocd_crop.pack(side="left")


    def initial(self):
        ...


    def bin_open_ocd_crop(self, *_):
        ocd_crop.OCDCrop()
