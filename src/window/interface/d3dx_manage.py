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

        BUTTON_WIDTH = 32

        self.labelframe_replace = ttkbootstrap.LabelFrame(master, text="3DMigoto 版本")
        self.labelframe_gamepath = ttkbootstrap.LabelFrame(master, text="游戏路径")


        self.labelframe_replace.pack(side="top", fill="x", padx=10, pady=10)
        self.labelframe_gamepath.pack(side="top", fill="x", padx=10, pady=(0, 10))
 
        self.combobox_versions = ttkbootstrap.Combobox(self.labelframe_replace, bootstyle="light")
        self.combobox_versions.pack(side="top", fill="x", expand=True, padx=10, pady=10)

        self.button_d3dxstart = ttkbootstrap.Button(self.labelframe_replace, text="启动 3DMiGoto 加载器", bootstyle="light-outline", width=BUTTON_WIDTH, command=self.bin_launch_d3dx)
        self.button_injection = ttkbootstrap.Button(self.labelframe_replace, text="一键启动", bootstyle="light-outline", width=BUTTON_WIDTH, command=self.bin_onekey_launch)
        self.button_open_work = ttkbootstrap.Button(self.labelframe_replace, text="打开工作目录", bootstyle="light-outline", width=BUTTON_WIDTH, command=self.bin_open_work)
        self.button_injection.pack(side="left", padx=(10, 10), pady=(0, 10))
        self.button_d3dxstart.pack(side="left", padx=(0, 10), pady=(0, 10))
        self.button_open_work.pack(side="left", padx=(0, 10), pady=(0, 10))

        self.entry_gamepath = ttkbootstrap.Entry(self.labelframe_gamepath, bootstyle="light")
        self.entry_gamepath.pack(side="top", fill="x", expand=True, padx=10, pady=10)

        self.button_filechoice = ttkbootstrap.Button(self.labelframe_gamepath, text="文件选择工具", bootstyle="light-outline", width=BUTTON_WIDTH, command=self.bin_choice_file)
        self.button_gamestart = ttkbootstrap.Button(self.labelframe_gamepath, text="启动游戏", bootstyle="light-outline", width=BUTTON_WIDTH, command=self.bin_launch_game)
        self.button_open_game = ttkbootstrap.Button(self.labelframe_gamepath, text="打开游戏目录", bootstyle="light-outline", width=BUTTON_WIDTH, command=self.bin_open_game)
        self.button_filechoice.pack(side="left", padx=(10, 10), pady=(0, 10))
        self.button_gamestart.pack(side="left", padx=(0, 10), pady=(0, 10))
        self.button_open_game.pack(side="left", padx=(0, 10), pady=(0, 10))

        self.combobox_versions.bind("<FocusIn>", self.bin_selection_clear)
        self.combobox_versions.bind("<<ComboboxSelected>>", self.bin_choice_version)


    def __init__(self, master):
        self.master = master
        self.install(master)


    def update(self):
        core.log.info("更新 d3dx 环境设置信息...")
        _GamePath = core.userenv.configuration.GamePath
        if _GamePath is None: _GamePath = "< 未设置 >"
        self.sbin_update_game_path(_GamePath)
        d3dxs = core.env.directory.resources.d3dxs
        if os.path.isdir(d3dxs):
            dirlist = os.listdir(d3dxs)
            lst = [x for x in dirlist if os.path.isfile(os.path.join(d3dxs, x))]
            self.combobox_versions.config(values=lst)

        try:
            with open(os.path.join(core.userenv.directory.work, f"d3dx_version_name_from_{core.env.CODE_NAME}"), "r", encoding="utf-8") as fileobject:
                version_name = fileobject.read()

            self.combobox_versions.set(version_name)

        except Exception:
            ...


    def sbin_update_game_path(self, text):
        self.entry_gamepath.delete(0, "end")
        self.entry_gamepath.insert(0, text)


    def bin_selection_clear(self, *args, **kwds):
        self.combobox_versions.selection_clear()


    def bin_choice_version(self, *args, **kwds):
        version_name = self.combobox_versions.get()
        self.bin_selection_clear()

        try:
            for name in os.listdir(core.userenv.directory.work):
                if name == "Mods": continue
                path = os.path.join(core.userenv.directory.work, name)
                if os.path.isfile(path): os.remove(path)
                if os.path.isdir(path): shutil.rmtree(path)
        except Exception:
            ...

        core.external.x7z(os.path.join(core.env.directory.resources.d3dxs, version_name), core.userenv.directory.work)

        try:
            with open(os.path.join(core.userenv.directory.work, f"d3dx_version_name_from_{core.env.CODE_NAME}"), "w", encoding="utf-8") as fileobject:
                fileobject.write(version_name)
        except Exception:
            ...

        self.sbin_auto_set_d3dx_ini()


    def bin_launch_d3dx(self, *args, **kwds):
        schemepath = os.path.join(core.userenv.directory.work, "scheme.json")
        if os.path.isfile(schemepath):
            try:
                with open(schemepath, "r", encoding="utf-8") as fileobject:
                    filecontent = fileobject.read()
                    scheme = json.loads(filecontent)
                    launch_name = scheme["launch"]
            except Exception:
                core.window.messagebox.showerror("scheme 数据解释失败\n请检查用户 work 目录或 d3dx 版本", title="数据错误")

        else:
            lst = os.listdir(core.userenv.directory.work)
            for name in ["3DMigotoLoader.exe", "3DMigoto Loader.exe"]:
                if name in lst:
                    launch_name = name
                    break
            else:
                core.window.messagebox.showerror(title="检索错误", message="无法找到正确的方式启动 3DMigoto 加载器\n请检查用户 work 目录或 d3dx 版本")
                return

        launch_file = os.path.abspath(os.path.join(core.userenv.directory.work, launch_name))

        try:
            win32api.ShellExecute(None, "runas", launch_file, None, os.path.abspath(core.userenv.directory.work), 1)
        except pywintypes.error as e:
            core.window.messagebox.showerror(title="异常捕获", message=f"{e.args[1]}: {e.args[0]}\n{e.args[2]}")
        except Exception:
            core.window.messagebox.showerror(title="程序故障", message="无法找到正确的方式启动该程序")
            return 0


    def bin_onekey_launch(self, *args, **kwds):
        core.window.messagebox.showinfo(title="成就：不信邪", message="都说过了这个玩意儿不能用")


    def bin_open_work(self, *args, **kwds):
        win32api.ShellExecute(None, "open", os.path.abspath(core.userenv.directory.work), None, os.path.abspath(core.userenv.directory.work), 1)


    def bin_open_game(self, *args, **kwds):
        path = core.userenv.configuration.GamePath
        if path is None:
            core.window.messagebox.showerror(title="数据未设置", message="无法打开游戏目录\n未设置游戏路径")
            return

        path = os.path.dirname(path)

        win32api.ShellExecute(None, "open", path, None, path, 1)


    def bin_choice_file(self, *args, **kdws):
        choice_PATH = tkinter.filedialog.askopenfilename(title="选择应用程序", filetypes=[("应用程序", "*.exe"), ("All Files", "*")])
        choice_PATH = choice_PATH.replace("/", "\\")
        if not choice_PATH: return None
        choice_NAME = os.path.basename(choice_PATH)

        if choice_NAME[choice_NAME.rfind("."):] != ".exe":
            core.window.messagebox.showerror(title="错误的映像名", message="你选择了一个非 .exe 后缀名的文件\n请确认选择的是应用程序文件\n操作已被阻止")
            return

        elif choice_NAME == "launcher.exe":
            core.window.messagebox.showwarning(title="意料之中的映像名", message="你似乎选择了 launcher.exe 文件\n通常情况下它是启动器程序而不是游戏启动程序")

        elif choice_NAME not in ["YuanShen.exe", "GenshinImpact.exe", "StarRail.exe"]:
            core.window.messagebox.showwarning(title="意料之中的映像名", message="你选择的文件映像名不在白名单之中\n请确保它是游戏的启动程序\n\n- GenshinImpact.exe\n- YuanShen.exe\n- StarRail.exe")

        core.userenv.configuration.GamePath = choice_PATH
        self.sbin_update_game_path(choice_PATH)
        self.sbin_auto_set_d3dx_ini()


    def bin_launch_game(self, *args, **kwds):
        path = core.userenv.configuration.GamePath
        if path is None:
            core.window.messagebox.showerror(title="数据未设置", message="无法启动游戏\n未设置游戏路径")
            return
        try:
            win32api.ShellExecute(None, "open", path, None, os.path.realpath(os.path.dirname(path)), 1)
        except pywintypes.error as e:
            core.window.messagebox.showerror(title="异常捕获", message=f"{e.args[1]}: {e.args[0]}\n{e.args[2]}")
        except Exception:
            core.window.messagebox.showerror(title="程序故障", message="无法找到正确的方式启动该程序")
            return


    def sbin_auto_set_d3dx_ini(self):
        gamepath = core.userenv.configuration.GamePath
        if gamepath is None: return
        schemepath = os.path.join(core.userenv.directory.work, "scheme.json")
        if os.path.isfile(schemepath):
            try:
                with open(schemepath, "r", encoding="utf-8") as fileobject:
                    filecontent = fileobject.read()
                    scheme = json.loads(filecontent)
                    if scheme["set-need"] is False: return
            except Exception:
                core.window.messagebox.showerror(title="数据错误", message="scheme 数据解释失败\n请检查用户 work 目录或 d3dx 版本")

        d3dxinipath = os.path.join(core.userenv.directory.work, "d3dx.ini")
        if not os.path.isfile(d3dxinipath): return

        self.sbin_set_d3dx_ini(d3dxinipath, gamepath)


    def sbin_set_d3dx_ini(self, d3dxinipath, gamepath):
        try:
            with open(d3dxinipath, "r", encoding="utf-8") as iF: iS = iF.read()
            with open(d3dxinipath, "w", encoding="utf-8") as iF:
                iSL = iS.split("\n")
                for iD in range(len(iSL)):
                    iP = iSL[iD]
                    if iP[:6] == "target":
                        iSL[iD] = "target = " + gamepath
                        break
                iS = "\n".join(iSL)
                iF.write(iS)
        except Exception:
            core.window.messagebox.showerror(title="意料之外的错误", message="在修改 d3dx.ini 时出现了意料之外的错误")
