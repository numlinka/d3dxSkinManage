# -*- coding: utf-8 -*-

# * domain: windows

import ttkbootstrap

import core


from . import messagebox
from . import status
from . import login
from . import operation
from . import modsManage
from . import d3dxManage
from . import modsWarehouse
from . import about

Windows = ttkbootstrap.Window()

Messagebox = messagebox.Messagebox(Windows)

FrameStauts = ttkbootstrap.Frame(Windows)
FrameMessage = ttkbootstrap.Frame(Windows)
FrameLogin = ttkbootstrap.Frame(Windows)
FrameOperation = ttkbootstrap.Frame(Windows)

LabelMessage = ttkbootstrap.Label(FrameMessage)

Status = status.Status(FrameStauts)
Login = login.Login(FrameLogin)
Operation = operation.Operation(FrameOperation)

ModsManage = modsManage.ModsManage(Operation.Frame_modsManage)
D3dxManage = d3dxManage.D3dxManage(Operation.Frame_d3dxManage)
ModsWarehouse = modsWarehouse.ModsWarehouse(Operation.Frame_modsWarehouse)
About = about.About(Operation.Frame_about)

try:
    Windows.iconbitmap(default=core.environment.local.iconbitmap)
    Windows.iconbitmap(bitmap=core.environment.local.iconbitmap)
except Exception:
    ...


class con(object):
    @classmethod
    def login(cls, userName):
        FrameLogin.pack_forget()
        FrameOperation.pack(side='top', fill='both', expand=True)
        Status.set_userName(userName)

        # ModsManage.bin_refresh() # ? 为时尚早


    @classmethod
    def logout(cls):
        ...


def initial():
    ttkbootstrap.Style(theme='darkly')

    style = ttkbootstrap.Style()
    style.configure('Treeview', rowheight=48)

    Windows.title(core.environment.title)
    _sw = Windows.winfo_screenwidth()
    _sh = Windows.winfo_screenheight()
    _w, _h = 1280, 800
    Windows.geometry(f'{_w}x{_h}+{(_sw - _w) // 2}+{(_sh - _h) // 2 - 40}')
    Windows.minsize(960, 600)

    FrameStauts.pack(side='bottom', fill='x')
    FrameMessage.pack(side='top', fill='both', expand=True)
    LabelMessage.pack(side='top', fill='both', padx=20, pady=20)

    Login.initial()
    core.additional.initial()
    # windnd.hook_dropfiles(Windows, func=core.additional.hook_dropfiles)


def ready():
    FrameMessage.pack_forget()
    FrameLogin.pack(side='top', fill='both', expand=True)
