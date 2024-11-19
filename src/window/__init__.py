# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# site
import ttkbootstrap
from libs import dispatch
from ._inform import Inform

# local
import core
from constant import *

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


def main_window_position_save():
    core.env.configuration.main_window_position_x = mainwindow.winfo_x()
    core.env.configuration.main_window_position_y = mainwindow.winfo_y()
    core.env.configuration.main_window_position_width = mainwindow.winfo_width()
    core.env.configuration.main_window_position_height = mainwindow.winfo_height()


def main_window_position_load():
    x_ = core.env.configuration.main_window_position_x
    y_ = core.env.configuration.main_window_position_y
    width_ = core.env.configuration.main_window_position_width
    height_ = core.env.configuration.main_window_position_height

    try:
        if None not in (x_, y_, width_, height_):
            coordinates = methods.get_screen_coordinates()

            x1, x2 = x_, x_ + width_
            y1, y2 = y_, y_ + height_

            for screen in coordinates:
                if (screen[0][0] <= x1 <= x2 <= screen[1][0] and screen[0][1] <= y1 <= y2 <= screen[1][1]):
                    mainwindow.geometry(f"{width_}x{height_}+{x_}+{y_}")
                    return

    except Exception as _:
        ...

    _sw = mainwindow.winfo_screenwidth()
    _sh = mainwindow.winfo_screenheight()
    _w, _h = 1280, 800
    _w, _h = 1440, 900
    mainwindow.geometry(f"{_w}x{_h}+{(_sw - _w) // 2}+{(_sh - _h) // 2 - 40}")
    return


def initial():
    core.log.info("初始化主窗口...", L.WINDOW)

    style.theme_use(core.env.configuration.style_theme)
    core.env.configuration.win_scaling = _win_scaling = (
        mainwindow.winfo_fpixels("1i") / 96
    )
    style.configure("Treeview", rowheight=16 + int(32 * _win_scaling))

    mainwindow.title(core.env.MAIN_TITLE)
    main_window_position_load()
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
    core.action.askexit.add_task(main_window_position_save, 6_000, "保存窗口位置")



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
