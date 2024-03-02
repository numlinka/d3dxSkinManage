# -*- coding: utf-8 -*-

# std
import os
import time
import locale
import fnmatch
import threading

# project
import core

# self
from . import add_mod
from . import add_preview


class StopDeliverSignal (Exception): ...



oscode = locale.getpreferredencoding()

# dropfiles 单个文件规则
single_dropfiles_rules = [
    ("*.png", add_preview.add_preview, False),
    ("*.jpg", add_preview.add_preview, False),
]
# add tuple[str, function, bool | None]
# 第一个元素为需要匹配的文件名 ( 使用通配符 )
# 第二个元素为回调函数
# 第三个元素为是否异步函数执行
#   True    异步执行 ( 在一个新的控制线程中执行 )
#   False   同步执行 ( 在当前线程中执行 )
#   None    回调执行 ( 将回调函数传递给主线程执行 )

# dropfiles 单个文件夹规则
single_dropfiles_folder_rules = []
# 同上

# 接管函数
takeover_functions = []
# 如果你想接管 hook_dropfiles_new 的流程
# 请将对应的函数 add 到该列表中 ( 只需要函数 )
# 如果你认为该消息是对你有利的且不希望 hook_dropfiles_new 执行后续流程
# 请 raise StopDeliverSignal 异常


def check_for_login() -> bool:
    return isinstance(core.userenv.user_name, str)


def hook_dropfiles_new(original_items: list):
    threading.Thread(None, async_hook_dropfiles_new, "async.dropfiles", (original_items, ), daemon=True).start()


def async_hook_dropfiles_new(original_items: list):
    core.log.debug(f"dropfiles_new 钩子 {original_items}")
    if not check_for_login():
        core.window.messagebox.showerror(title="dropfiles: 未登录错误", message="必须先登录一个用户\n才能使用文件拖入功能")
        return


    try:
        items = [x.decode(oscode) for x in original_items]

    except Exception:
        core.window.messagebox.showerror(title="dropfiles: 编码不可解", message=f"无法解码消息内容\n请检查系统编码是否为 {oscode}")
        return


    try:
        for callback in takeover_functions:
            callback(items)

    except StopDeliverSignal:
        return

    except Exception as e:
        core.log.error(f"takeover_functions Exception {e.__class__} {e}")


    try:
        if len(items) == 1:
            item = items[0]
            if os.path.isfile(item):
                single_rule_matching(item, single_dropfiles_rules)

            elif os.path.isdir(item):
                single_rule_matching(item, single_dropfiles_folder_rules)

            else:
                core.window.messagebox.showerror(title="dropfiles: 消息检查错误", message=f"无法找到目标文件或目录\n{item}")
                return

        else:
            core.window.messagebox.showerror(title="dropfiles: 消息检查错误", message=f"没有匹配到规则\n没有处理对应多文件的触发器")
            return

    except Exception as e:
        core.window.messagebox.showerror(title="dropfiles: 未定义错误", message=f"{e.__class__}\n{e}\n{item}")
        return


def single_rule_matching(item: str, rules: list):
    basename = os.path.basename(item)
    efficient = False
    for rule, callback, async_ in rules:
        if not fnmatch.fnmatch(basename, rule): continue

        efficient = True
        match async_:
            case None:  core.window.mainwindow.after(10, callback, item)
            case True:  threading.Thread(None, callback, "additional.dropfiles", (item, ), daemon=True).start()
            case False: callback(item)

        time.sleep(0.1)

    if not efficient:
        core.window.messagebox.showerror(title="dropfiles: 没有匹配到规则", message=f"没有匹配到规则\n没有处理该文件类型的触发器")




# ! 以下全部弃用

code1 = 'gb18030'
code2 = 'utf-8'


rule_single = [
    (['.png', '.jpg'], add_preview.add_preview, False),
    (['.zip', '.rar', '.7z'], add_mod.AddMods, True)
]


def hook_dropfiles(items: list):
    core.log.debug(f"dropfiles 钩子 {items}")
    try:
        if not check_for_login():
            core.window.messagebox.showerror(title='未登录错误', message='必须先登录一个用户\n才能使用文件拖入功能')
            return

        lst = []

        for item in items:
            try:
                try: content = item.decode(code1)
                except Exception: content = item.decode(code2)
                lst.append(content)
            except Exception:
                core.window.messagebox.showerror(title='编码不可解', message='无法解码消息内容\n请检查系统编码是否为 utf-8 或 gb18030')
                return

        core.log.debug(f"dropfiles 钩子内容 {lst}")

        if len(lst) <= 0:
            ...

        elif len(lst) == 1:
            bin_dropfiles_single(lst.pop())

        else:
            bin_dropfiles_multiple(lst)

    except Exception as e:
        core.window.messagebox.showerror(title='触发器异常', message=f'hook 异常 / 任务冲突\n请稍后重试\n{e.__class__} {e}')


def __exec_call(func_, async_: bool, arg_: object):
        if async_: threading.Thread(None, func_, 'hookTask', (arg_, ), daemon=True).start()
        else: func_(arg_)


def bin_dropfiles_single(content):
    if os.path.isfile(content):
        basename = os.path.basename(content)

        suffix = basename[basename.rfind('.'):]

        for rule in rule_single:
            accept_, func_, async_ = rule

            if suffix in accept_:
                __exec_call(func_, async_, content)
                return

        else:
            core.window.messagebox.showerror(title='不支持的文件类型', message='没有处理该文件类型的触发器')


    elif os.path.isdir(content):
        # if not core.window.messagebox.askyesno(title='操作确认', message='是否将该文件夹作为 Mod 导入?'): return
        __exec_call(add_mod.add_mod_is_dir, True, content)


    else:
        core.window.messagebox.showerror(title='无法处理', message='未知目标类型或路径不存在')
        return


def bin_dropfiles_multiple(content):
    core.window.messagebox.showerror(title='无法处理', message='无法一次性处理多个文件\n请将文件分别导入')
    return
