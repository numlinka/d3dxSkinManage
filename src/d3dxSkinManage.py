# -*- coding: utf-8 -*-

import os
import sys
import ctypes
# import inspect

import core


# ! 禁用 Windows 缩放
# * 让程序使用自己的 DPI 适配
try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception: ...


def main():
    core.run()


if __name__ == '__main__':
    main()


try:
    sys.exit(0)  # SystemExit
except Exception:
    os._exit(0)

# exit()
