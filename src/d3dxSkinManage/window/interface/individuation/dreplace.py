# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# site
import ttkbootstrap


class DReplace (object):
    def __init__(self, master):
        self.master = master

        BUTTON_WIDTH = 20

        self.combobox_versions = ttkbootstrap.Combobox(self.master)#, bootstyle="light")
        self.combobox_versions.pack(side="top", fill="x", padx=10, pady=10)

        self.frame_top = ttkbootstrap.Frame(self.master)
        self.frame_bottom = ttkbootstrap.Frame(self.master)
        self.frame_top.pack(side="top", fill="x")
        self.frame_bottom.pack(side="bottom", fill="x")

        self.button_d3dxstart = ttkbootstrap.Button(self.frame_bottom, text="启动加载器", bootstyle="outline", width=BUTTON_WIDTH)#, command=self.bin_launch_d3dx)
        self.button_open_work = ttkbootstrap.Button(self.frame_top, text="打开工作目录", bootstyle="outline", width=BUTTON_WIDTH)#, command=self.bin_open_work)

        # self.button_injection = ttkbootstrap.Button(self.master, text="一键启动", bootstyle="outline", width=BUTTON_WIDTH)#, command=self.bin_onekey_launch)
        # self.button_injection.pack(side="top", padx=(10, 10), pady=(0, 10))

        self.button_open_work.pack(side="left", padx=10, pady=(0, 10))
        self.button_d3dxstart.pack(side="right", padx=10, pady=10)
