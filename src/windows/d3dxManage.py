# -*- coding: utf-8 -*-

import os
import json
import shutil
import tkinter.filedialog

import win32api
import pywintypes
import ttkbootstrap

import core


class D3dxManage(object):
    def install(self, master):
        self.master = master

        BUTTON_WIDTH = 24

        self.LabelFrame_replace = ttkbootstrap.LabelFrame(master, text='3DMigoto 版本')
        self.LabelFrame_gamePath = ttkbootstrap.LabelFrame(master, text='游戏路径')


        self.LabelFrame_replace.pack(side='top', fill='x', padx=10, pady=10)
        self.LabelFrame_gamePath.pack(side='top', fill='x', padx=10, pady=(0, 10))
 
        self.Combobox_versions = ttkbootstrap.Combobox(self.LabelFrame_replace)
        self.Combobox_versions.pack(side='left', fill='x', expand=True, padx=10, pady=10)

        self.Button_d3dxstart = ttkbootstrap.Button(self.LabelFrame_replace, text='3DMiGoto 加载器', width=BUTTON_WIDTH, command=self.bin_launch_d3dx)
        self.Button_injection = ttkbootstrap.Button(self.LabelFrame_replace, text='一键启动', width=BUTTON_WIDTH, command=self.bin_onekey_launch)
        self.Button_injection.pack(side='left', padx=(0, 10), pady=10)
        self.Button_d3dxstart.pack(side='left', padx=(0, 10), pady=10)

        self.Entry_gamePath = ttkbootstrap.Entry(self.LabelFrame_gamePath)
        self.Entry_gamePath.pack(side='left', fill='x', expand=True, padx=10, pady=10)

        self.Button_filechoice = ttkbootstrap.Button(self.LabelFrame_gamePath, text='文件选择工具', width=BUTTON_WIDTH, command=self.bin_choice_file)
        self.Button_gamestart = ttkbootstrap.Button(self.LabelFrame_gamePath, text='启动游戏', width=BUTTON_WIDTH, command=self.bin_launch_game)
        self.Button_filechoice.pack(side='left', padx=(0, 10), pady=10)
        self.Button_gamestart.pack(side='left', padx=(0, 10), pady=10)

        self.Combobox_versions.bind('<FocusIn>', self.bin_selection_clear)
        self.Combobox_versions.bind('<<ComboboxSelected>>', self.bin_choice_version)

    def __init__(self, master):
        self.master = master
        self.install(master)


    def update(self):
        _GamePath = core.environment.user.object_configuration.GamePath
        if _GamePath is None: _GamePath = '< 未设置 >'
        self.sbin_update_game_path(_GamePath)
        d3dxs = core.environment.resources.d3dxs
        if os.path.isdir(d3dxs):
            dirlist = os.listdir(d3dxs)
            lst = [x for x in dirlist if os.path.isfile(os.path.join(d3dxs, x))]
            self.Combobox_versions.config(values=lst)
        try:
            with open(os.path.join(core.environment.user.work, f'd3dx_version_name_from_{core.environment.code_name}'), 'r', encoding='utf-8') as fileobject:
                version_name = fileobject.read()

            self.Combobox_versions.set(version_name)
        except Exception:
            ...


    def sbin_update_game_path(self, text):
        self.Entry_gamePath.delete(0, 'end')
        self.Entry_gamePath.insert(0, text)


    def bin_selection_clear(self, *args, **kwds):
        self.Combobox_versions.selection_clear()


    def bin_choice_version(self, *args, **kwds):
        version_name = self.Combobox_versions.get()
        self.bin_selection_clear()

        try:
            for name in os.listdir(core.environment.user.work):
                if name == 'Mods': continue
                path = os.path.join(core.environment.user.work, name)
                if os.path.isfile(path): os.remove(path)
                if os.path.isdir(path): shutil.rmtree(path)
        except Exception:
            ...

        core.External.x7z(os.path.join(core.environment.resources.d3dxs, version_name), core.environment.user.work)

        try:
            with open(os.path.join(core.environment.user.work, f'd3dx_version_name_from_{core.environment.code_name}'), 'w', encoding='utf-8') as fileobject:
                fileobject.write(version_name)
        except Exception:
            ...

        self.sbin_auto_set_d3dx_ini()


    def bin_launch_d3dx(self, *args, **kwds):
        schemepath = os.path.join(core.environment.user.work, 'scheme.json')
        if os.path.isfile(schemepath):
            try:
                with open(schemepath, 'r', encoding='utf-8') as fileobject:
                    filecontent = fileobject.read()
                    scheme = json.loads(filecontent)
                    launch_name = scheme['launch']
            except Exception:
                core.UI.Messagebox.showerror('scheme 数据解释失败\n请检查用户 work 目录或 d3dx 版本', title='数据错误')

        else:
            lst = os.listdir(core.environment.user.work)
            for name in ['3DMigotoLoader.exe', '3DMigoto Loader.exe']:
                if name in lst:
                    launch_name = name
                    break
            else:
                core.UI.Messagebox.showerror(title='检索错误', message='无法找到正确的方式启动 3DMigoto 加载器\n请检查用户 work 目录或 d3dx 版本')
                return

        launch_file = os.path.abspath(os.path.join(core.environment.user.work, launch_name))

        try:
            win32api.ShellExecute(None, 'open', launch_file, None, os.path.abspath(core.environment.user.work), 1)
        except pywintypes.error as e:
            core.UI.Messagebox.showerror(title='异常捕获', message=f'{e.args[1]}: {e.args[0]}\n{e.args[2]}')
        except Exception:
            core.UI.Messagebox.showerror(title='程序故障', message='无法找到正确的方式启动该程序')
            return 0


    def bin_onekey_launch(self, *args, **kwds):
        core.UI.Messagebox.showinfo(title='待开发功能', message='该功能暂未开发')


    def bin_choice_file(self, *args, **kdws):
        choice_PATH = tkinter.filedialog.askopenfilename(title='选择应用程序', filetypes=[('应用程序', '*.exe'), ('All Files', '*')])
        choice_PATH = choice_PATH.replace('/', '\\')
        if not choice_PATH: return None
        choice_NAME = os.path.basename(choice_PATH)

        if choice_NAME[choice_NAME.rfind('.'):] != '.exe':
            core.UI.Messagebox.showerror(title='错误的映像名', message='你选择了一个非 .exe 后缀名的文件\n请确认选择的是应用程序文件\n操作已被阻止')
            return

        elif choice_NAME == 'launcher.exe':
            core.UI.Messagebox.showwarning(title='意料之中的映像名', message='你似乎选择了 launcher.exe 文件\n通常情况下它是启动器程序而不是游戏启动程序')

        elif choice_NAME not in ['YuanShen.exe', 'GenshinImpact.exe', 'StarRail.exe']:
            core.UI.Messagebox.showwarning(title='意料之中的映像名', message='你选择的文件映像名不在白名单之中\n请确保它是游戏的启动程序\n\n- GenshinImpact.exe\n- YuanShen.exe\n- StarRail.exe')

        core.environment.user.object_configuration.GamePath = choice_PATH
        self.sbin_update_game_path(choice_PATH)
        self.sbin_auto_set_d3dx_ini()


    def bin_launch_game(self, *args, **kwds):
        path = core.environment.user.object_configuration.GamePath
        if path is None:
            core.UI.Messagebox.showerror(title='数据未设置', message='无法启动游戏\n未设置游戏路径')
        try:
            win32api.ShellExecute(None, 'open', path, None, os.path.realpath(os.path.dirname(path)), 1)
        except pywintypes.error as e:
            core.UI.Messagebox.showerror(title='异常捕获', message=f'{e.args[1]}: {e.args[0]}\n{e.args[2]}')
        except Exception:
            core.UI.Messagebox.showerror(title='程序故障', message='无法找到正确的方式启动该程序')
            return 0


    def sbin_auto_set_d3dx_ini(self):
        gamepath = core.environment.user.object_configuration.GamePath
        if gamepath is None: return
        schemepath = os.path.join(core.environment.user.work, 'scheme.json')
        if os.path.isfile(schemepath):
            try:
                with open(schemepath, 'r', encoding='utf-8') as fileobject:
                    filecontent = fileobject.read()
                    scheme = json.loads(filecontent)
                    if scheme['set-need'] is False: return
            except Exception:
                core.UI.Messagebox.showerror(title='数据错误', message='scheme 数据解释失败\n请检查用户 work 目录或 d3dx 版本')

        d3dxinipath = os.path.join(core.environment.user.work, 'd3dx.ini')
        if not os.path.isfile(d3dxinipath): return

        self.sbin_set_d3dx_ini(d3dxinipath, gamepath)


    def sbin_set_d3dx_ini(self, d3dxinipath, gamepath):
        try:
            with open(d3dxinipath, 'r', encoding='utf-8') as iF: iS = iF.read()
            with open(d3dxinipath, 'w', encoding='utf-8') as iF:
                iSL = iS.split('\n')
                for iD in range(len(iSL)):
                    iP = iSL[iD]
                    if iP[:6] == 'target':
                        iSL[iD] = 'target = ' + gamepath
                        break
                iS = '\n'.join(iSL)
                iF.write(iS)
        except Exception:
            core.UI.Messagebox.showerror(title='意料之外的错误', message='在修改 d3dx.ini 时出现了意料之外的错误')
