import os
import sys

import core


ZIP_RUN = """初始化流程已被中止
\n\n
发生了什么？

程序在不适宜的目录下运行
你很有可能是在压缩包里直接运行程序
\n\n
该怎么做？

1. 退出程序
2. 将程序解压到其它目录下
3. 双击运行解压后的程序
\n\n
还是不会？

叫你男朋友来弄
\n\n
无论上述猜测是否正确
程序都将中止执行
"""

MISS_MODULE = """初始化流程已被中止
\n\n
程序存在以下问题
"""

MISS_MODULE_BASENAME = f"""
主程序名称不为 d3dxSkinManage.exe
    无论出于什么原因，你都不应该修改主程序的名称
    这可能导致其它组件无法识别到主程序
"""

MISS_MODULE_UPDATE = """
缺少更新组件
    却少该组件会导致程序更新无法正常进行
"""

MISS_MODULE_7ZIP = """
缺少 7zip 组件
    缺少该组件时程序无法进行解压缩操作
"""

MISS_MODULE_OVER = """
\n
该怎么做？

1. 点程序窗口右下角的帮助按钮
2. 在官网下载完整的程序包 或 参考文档补全缺失的组件
\n\n
不要把更新包当成完整包直接使用

为避免呆子在遇到此类错误时不知所措，程序将中止执行，即使某些错误类型无关紧要
如果这个残缺包是其他人给你的，你可以在闲暇之余去骂他一顿
"""


def zip_direct_run():
    temp_path = os.environ.get("TEMP", "")
    if not temp_path or not sys.executable.startswith(temp_path):
        return

    core.sync.clear()
    core.window.block.setcontent(ZIP_RUN)
    core.window.status.set_status("别在压缩包里直接运行程序", 1)
    raise SystemExit


def miss_components():
    abnormality = False
    basename = os.path.basename(sys.executable)
    msg = MISS_MODULE
    if not basename in [core.env.cwd.self, "python.exe"]:
        abnormality = True
        msg += MISS_MODULE_BASENAME

    if not os.path.isfile(core.env.cwd.update):
        abnormality = True
        msg += MISS_MODULE_UPDATE

    if not os.path.isfile(core.env.cwd.local.t7z):
        abnormality = True
        msg += MISS_MODULE_7ZIP

    if abnormality:
        msg += MISS_MODULE_OVER
        core.window.block.setcontent(msg)
        core.window.status.set_status("程序存在异常", 1)
        raise SystemExit
