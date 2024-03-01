# -*- coding: utf-8 -*-

import os
import json
import shutil
import tkinter.filedialog

import win32api
import win32gui
import pywintypes
import ttkbootstrap

import core
from constant import *


LOG_LEVEL = {
    "ALL": ~ 0x7F,
    "TRACE": ~ 0x40,
    "DEBUG": ~ 0x20,
    "INFO": 0x00,
    "WARN": 0x20,
    "SEVERE": 0x30,
    "ERROR": 0x40,
    "FATAL": 0x60,
    "OFF": 0x7F
}

ANNOTATION_LEVEL = {
    "全部": 3,
    "较多": 2,
    "较少": 1,
    "关闭": 0
}


end = "end"
APPROXIMATE_MATCH = ["key-in only", "similarity only", "similarity threshold", "similarity/key-in"]




class UnityArgs (object):
    def __init__ (self, *_):
        self.window = ttkbootstrap.Toplevel("Unity 通用参数设置")
        self.window.transient(core.window.mainwindow)
        self.window.grab_set()

        self.window.resizable(False, False)

        try:
            self.window.iconbitmap(default=core.env.file.local.iconbitmap)
            self.window.iconbitmap(bitmap=core.env.file.local.iconbitmap)

        except Exception:
            ...

        SKL = "w"
        SKB = "ew"
        WIDTH = 30

        self.vs_popupwindow = ["False", "True"]
        self.vs_fullscreen = ["不设置", "0", "1"]
        self.vn_width = 300
        self.vx_width = self.window.winfo_screenwidth()
        self.vn_height = 200
        self.vx_height = self.window.winfo_screenheight()

        self.wfe_args = ttkbootstrap.Frame(self.window)
        self.wfe_args.pack(side="top", fill="x")

        self.wll_popupwindow = ttkbootstrap.Label(self.wfe_args, text="无边框窗口")
        self.wll_fullscreen = ttkbootstrap.Label(self.wfe_args, text="全屏运行")
        self.wll_screen_width = ttkbootstrap.Label(self.wfe_args, text="窗口宽度")
        self.wll_screen_height = ttkbootstrap.Label(self.wfe_args, text="窗口高度")

        self.wcb_popupwindow = ttkbootstrap.Combobox(self.wfe_args, values=self.vs_popupwindow, width=WIDTH)
        self.wcb_fullscreen = ttkbootstrap.Combobox(self.wfe_args, values=self.vs_fullscreen, width=WIDTH)
        self.wsb_screen_width = ttkbootstrap.Spinbox(self.wfe_args, from_=self.vn_width, to=self.vx_width, width=WIDTH)
        self.wsb_screen_height = ttkbootstrap.Spinbox(self.wfe_args, from_=self.vn_height, to=self.vx_height, width=WIDTH)

        self.wll_popupwindow.grid(row=0, column=0, pady=10, padx=10, sticky=SKL)
        self.wll_fullscreen.grid(row=1, column=0, pady=(0, 10), padx=10, sticky=SKL)
        self.wll_screen_width.grid(row=2, column=0, pady=(0, 10), padx=10, sticky=SKL)
        self.wll_screen_height.grid(row=3, column=0, pady=(0, 10), padx=10, sticky=SKL)

        self.wcb_popupwindow.grid(row=0, column=1, pady=10, padx=10, sticky=SKB)
        self.wcb_fullscreen.grid(row=1, column=1, pady=(0, 10), padx=10, sticky=SKB)
        self.wsb_screen_width.grid(row=2, column=1, pady=(0, 10), padx=10, sticky=SKB)
        self.wsb_screen_height.grid(row=3, column=1, pady=(0, 10), padx=10, sticky=SKB)

        self.wbn_ok = ttkbootstrap.Button(self.window, text="确定", width=10, bootstyle="success-outline", command=self.bin_ok)
        self.wbn_ok.pack(side="right", padx=10, pady=(0, 10))

        core.window.mainwindow.update()

        width = self.window.winfo_width()
        height = self.window.winfo_height()

        _x, _y = win32gui.GetCursorInfo()[2]

        x = _x - width // 2
        y = _y - height // 2 - 20

        if x < 0: x = 0
        if y < 0: y = 0

        self.window.geometry(f'+{x}+{y}')


    def bin_ok(self, *_):
        arguments = []

        v_pw = self.wcb_popupwindow.get().strip()
        v_fs = self.wcb_fullscreen.get().strip()
        v_sw = self.wsb_screen_width.get().strip()
        v_sh = self.wsb_screen_height.get().strip()

        if v_pw in ["True", "true", "TRUE", "1"]: arguments.append("-popupwindow")
        if v_fs in ["True", "true", "TRUE", "1"]: arguments.append("-screen-fullscreen 1")
        elif v_fs in ["False", "false", "FALSE", "0"]: arguments.append("-screen-fullscreen 0")

        try:
            value = int(v_sw)
            if value <= 300:
                v_sw = "300"
            arguments.append(f"-screen-width {v_sw}")

        except Exception:
            ...

        try:
            value = int(v_sh)
            if value <= 200:
                v_sh = "200"
            arguments.append(f"-screen-height {v_sh}")

        except Exception:
            ...

        texts = " ".join(arguments)
        core.window.interface.d3dx_manage.entry_game_argument.delete(0, "end")
        core.window.interface.d3dx_manage.entry_game_argument.insert(0, texts)

        self.window.destroy()



