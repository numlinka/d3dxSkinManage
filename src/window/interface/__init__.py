# -*- coding: utf-8 -*-

import ttkbootstrap

from .about import About
from .mods_manage import ModsManage
from .d3dx_manage import D3dxManage
from .mods_warehouse import ModsWarehouse
from .tools import Tools


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

        self.frame_about = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_about, text='关于')

        self.frame_tools = ttkbootstrap.Frame(self.notebook)
        self.notebook.add(self.frame_tools, text='工具')

        self.mods_manage = ModsManage(self.frame_mods_manage)
        self.d3dx_manage = D3dxManage(self.frame_d3dx_manage)
        self.mods_warehouse = ModsWarehouse(self.frame_mods_warehouse)
        self.about = About(self.frame_about)
        self.tools = Tools(self.frame_tools)


    def initial(self):
        self.mods_manage.initial()
        self.d3dx_manage.initial()
        self.mods_warehouse.initial()