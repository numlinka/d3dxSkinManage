# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import os
import re
from typing import *

# local
import core
import window

# site
import ttkbootstrap
import ttkbootstrap.style


NORMAL = "normal"
SUGGEST = "suggest"
WARN = "warn"
ERROR = "error"


class Suggestions(object):
    def __init__(self) -> None:
        titles = (
            ("#0", "项目", 100),
            ("#1", "检查结果", 500)
        )
        self.window = ttkbootstrap.Toplevel()
        self.window.title("优化建议")
        self.window.geometry("800x500")
        window.methods.fake_withdraw(self.window)
        window.methods.center_window_for_window(self.window, window.mainwindow, 800, 500, True)
        self.window.transient(core.window.mainwindow)
        self.window.grab_set()
        self.window.focus()

        self.suggests = ttkbootstrap.Treeview(self.window, show="tree headings", selectmode="extended", columns=("#1",))
        self.scrollbar = ttkbootstrap.Scrollbar(self.window, command=self.suggests.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.suggests.pack(fill="both", expand=True)

        self.suggests.configure(yscrollcommand=self.scrollbar.set)

        self.suggests.tag_configure(NORMAL)
        self.suggests.tag_configure(SUGGEST, foreground="yellow")
        self.suggests.tag_configure(WARN, foreground="orange")
        self.suggests.tag_configure(ERROR, foreground="red")

        for tree, text, width in titles:
            self.suggests.column(tree, width=width, anchor="w")
            self.suggests.heading(tree, text=text)

        core.construct.taskpool.addtask(self.action, False)


    def add(self, text: str, result: str = ..., level: str = ...):
        if result is ...:
            result = "正常"

        if level is ...:
            level = NORMAL

        self.suggests.insert("", "end", text=text, values=(result, ), tags=level)


    def action(self, *_):
        for text, task in CHECK_LIST:
            try:
                level, result = task()
                self.window.after(0, self.add, text, result, level)

            except Exception:
                self.window.after(0, self.add, text, "检查异常失败", ERROR)

        self.window.after(0, self.add, "结束", "所有检查均已完成", NORMAL)


def check_cwd(*_) -> Tuple[str, str]:
    pattern = re.compile(r"[^a-zA-Z0-9\s\-_\\/]")
    match = pattern.search(core.env.cwd)
    if not match:
        return WARN, "工作目录中存在拉丁字母和阿拉伯数字以外的字符"

    if " " in core.env.cwd:
        return SUGGEST, "工作目录中存在空格字符"

    return NORMAL, "正常"


def check_rights(*_) -> Tuple[str, str]:
    try:
        file = open(os.path.join(core.env.cwd, "check_rights.temp.file"), "w")
        file.write("check_rights")
        file.close()
        os.remove(os.path.join(core.env.cwd, "check_rights.temp.file"))

    except PermissionError:
        return ERROR, "没有权限访问工作目录"

    except FileNotFoundError:
        return ERROR, "工作目录不存在"

    except Exception as e:
        return ERROR, f"未知错误：{e}"

    else:
        return NORMAL, "正常"


def check_rights_groups(*_) -> Tuple[str, str]:
    if core.env.is_admin:
        return SUGGEST, "程序运行在管理员权限组下"

    return NORMAL, "正常"


def check_update_components(*_) -> Tuple[str, str]:
    if not os.path.isfile("update.exe"):
        return ERROR, "缺少更新组件 update.exe"

    else:
        return NORMAL, "正常（也许）"


def check_7zip_components(*_) -> Tuple[str, str]:
    if not os.path.isfile(core.env.cwd.local.t7z):
        return ERROR, "缺少 7zip 组件 7z.exe"

    if not os.path.isfile(os.path.join(core.env.cwd.local.t7zip, "7z.dll")):
        return ERROR, "缺少 7zip 组件 7z.dll"

    file_path_compression = os.path.join(core.env.cwd.resources.cache, "compression.test")
    file_path_compressed = os.path.join(core.env.cwd.resources.cache, "compressed.test")

    with open(file_path_compression, "w") as file_object:
        file_object.write("compression.test")

    core.external.a7z(file_path_compression, file_path_compressed)
    os.remove(file_path_compression)

    if not os.path.isfile(file_path_compressed):
        return ERROR, "压缩测试失败"

    core.external.x7z(file_path_compressed, core.env.cwd.resources.cache)
    os.remove(file_path_compressed)

    if not os.path.isfile(file_path_compression):
        return ERROR, "解压测试失败"

    os.remove(file_path_compression)
    return NORMAL, "正常"


def check_userenv_name(*_) -> Tuple[str, str]:
    if core.userenv.user_name is Ellipsis:
        return SUGGEST, "未登录任何用户环境"

    pattern = re.compile(r"[^a-zA-Z0-9\s\-_\\/]")
    match = pattern.search(core.env.cwd)
    if not match:
        return WARN, "用户名存在拉丁字母和阿拉伯数字以外的字符"

    if " " in core.env.cwd:
        return SUGGEST, "用户名存在空格字符"

    return NORMAL, "正常"


def check_game_path(*_) -> Tuple[str, str]:
    if core.userenv.user_name is Ellipsis:
        return SUGGEST, "未登录任何用户环境"

    if not os.path.isfile(core.userenv.configuration.GamePath):
        return ERROR, "游戏路径不存在"

    return NORMAL, "正常"



CHECK_LIST = [
    ("工作目录", check_cwd),
    ("访问权限", check_rights),
    ("权限组", check_rights_groups),
    ("更新组件", check_update_components),
    ("7zip 组件", check_7zip_components),
    ("用户环境名称", check_userenv_name),
    ("游戏路径", check_game_path),
]
