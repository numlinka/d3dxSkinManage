# -*- coding: utf-8 -*-

import webbrowser
import ttkbootstrap

import core

class About (object):
    def install(self, master):
        self.master = master

        self.Frame = ttkbootstrap.Frame(self.master)
        self.Frame.pack(side='top', fill='x', padx=10, pady=10)

        self.d = ttkbootstrap.Label(self.Frame, text='看什么看')
        self.d.pack(side='left')

        self.Frame_afdian = ttkbootstrap.Frame(self.master)
        self.Frame_channel = ttkbootstrap.Frame(self.master)

        self.Frame_afdian.pack(side='bottom', fill='x', padx=10, pady=10)
        self.Frame_channel.pack(side='bottom', fill='x', padx=10, pady=(10, 0))


        self.Label_sponsor = ttkbootstrap.Label(self.Frame_afdian, text='赞助: ', font=('黑体', 16))
        self.Label_afdian = ttkbootstrap.Label(self.Frame_afdian, text='>> 爱发电 >>>', font=('黑体', 16), foreground='medium purple', cursor='hand2')

        self.Label_sponsor.pack(side='left')
        self.Label_afdian.pack(side='left')


        self.Label_channel = ttkbootstrap.Label(self.Frame_channel, text='频道: ', font=('黑体', 16))
        self.Label_vocechat = ttkbootstrap.Label(self.Frame_channel, text='>> 聊天室 >>>', font=('黑体', 16), foreground='deep sky blue', cursor='hand2')

        self.Label_channel.pack(side='left')
        self.Label_vocechat.pack(side='left')

        self.Label_afdian.bind('<Button-1>', self.bin_open_afdian)
        self.Label_vocechat.bind('<Button-1>', self.bin_open_vocechat)


    def __init__(self, master):
        self.master = master
        try: self.install(master)
        except Exception: ...


    def bin_open_afdian(self, *args):
        webbrowser.open(core.environment.link.afdian)


    def bin_open_vocechat(self, *args):
        webbrowser.open(core.environment.link.vocechat)
