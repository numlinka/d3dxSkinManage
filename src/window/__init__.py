# -*- coding: utf-8 -*-

# libs
import ttkbootstrap
# import tkinterdnd2

# self
from .messagebox import Messagebox
from .title import Title
from .status import Status
from .login import Login
from .block import Block
from .interface import Interface
from .annotation_toplevel import AnnotationToplevel

from constant import *

import core


mainwindow = ttkbootstrap.Window()
# mainwindow = tkinterdnd2.TkinterDnD.Tk()
# mainwindow.overrideredirect(True)
messagebox = Messagebox(mainwindow)
annotation_toplevel = AnnotationToplevel()

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


def initial():
    core.log.info("初始化主窗口...", L.WINDOW)
    ttkbootstrap.Style(theme="darkly")

    style = ttkbootstrap.Style()
    style.configure("Treeview", rowheight=48)

    mainwindow.title(core.env.MAIN_TITLE)
    _sw = mainwindow.winfo_screenwidth()
    _sh = mainwindow.winfo_screenheight()
    _w, _h = 1280, 800
    _w, _h = 1440, 900
    mainwindow.geometry(f"{_w}x{_h}+{(_sw - _w) // 2}+{(_sh - _h) // 2 - 40}")
    mainwindow.minsize(960, 600)

    try:
        mainwindow.iconbitmap(default=core.env.file.local.iconbitmap)
        mainwindow.iconbitmap(bitmap=core.env.file.local.iconbitmap)

    except Exception as e:
        core.log.error(f"窗口图标设置异常", L.WINDOW)

    frame_title.pack(side="top", fill="x")
    frame_block.pack(side="top", fill="both", expand=True)
    frame_status.pack(side="bottom", fill="x")

    _alt_set = annotation_toplevel.register
    _alt_set(login.label_description, T.ANNOTATION_USER_DESCRIPTION)
    _alt_set(login.button_login, T.ANNOTATION_LOGIN)
    _alt_set(status.label_help, T.ANNOTATION_HELP)

    _alt_set(interface.d3dx_manage.combobox_versions, T.ANNOTATION_D3DX_VERSION)
    _alt_set(interface.d3dx_manage.button_injection, T.ANNOTATION_D3DX_INJECTION)
    _alt_set(interface.d3dx_manage.button_d3dxstart, T.ANNOTATION_D3DX_START)
    _alt_set(interface.d3dx_manage.button_open_work, T.ANNOTATION_D3DX_OPEN_WORK_DIR)
    _alt_set(interface.d3dx_manage.entry_gamepath, T.ANNOTATION_D3DX_SET_GAME_PATH)
    _alt_set(interface.d3dx_manage.button_filechoice, T.ANNOTATION_D3DX_SET_GAME_PATH)
    _alt_set(interface.d3dx_manage.button_gamestart, T.ANNOTATION_D3DX_START)
    _alt_set(interface.d3dx_manage.button_open_game, T.ANNOTATION_D3DX_GAME_WORK_DIR)

    _alt_set(interface.mods_warehouse.Entry_search, T.ANNOTATION_WAREHOUSE_SEARCH)
    _alt_set(interface.mods_warehouse.Button_download, T.ANNOTATION_WAREHOUSE_DOWNLOAD)
    _alt_set(interface.mods_warehouse.Button_open_url, T.ANNOTATION_WAREHOUSE_OPEN_URL)


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
