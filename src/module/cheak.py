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

def zip_direct_run():
    temp_path = os.environ.get("TEMP", "")
    if not temp_path and not sys.executable.startswith(temp_path):
        return

    core.sync.clear()
    core.window.block.setcontent(ZIP_RUN)
    core.window.status.set_status("别在压缩包里直接运行程序", 1)
    raise SystemExit