class D3dxManage(object):
    def install(self, master):
        self.master = master
        self.style = ttkbootstrap.Style()

        BUTTON_WIDTH = 36 # 24

        self.labelframe_global = ttkbootstrap.LabelFrame(self.master, text="全局设置")
        self.labelframe_userenv = ttkbootstrap.LabelFrame(self.master, text="用户设置")

        self.labelframe_global.pack(side="left", fill="both", padx=10, pady=10, expand=True)
        self.labelframe_userenv.pack(side="left", fill="both", padx=(0, 10), pady=10, expand=True)
        # self.labelframe_global.grid_columnconfigure(0, weight=0)
        self.labelframe_global.grid_columnconfigure(1, weight=1)

        STICKY_KEY = "e"
        STICKY_VALUE = "ew"


        # self.frame_theme = ttkbootstrap.Frame(self.labelframe_global)
        # self.label_theme = ttkbootstrap.Label(self.frame_theme, text="主题风格")
        # self.combobox_theme = ttkbootstrap.Combobox(self.frame_theme)

        self.label_theme = ttkbootstrap.Label(self.labelframe_global, text="主题风格")
        self.combobox_theme = ttkbootstrap.Combobox(self.labelframe_global)

        # self.frame_theme.pack(side="top", fill="x", padx=10, pady=(10, 10))
        # self.label_theme.pack(side="left", padx=(0, 5))
        # self.combobox_theme.pack(side="right")

        self.label_theme.grid(row=0, column=0, pady=10, padx=10, sticky=STICKY_KEY)
        self.combobox_theme.grid(row=0, column=1, pady=10, padx=(0, 10), sticky=STICKY_VALUE)

        # self.frame_log_level = ttkbootstrap.Frame(self.labelframe_global)
        # self.label_log_level = ttkbootstrap.Label(self.frame_log_level, text="日志等级")
        # self.combobox_log_level = ttkbootstrap.Combobox(self.frame_log_level, values=[x for x in LOG_LEVEL])

        self.label_log_level = ttkbootstrap.Label(self.labelframe_global, text="日志等级")
        self.combobox_log_level = ttkbootstrap.Combobox(self.labelframe_global, values=[x for x in LOG_LEVEL])

        # self.frame_log_level.pack(side="top", fill="x", padx=10, pady=(0, 10))
        # self.label_log_level.pack(side="left", padx=(0, 5))
        # self.combobox_log_level.pack(side="right")

        self.label_log_level.grid(row=1, column=0, pady=(0, 10), padx=10, sticky=STICKY_KEY)
        self.combobox_log_level.grid(row=1, column=1, pady=(0, 10), padx=(0, 10), sticky=STICKY_VALUE)

        # self.frame_annotation_level = ttkbootstrap.Frame(self.labelframe_global)
        # self.label_annotation_level = ttkbootstrap.Label(self.frame_annotation_level, text="描述提示词数量")
        # self.combobox_annotation_level = ttkbootstrap.Combobox(self.frame_annotation_level, values=[x for x in ANNOTATION_LEVEL])

        self.label_annotation_level = ttkbootstrap.Label(self.labelframe_global, text="描述提示词数量")
        self.combobox_annotation_level = ttkbootstrap.Combobox(self.labelframe_global, values=[x for x in ANNOTATION_LEVEL])

        # self.frame_annotation_level.pack(side="top", fill="x", padx=10, pady=(0, 10))
        # self.label_annotation_level.pack(side="left", padx=(0, 5))
        # self.combobox_annotation_level.pack(side="right")

        self.label_annotation_level.grid(row=2, column=0, pady=(0, 10), padx=10, sticky=STICKY_KEY)
        self.combobox_annotation_level.grid(row=2, column=1, pady=(0, 10), padx=(0, 10), sticky=STICKY_VALUE)

        # self.frame_approximate = ttkbootstrap.Frame(self.labelframe_global)
        # self.label_approximate = ttkbootstrap.Label(self.frame_approximate, text="头像匹配算法", width=50)
        # self.combobox_approximate = ttkbootstrap.Combobox(self.frame_approximate, values=APPROXIMATE_MATCH)

        self.label_approximate = ttkbootstrap.Label(self.labelframe_global, text="头像名称匹配算法")
        self.combobox_approximate = ttkbootstrap.Combobox(self.labelframe_global, values=APPROXIMATE_MATCH)

        # self.frame_approximate.pack(side="top", fill="x", padx=10, pady=(0, 10))
        # self.label_approximate.pack(side="left", padx=(0, 5))
        # self.combobox_approximate.pack(side="right")

        self.label_approximate.grid(row=3, column=0, pady=(0, 10), padx=10, sticky=STICKY_KEY)
        self.combobox_approximate.grid(row=3, column=1, pady=(0, 10), padx=(0, 10), sticky=STICKY_VALUE)



        self.labelframe_replace = ttkbootstrap.LabelFrame(self.labelframe_userenv, text="3DMigoto 版本")
        self.labelframe_gamepath = ttkbootstrap.LabelFrame(self.labelframe_userenv, text="游戏路径")
        self.labelframe_custom = ttkbootstrap.LabelFrame(self.labelframe_userenv, text="自定义启动项")

        self.labelframe_replace.pack(side="top", fill="x", padx=10, pady=10)
        self.labelframe_gamepath.pack(side="top", fill="x", padx=10, pady=(0, 10))
        self.labelframe_custom.pack(side="top", fill="x", padx=10, pady=(0, 10))
 
        self.combobox_versions = ttkbootstrap.Combobox(self.labelframe_replace)#, bootstyle="light")
        self.combobox_versions.pack(side="top", fill="x", expand=True, padx=10, pady=10)

        self.button_d3dxstart = ttkbootstrap.Button(self.labelframe_replace, text="启动加载器", bootstyle="outline", width=BUTTON_WIDTH, command=self.bin_launch_d3dx)
        self.button_injection = ttkbootstrap.Button(self.labelframe_replace, text="一键启动", bootstyle="outline", width=BUTTON_WIDTH, command=self.bin_onekey_launch)
        self.button_open_work = ttkbootstrap.Button(self.labelframe_replace, text="打开工作目录", bootstyle="outline", width=BUTTON_WIDTH, command=self.bin_open_work)
        self.button_injection.pack(side="left", padx=(10, 10), pady=(0, 10), fill="x", expand=True)
        self.button_d3dxstart.pack(side="left", padx=(0, 10), pady=(0, 10), fill="x", expand=True)
        self.button_open_work.pack(side="left", padx=(0, 10), pady=(0, 10), fill="x", expand=True)

        self.entry_gamepath = ttkbootstrap.Entry(self.labelframe_gamepath)#, bootstyle="light")
        self.wfe_game_args = ttkbootstrap.Frame(self.labelframe_gamepath)
        self.entry_game_argument = ttkbootstrap.Entry(self.wfe_game_args)#, bootstyle="light")
        self.wbn_unity_args = ttkbootstrap.Button(self.wfe_game_args, text="+", command=UnityArgs)
        self.entry_gamepath.pack(side="top", fill="x", expand=True, padx=10, pady=10)
        self.wfe_game_args.pack(side="top", fill="x", expand=True, padx=10, pady=(0, 10))
        self.entry_game_argument.pack(side="left", fill="x", expand=True)
        self.wbn_unity_args.pack(side="left", padx=(5, 0))

        self.button_filechoice = ttkbootstrap.Button(self.labelframe_gamepath, text="文件选择工具", bootstyle="outline", width=BUTTON_WIDTH, command=self.bin_choice_file)
        self.button_gamestart = ttkbootstrap.Button(self.labelframe_gamepath, text="启动游戏", bootstyle="outline", width=BUTTON_WIDTH, command=self.bin_launch_game)
        self.button_open_game = ttkbootstrap.Button(self.labelframe_gamepath, text="打开游戏目录", bootstyle="outline", width=BUTTON_WIDTH, command=self.bin_open_game)
        # self.button_unity_argument = ttkbootstrap.Button(self.labelframe_gamepath, text="Unity 通用启动参数", bootstyle="outline", width=BUTTON_WIDTH)
        self.button_filechoice.pack(side="left", padx=(10, 10), pady=(0, 10), fill="x", expand=True)
        self.button_gamestart.pack(side="left", padx=(0, 10), pady=(0, 10), fill="x", expand=True)
        self.button_open_game.pack(side="left", padx=(0, 10), pady=(0, 10), fill="x", expand=True)
        # self.button_unity_argument.pack(side="left", padx=(0, 10), pady=(0, 10))

        self.entry_custom = ttkbootstrap.Entry(self.labelframe_custom)#, bootstyle="light")
        self.entry_custom_argument = ttkbootstrap.Entry(self.labelframe_custom)#, bootstyle="light")
        self.entry_custom.pack(side="top", fill="x", expand=True, padx=10, pady=10)
        self.entry_custom_argument.pack(side="top", fill="x", expand=True, padx=10, pady=(0, 10))

        self.button_custom_filechoice = ttkbootstrap.Button(self.labelframe_custom, text="文件选择工具", bootstyle="outline", width=BUTTON_WIDTH, command=self.bin_custom_choice_file)
        self.button_custom_start = ttkbootstrap.Button(self.labelframe_custom, text="启动程序", bootstyle="outline", width=BUTTON_WIDTH, command=self.bin_custom_launch)
        self.button_custom_openpath = ttkbootstrap.Button(self.labelframe_custom, text="打开所在目录", bootstyle="outline", width=BUTTON_WIDTH, command=self.bin_custom_open_path)

        self.button_custom_filechoice.pack(side="left", padx=(10, 10), pady=(0, 10), fill="x", expand=True)
        self.button_custom_start.pack(side="left", padx=(0, 10), pady=(0, 10), fill="x", expand=True)
        self.button_custom_openpath.pack(side="left", padx=(0, 10), pady=(0, 10), fill="x", expand=True)

        self.combobox_theme.bind("<FocusIn>", lambda *_: self.combobox_theme.selection_clear())
        self.combobox_versions.bind("<FocusIn>", lambda *_: self.combobox_versions.selection_clear())
        self.combobox_log_level.bind("<FocusIn>", lambda *_: self.combobox_log_level.selection_clear())
        self.combobox_annotation_level.bind("<FocusIn>", lambda *_: self.combobox_annotation_level.selection_clear())
        self.combobox_approximate.bind("<FocusIn>", lambda *_: self.combobox_approximate.selection_clear())

        self.combobox_versions.bind("<<ComboboxSelected>>", self.bin_choice_version)
        self.combobox_theme.bind("<<ComboboxSelected>>", self.bin_set_style_theme)
        self.combobox_log_level.bind("<<ComboboxSelected>>", self.bin_set_log_level)
        self.combobox_annotation_level.bind("<<ComboboxSelected>>", self.bin_set_annotation_level)
        self.combobox_approximate.bind("<<ComboboxSelected>>", self.bin_set_approximate)


    def initial(self):
        _alt_set = core.window.annotation_toplevel.register

        _alt_set(self.combobox_theme, T.ANNOTATION_STYLE_THEME, 2)
        _alt_set(self.combobox_log_level, T.ANNOTATION_LOG_LEVEL, 2)
        _alt_set(self.combobox_annotation_level, T.ANNOTATION_ANNOTATION_LEVEL, 2)

        _alt_set(self.combobox_versions, T.ANNOTATION_D3DX_VERSION, 2)
        _alt_set(self.button_injection, T.ANNOTATION_D3DX_INJECTION, 2)
        _alt_set(self.button_d3dxstart, T.ANNOTATION_D3DX_START, 2)
        _alt_set(self.button_open_work, T.ANNOTATION_D3DX_OPEN_WORK_DIR, 2)

        _alt_set(self.entry_gamepath, T.ANNOTATION_D3DX_SET_GAME_PATH, 2)
        _alt_set(self.entry_game_argument, T.ANNOTATION_D3DX_GAME_ARGUMENT, 2)
        _alt_set(self.wbn_unity_args, T.ANNOTATION_UNITY_ARGS, 2)
        _alt_set(self.button_filechoice, T.ANNOTATION_D3DX_SET_GAME_PATH, 2)
        _alt_set(self.button_gamestart, T.ANNOTATION_D3DX_START, 2)
        _alt_set(self.button_open_game, T.ANNOTATION_D3DX_GAME_WORK_DIR, 2)

        _alt_set(self.entry_custom, T.ANNOTATION_D3DX_CUSTOM_PATH, 2)
        _alt_set(self.entry_custom_argument, T.ANNOTATION_D3DX_CUSTOM_ARGUMENT, 2)
        _alt_set(self.button_custom_filechoice, T.ANNOTATION_D3DX_CUSTOM_PATH, 2)
        _alt_set(self.button_custom_start, T.ANNOTATION_D3DX_CUSTOM_LAUNCH, 2)
        _alt_set(self.button_custom_openpath, T.ANNOTATION_D3DX_CUSTOM_DIR, 2)


    def __init__(self, master):
        self.master = master
        self.install(master)


    def update(self):
        core.log.info("更新 d3dx 环境设置信息...")

        self.combobox_theme.config(values=core.window.style_theme_names)
        self.combobox_theme.delete(0, end)
        self.combobox_theme.insert(0, core.env.configuration.style_theme)

        for key, value in LOG_LEVEL.items():
            if core.env.configuration.log_level == value:
                self.combobox_log_level.delete(0, end)
                self.combobox_log_level.insert(0, key)
                break

        for key, value in ANNOTATION_LEVEL.items():
            if core.env.configuration.annotation_level == value:
                self.combobox_annotation_level.delete(0, end)
                self.combobox_annotation_level.insert(0, key)
                break

        self.combobox_approximate.delete(0, end)
        self.combobox_approximate.insert(0, core.env.configuration.thumbnail_approximate_algorithm)

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

        custom_file = core.userenv.configuration.custom_launch
        if custom_file is None: custom_file = "< 未设置 >"
        self.entry_custom.delete(0, end)
        self.entry_custom.insert(0, custom_file)

        game_launch_argument = core.userenv.configuration.game_launch_argument

        if isinstance(game_launch_argument, str):
            self.entry_game_argument.delete(0, end)
            self.entry_game_argument.insert(0, game_launch_argument)

        custom_launch_argument = core.userenv.configuration.custom_launch_argument

        if isinstance(custom_launch_argument, str):
            self.entry_custom_argument.delete(0, end)
            self.entry_custom_argument.insert(0, custom_launch_argument)




    def sbin_update_game_path(self, text):
        self.entry_gamepath.delete(0, end)
        self.entry_gamepath.insert(0, text)


    def bin_set_style_theme(self, *_):
        self.combobox_theme.selection_clear()
        value = self.combobox_theme.get()
        if value not in core.window.style_theme_names:
            return
        
        core.window.style.theme_use(value)
        core.env.configuration.style_theme = value
        core.window.style.configure("Treeview", rowheight=48)


    def bin_set_log_level(self, *_):
        self.combobox_log_level.selection_clear()
        key = self.combobox_log_level.get()
        value = LOG_LEVEL.get(key, None)
        if value is None:
            return
        core.env.configuration.log_level = value


    def bin_set_annotation_level(self, *_):
        self.combobox_annotation_level.selection_clear()
        key = self.combobox_annotation_level.get()
        value = ANNOTATION_LEVEL.get(key, None)
        if value is None:
            return
        core.env.configuration.annotation_level = value


    def bin_set_approximate(self, *_):
        self.combobox_approximate.selection_clear()
        value = self.combobox_approximate.get()
        core.env.configuration.thumbnail_approximate_algorithm = value
        core.window.interface.mods_manage.update_classification_list()
        core.window.interface.mods_warehouse.refresh()


    def bin_selection_clear(self, *args, **kwds):
        self.combobox_versions.selection_clear()
        self.combobox_log_level.selection_clear()
        self.combobox_annotation_level.selection_clear()


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
            if e.args[0] == 5:
                core.window.messagebox.showerror(title="权限请求被拒绝", message="你拒绝了程序请求管理员权限\n这是你的问题，而非程序出现了逻辑错误")
            else:
                core.window.messagebox.showerror(title="异常捕获", message=f"{e.args[1]}: {e.args[0]}\n{e.args[2]}")
        except Exception:
            core.window.messagebox.showerror(title="程序故障", message="无法找到正确的方式启动该程序")
            return 0


    def bin_onekey_launch(self, *args, **kwds):
        core.window.messagebox.showinfo(title="成就：不信邪", message="都说过了这个玩意儿不能用")


    def bin_open_work(self, *args, **kwds):
        # win32api.ShellExecute(None, "open", os.path.abspath(core.userenv.directory.work), None, os.path.abspath(core.userenv.directory.work), 1)
        core.external.view_directory(os.path.abspath(core.userenv.directory.work))


    def bin_open_game(self, *args, **kwds):
        path = core.userenv.configuration.GamePath
        if path is None:
            core.window.messagebox.showerror(title="数据未设置", message="无法打开游戏目录\n未设置游戏路径")
            return

        path = os.path.dirname(path)

        # win32api.ShellExecute(None, "open", path, None, path, 1)
        core.external.view_directory(path)


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

        argument = self.entry_game_argument.get().strip()
        core.userenv.configuration.game_launch_argument = argument

        if path is None:
            core.window.messagebox.showerror(title="数据未设置", message="无法启动游戏\n未设置游戏路径")
            return
        try:
            win32api.ShellExecute(None, "open", path, argument, os.path.realpath(os.path.dirname(path)), 1)
        except pywintypes.error as e:
            if e.args[0] == 5:
                core.window.messagebox.showerror(title="权限请求被拒绝", message="你拒绝了程序请求管理员权限\n这是你的问题，而非程序出现了逻辑错误")
            else:
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


    def bin_custom_choice_file(self, *_):
        choice_PATH = tkinter.filedialog.askopenfilename(title="选择应用程序", filetypes=[("应用程序", "*.exe"), ("All Files", "*")])
        choice_PATH = choice_PATH.replace("/", "\\")
        if not choice_PATH: return None
        choice_NAME = os.path.basename(choice_PATH)

        if choice_NAME[choice_NAME.rfind("."):] != ".exe":
            core.window.messagebox.showerror(title="错误的映像名", message="你选择了一个非 .exe 后缀名的文件\n请确认选择的是应用程序文件\n操作已被阻止")
            return

        core.userenv.configuration.custom_launch = choice_PATH
        self.entry_custom.delete(0, end)
        self.entry_custom.insert(0, choice_PATH)


    def bin_custom_launch(self, *_):
        path = core.userenv.configuration.custom_launch
        if path is None:
            core.window.messagebox.showerror(title="数据未设置", message="无法启动程序\n未设置程序路径")
            return

        argument = self.entry_custom_argument.get().strip()
        core.userenv.configuration.custom_launch_argument = argument

        try:
            win32api.ShellExecute(None, "open", path, argument, os.path.realpath(os.path.dirname(path)), 1)
        except pywintypes.error as e:
            if e.args[0] == 5:
                core.window.messagebox.showerror(title="权限请求被拒绝", message="你拒绝了程序请求管理员权限\n这是你的问题，而非程序出现了逻辑错误")
            else:
                core.window.messagebox.showerror(title="异常捕获", message=f"{e.args[1]}: {e.args[0]}\n{e.args[2]}")
        except Exception:
            core.window.messagebox.showerror(title="程序故障", message="无法找到正确的方式启动该程序")
            return


    def bin_custom_open_path(self, *_):
        path = core.userenv.configuration.custom_launch
        if path is None:
            core.window.messagebox.showerror(title="数据未设置", message="无法打开程序目录\n未设置程序路径")
            return

        path = os.path.dirname(path)

        # win32api.ShellExecute(None, "open", path, None, path, 1)
        core.external.view_directory(path)
