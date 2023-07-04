# -*- coding: utf-8 -*-

import ttkbootstrap

import core



class FullScreenPreview (object):
    def __init__(self, tkimg):
        self.windows = ttkbootstrap.Toplevel()
        self.windows.attributes("-fullscreen", True)
        self.windows.attributes("-topmost", True)

        self.tkimg = tkimg

        self.Label_image = ttkbootstrap.Label(self.windows, anchor='center', cursor='plus', image=self.tkimg)
        self.Label_image.pack(side='top', fill='both', expand=True)

        self.Label_image.bind('<Button-1>', self.exit_)

    def exit_(self, *args):
        self.windows.destroy()


def full_screen_preview(*args):
    SHA = core.window.interface.mods_manage.label_SHA['text']
    width = core.window.mainwindow.winfo_screenwidth()
    height = core.window.mainwindow.winfo_screenheight()
    tkimg = core.module.image.get_full_screen_preview(SHA, width, height)
    if tkimg is None: return
    FullScreenPreview(tkimg)
