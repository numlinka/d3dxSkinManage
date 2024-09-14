# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import datetime
import webbrowser

# site
import ttkbootstrap
from ttkbootstrap.constants import *

# local
import core

# self
from .about import About
from .mods_manage import ModsManage
from .d3dx_manage import D3dxManage
from .mods_warehouse import ModsWarehouse
from .tools import Tools
from .individuation import Individuation
from .plugins import Plugins


class Interface(object):
    def __init__(self, master):
        self.master = master

        self.notebook = ttkbootstrap.Notebook(self.master)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=(5, 0))

        self.frame_mods_manage = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_mods_manage, text='Mods 管理')

        self.frame_d3dx_manage = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_d3dx_manage, text='环境设置')

        self.frame_mods_warehouse = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_mods_warehouse, text='Mods 仓库')

        self.frame_tools = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_tools, text='工具')

        # self.frame_individuation = ttkbootstrap.Frame(self.notebook)
        # self.notebook.add(self.frame_individuation, text='个性化')

        self.frame_plugins = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_plugins, text='插件')

        self.frame_about = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_about, text='关于')

        self.mods_manage = ModsManage(self.frame_mods_manage)
        self.d3dx_manage = D3dxManage(self.frame_d3dx_manage)
        self.mods_warehouse = ModsWarehouse(self.frame_mods_warehouse)
        self.about = About(self.frame_about)
        self.tools = Tools(self.frame_tools)
        self.plugins = Plugins(self.frame_plugins)
        # self.individuation = Individuation(self.frame_individuation)

    def initial(self):
        self.mods_manage.initial()
        self.d3dx_manage.initial()
        # self.mods_warehouse.initial()


        try:
            # 在检测到系统版本变化时，设置起始页为关于页面
            uuid = core.env.uuid

            if uuid != core.env.configuration.uuid:
                self.notebook.select(5)
                core.env.configuration.uuid = uuid


            # 在检测到 30 天内未设置起始页为关于页面时，设置起始页为关于页面
            now_current_date = datetime.datetime.now()
            now_timestamp = int(now_current_date.timestamp())

            if not isinstance(core.env.configuration.last_launch_about_timestamp, int):
                core.env.configuration.last_launch_about_timestamp = 0

            if now_timestamp >= core.env.configuration.last_launch_about_timestamp + 2592000:
                self.notebook.select(5)
                core.env.configuration.last_launch_about_timestamp = now_timestamp


            # 在检测到版本变化时，设置起始页为关于页面
            if not isinstance(core.env.configuration.last_launch_version, int):
                core.env.configuration.last_launch_version = 0

            if core.env.VERSION_CODE != core.env.configuration.last_launch_version:
                self.notebook.select(5)
                core.env.configuration.last_launch_version = core.env.VERSION_CODE

        except Exception as _:
            ...


        try:
            if not core.env.is_admin:
                return
                ...

            self.w_admin = ttkbootstrap.Frame(self.master)
            self.w_admin_warn = ttkbootstrap.Label(self.w_admin, text="管理员运行可能会遇到的一些问题", bootstyle=WARNING)
            self.w_admin_detail = ttkbootstrap.Label(self.w_admin, text="[详情]", cursor="hand2")
            self.w_admin_close = ttkbootstrap.Label(self.w_admin, text="[关闭提醒]", cursor="hand2")

            self.w_admin.place(x=-10, y=5, relx=1.0, rely=0, anchor=NE)
            self.w_admin_warn.pack(side=LEFT)
            self.w_admin_close.pack(side=RIGHT)
            self.w_admin_detail.pack(side=RIGHT, padx=5)

            self.w_admin_detail.bind("<Button-1>", self.bin_about_admin_warn)
            self.w_admin_close.bind("<Button-1>", self.bin_close_admin_warn)

        except Exception as _:
            ...


    def bin_about_admin_warn(self, *_) -> None:
        webbrowser.open("https://d3dxskinmanage.numlinka.com/help/about-admin-rights")


    def bin_close_admin_warn(self, *_) -> None:
        self.w_admin.place_forget()
