
# std
import os
import json
import locale
import threading
import tkinter.filedialog

# site
import ttkbootstrap
from ttkbootstrap.constants import *

# libs
import core
import window
from constant import *



class containe ():
    action = threading.Lock()



class LaunchScript (object):
    def __init__(self) -> None:
        result = containe.action.acquire(timeout=0.01)
        if not result:
            core.window.messagebox.showerror(title="操作已被阻止", message="请勿重复启动该工具")
            return


        self.window = ttkbootstrap.Toplevel()
        core.window.methods.fake_withdraw(self.window)
        self.window.title("简易启动脚本生成工具")
        self.window.resizable(width=False, height=False)
        self.window.protocol('WM_DELETE_WINDOW', self.bin_close)
        self.window.transient(window.mainwindow)
        self.window.focus_set()

        try:
            self.window.iconbitmap(default=core.env.file.local.iconbitmap)
            self.window.iconbitmap(bitmap=core.env.file.local.iconbitmap)
        except Exception:
            ...


        self.frame_option = ttkbootstrap.Frame(self.window)
        self.frame_button = ttkbootstrap.Frame(self.window)

        self.frame_option.pack(side=TOP, fill=X, padx=(5, 5), pady=(5, 5))
        self.frame_button.pack(side=BOTTOM, fill=X, padx=(5, 5), pady=(0, 5))

        self.frame_option.grid_columnconfigure(0, weight=1)

        self.v_runas    = ttkbootstrap.BooleanVar()
        self.v_3dmigoto = ttkbootstrap.BooleanVar()
        self.v_game     = ttkbootstrap.BooleanVar()
        self.v_custom   = ttkbootstrap.BooleanVar()

        self.label_runas    = ttkbootstrap.Label(self.frame_option, text="请求管理员权限")
        self.label_3dmigoto = ttkbootstrap.Label(self.frame_option, text="启动加载器")
        self.label_game     = ttkbootstrap.Label(self.frame_option, text="启动游戏")
        self.label_custom   = ttkbootstrap.Label(self.frame_option, text="启动自定义程序")

        self.check_runas    = ttkbootstrap.Checkbutton(self.frame_option, variable=self.v_runas,    bootstyle=(SUCCESS, SQUARE, TOGGLE), cursor="hand2")
        self.check_3dmigoto = ttkbootstrap.Checkbutton(self.frame_option, variable=self.v_3dmigoto, bootstyle=(SUCCESS, SQUARE, TOGGLE), cursor="hand2")
        self.check_game     = ttkbootstrap.Checkbutton(self.frame_option, variable=self.v_game,     bootstyle=(SUCCESS, SQUARE, TOGGLE), cursor="hand2")
        self.check_custom   = ttkbootstrap.Checkbutton(self.frame_option, variable=self.v_custom,   bootstyle=(SUCCESS, SQUARE, TOGGLE), cursor="hand2")

        self.label_runas    .grid(row=0, column=0, sticky=W, padx=(0, 0), pady=(0, 0))
        self.label_3dmigoto .grid(row=1, column=0, sticky=W, padx=(0, 0), pady=(5, 0))
        self.label_game     .grid(row=2, column=0, sticky=W, padx=(0, 0), pady=(5, 0))
        self.label_custom   .grid(row=3, column=0, sticky=W, padx=(0, 0), pady=(5, 0))

        self.check_runas    .grid(row=0, column=1, sticky=W, padx=(5, 0), pady=(0, 0))
        self.check_3dmigoto .grid(row=1, column=1, sticky=W, padx=(5, 0), pady=(5, 0))
        self.check_game     .grid(row=2, column=1, sticky=W, padx=(5, 0), pady=(5, 0))
        self.check_custom   .grid(row=3, column=1, sticky=W, padx=(5, 0), pady=(5, 0))

        self.button_sure = ttkbootstrap.Button(self.frame_button, text="生成", width=10, bootstyle=(SUCCESS, OUTLINE), cursor="hand2", command=self.bin_sure)
        self.button_sure.pack(side=RIGHT)

        self.window.update()
        window.methods.center_window_for_window(self.window, window.mainwindow, 300, 200, True)


    def bin_sure(self, *_):
        filepath = tkinter.filedialog.asksaveasfilename(
            title="生成脚本位置",
            initialfile=core.userenv.user_name,
            defaultextension=".bat",
            filetypes=[("批处理文件", ".bat")]
            )

        if not filepath: return

        content = ""

        if self.v_runas.get():
            content += '''%1 start "" mshta vbscript:createobject("shell.application").shellexecute("""%~0""","::",,"runas",1)(window.close)&exit\n'''


        if self.v_3dmigoto.get():
            schemepath = os.path.join(core.userenv.directory.work, "scheme.json")
            if os.path.isfile(schemepath):
                try:
                    with open(schemepath, "r", encoding="utf-8") as fileobject:
                        filecontent = fileobject.read()
                        scheme = json.loads(filecontent)
                        launch_name = scheme["launch"]
                except Exception:
                    window.messagebox.showerror("scheme 数据解释失败\n请检查用户 work 目录或 d3dx 版本", title="数据错误")

            else:
                lst = os.listdir(core.userenv.directory.work)
                for name in ["3DMigotoLoader.exe", "3DMigoto Loader.exe"]:
                    if name in lst:
                        launch_name = name
                        break
                else:
                    window.messagebox.showerror(title="检索错误", message="无法找到正确的方式启动 3DMigoto 加载器\n请检查用户 work 目录或 d3dx 版本")
                    return

            launch_file = os.path.abspath(os.path.join(core.userenv.directory.work, launch_name))

            content += f"cd /d \"{os.path.abspath(core.userenv.directory.work)}\"\n"
            content += f"start \"\" \"{launch_file}\"\n"


        if self.v_game.get():
            path = core.userenv.configuration.GamePath
            argument = core.userenv.configuration.game_launch_argument

            if not path:
                window.messagebox.showerror(title="解析错误", message="未设置游戏路径")
                return

            content += f"cd /d \"{os.path.dirname(path)}\"\n"

            if argument:
                content += f"start \"\" \"{path}\" {argument}\n"

            else:
                content += f"start \"\" \"{path}\"\n"

        if self.v_custom.get():
            path = core.userenv.configuration.custom_launch
            argument = core.userenv.configuration.custom_launch_argument

            if not path:
                window.messagebox.showerror(title="解析错误", message="未设置自定义启动项目路径")
                return

            content += f"cd /d \"{os.path.dirname(path)}\"\n"

            if argument:
                content += f"start \"\" \"{path}\" {argument}\n"

            else:
                content += f"start \"\" \"{path}\"\n"


        with open(filepath, "w", encoding=locale.getpreferredencoding()) as f:
            f.write(content)

        self.bin_close()


    def bin_close(self, *_):
        containe.action.release()
        self.window.destroy()
