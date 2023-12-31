# -*- coding: utf-8 -*-

import datetime
import subprocess

import ttkbootstrap

import core

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
        self.mods_warehouse.initial()


        try:
            # 在检测到系统版本变化时，设置起始页为关于页面
            result = subprocess.check_output("wmic csproduct get UUID", shell=True)
            uuid = result.decode("utf-8").replace("UUID", "").strip()

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
