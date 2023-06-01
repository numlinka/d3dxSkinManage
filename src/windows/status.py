# -*- coding: utf-8 -*-


import webbrowser
import ttkbootstrap

import windows
import core



class Status(object):
    def __init__(self, master):
        self.master = master

        self.Label_userName = ttkbootstrap.Label(self.master, text='* /')
        self.Label_mark = ttkbootstrap.Label(self.master, text='[S]')
        self.Label_status = ttkbootstrap.Label(self.master, text='-')
        self.Progressbar_step = ttkbootstrap.Progressbar(self.master)

        self.Label_userName.pack(side='left', padx=5, pady=5)
        self.Label_mark.pack(side='left', padx=5, pady=5)
        self.Label_status.pack(side='left', padx=5, pady=5)
        self.Progressbar_step.pack(side='left', padx=5, pady=5)

        # self.Label_logout = ttkbootstrap.Label(self.master, text='[ 注销 ]', foreground='#00FFFF', cursor='hand2')
        # self.Label_logout.pack(side='right', padx=10, pady=5 )

        self.Label_help = ttkbootstrap.Label(self.master, text='[ 帮助 ]', cursor='hand2')
        self.Label_help.pack(side='right', padx=10, pady=5 )

        # self.Label_logout.bind('<Button-1>', self.bin_logout)
        self.Label_help.bind('<Button-1>', self.bin_open_help)


    def bin_logout(self, *args):
        windows.Messagebox.showinfo
        # a = tkinter.messagebox.askokcancel("实际上这个控件并没有什么用\n倒是可以点着玩儿", "未定义事件")


    def bin_open_help(self, *args):
        webbrowser.open(core.environment.link.help)


    def set_userName(self, userName):
        self.Label_userName['text'] = f'* {userName}'


    def set_mark(self, mark):
        self.Label_mark['text'] = f'[{mark}]'


    def set_status(self, status, LEVEL: int = 0):
        if not isinstance(LEVEL, int): LEVEL = 0
        color = ['', 'red', 'orange'][LEVEL]
        self.Label_status['text'] = status
        self.Label_status['foreground'] = color
