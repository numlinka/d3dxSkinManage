# d3dxSkinManage
# Copyright (C) 2023 numlinka
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# std
import sys
import ctypes

# local
import core


# ! 禁用 Windows 缩放
# * 让程序使用自己的 DPI 适配
try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception: ...


def main():
    core.run()


if __name__ == "__main__":
    main()
    sys.exit(0)
