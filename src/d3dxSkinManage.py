# -*- coding: utf-8 -*-

import sys
import ctypes

import core


# ! 禁用 Windows 缩放
# * 让程序使用自己的 DPI 适配
try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception: ...


def main():
    core.run()


if __name__ == '__main__':
    main()
    sys.exit(0)
