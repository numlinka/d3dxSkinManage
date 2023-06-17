# -*- coding: utf-8 -*-

import ttkbootstrap


class Operation(object):
    def __init__(self, master):
        self.master = master

        self.Notebook = ttkbootstrap.Notebook(self.master)
        self.Notebook.pack(fill='both', expand=True, padx=5, pady=(5, 0))

        self.Frame_modsManage = ttkbootstrap.Frame(self.Notebook)
        self.Notebook.add(self.Frame_modsManage, text='Mods 管理')

        self.Frame_d3dxManage = ttkbootstrap.Frame(self.Notebook)
        self.Notebook.add(self.Frame_d3dxManage, text='3DMiGoto')

        self.Frame_modsWarehouse = ttkbootstrap.Frame(self.Notebook)
        self.Notebook.add(self.Frame_modsWarehouse, text='Mods 仓库')

        self.Frame_about = ttkbootstrap.Frame(self.Notebook)
        self.Notebook.add(self.Frame_about, text='关于')
