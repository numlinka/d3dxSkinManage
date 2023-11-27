# -*- coding: utf-8 -*-

import webbrowser
import ttkbootstrap

import core
from constant import *

class About (object):
    def install(self, master):
        self.master = master

        self.frame = ttkbootstrap.Frame(self.master)
        self.frame.pack(side="top", fill="x", padx=10, pady=10)

        self.what_to_look_at = ttkbootstrap.Label(self.frame, text=T.TEXT_ADOUT)
        self.what_to_look_at.pack(side="left")

        self.frame_afdian = ttkbootstrap.Frame(self.master)
        self.frame_channel = ttkbootstrap.Frame(self.master)

        self.frame_afdian.pack(side="bottom", fill="x", padx=10, pady=10)
        self.frame_channel.pack(side="bottom", fill="x", padx=10, pady=(10, 0))


        self.label_sponsor = ttkbootstrap.Label(self.frame_afdian, text="赞助: ", font=("黑体", 16))
        self.label_afdian = ttkbootstrap.Label(self.frame_afdian, text=">> 爱发电 >>>", font=("黑体", 16), foreground="medium purple", cursor="hand2")

        self.label_sponsor.pack(side="left")
        self.label_afdian.pack(side="left")


        self.label_channel = ttkbootstrap.Label(self.frame_channel, text="频道: ", font=("黑体", 16))
        self.label_vocechat = ttkbootstrap.Label(self.frame_channel, text=">> 聊天室 >>>", font=("黑体", 16), foreground="deep sky blue", cursor="hand2")

        # self.label_channel.pack(side="left")
        # self.label_vocechat.pack(side="left")

        self.label_afdian.bind("<Button-1>", self.bin_open_afdian)
        self.label_vocechat.bind("<Button-1>", self.bin_open_vocechat)


    def __init__(self, master):
        self.master = master
        try: self.install(master)
        except Exception: ...


    def bin_open_afdian(self, *args):
        webbrowser.open(core.env.Link.afdian)


    def bin_open_vocechat(self, *args):
        webbrowser.open(core.env.Link.vocechat)
