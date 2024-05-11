# -*- coding: utf-8 -*-

# libs
import ttkbootstrap
# import tkinterdnd2
from libs import dispatch

# self
from . import methods
from . import _title_content
from .messagebox import Messagebox
from .title import Title
from .status import Status
from .login import Login
from .block import Block
from .interface import Interface
from .annotation_toplevel import AnnotationToplevel
from ._inform import Inform

from constant import *

import core


mainwindow = ttkbootstrap.Window()
# mainwindow = tkinterdnd2.TkinterDnD.Tk()
# mainwindow.overrideredirect(True)
messagebox = Messagebox(mainwindow)
annotation_toplevel = AnnotationToplevel()
dispatch.settings.tk_mainwindow = mainwindow
inform = Inform()

treeview_thumbnail = core.module.image.ImageTkThumbnailGroup(40, 40)

frame_title = ttkbootstrap.Frame(mainwindow)
frame_status = ttkbootstrap.Frame(mainwindow)
frame_login = ttkbootstrap.Frame(mainwindow)
frame_block = ttkbootstrap.Frame(mainwindow)
frame_notebook = ttkbootstrap.Frame(mainwindow)


# title = Title(frame_title)
status = Status(frame_status)
login = Login(frame_login)
block = Block(frame_block)
interface = Interface(frame_notebook)

style = ttkbootstrap.Style()
style_theme_names = style.theme_names()


def initial():
    core.log.info("初始化主窗口...", L.WINDOW)

    style.theme_use(core.env.configuration.style_theme)
    style.configure("Treeview", rowheight=48)

    mainwindow.title(core.env.MAIN_TITLE)
    _sw = mainwindow.winfo_screenwidth()
    _sh = mainwindow.winfo_screenheight()
    _w, _h = 1280, 800
    _w, _h = 1440, 900
    mainwindow.geometry(f"{_w}x{_h}+{(_sw - _w) // 2}+{(_sh - _h) // 2 - 40}")
    mainwindow.minsize(960, 600)
    core.action.askexit.add_task(mainwindow.destroy, 10_000, "关闭窗口")
    mainwindow.protocol("WM_DELETE_WINDOW", core.action.askexit.execute)

    try:
        mainwindow.iconbitmap(default=core.env.file.local.iconbitmap)
        mainwindow.iconbitmap(bitmap=core.env.file.local.iconbitmap)

    except Exception as e:
        core.log.error(f"窗口图标设置异常", L.WINDOW)

    frame_title.pack(side="top", fill="x")
    frame_block.pack(side="top", fill="both", expand=True)
    frame_status.pack(side="bottom", fill="x")

    _alt_set = annotation_toplevel.register
    _alt_set(login.label_description, T.ANNOTATION_USER_DESCRIPTION, 2)
    _alt_set(login.button_login, T.ANNOTATION_LOGIN, 1)
    _alt_set(status.label_help, T.ANNOTATION_HELP, 1)
    interface.initial()
    _title_content.initial()



def ready_login():
    core.log.info("就绪", L.WINDOW)
    frame_block.pack_forget()
    frame_block.pack_forget()
    frame_login.pack(side="top", fill="both", expand=True)


def _login(__name):
    core.log.info("登录用户界面...", L.WINDOW)
    frame_login.pack_forget()
    frame_notebook.pack(side='top', fill='both', expand=True)
    status.set_userName(__name)


def auto_login_check():
    try:
        username = core.argv.autologin
        if not username: return
        core.login(username)

    except Exception as _:
        ...
