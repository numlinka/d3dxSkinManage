# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# site
import ttkbootstrap


class Custom (object):
    def __init__(self, master):
        self.master = master

        BUTTON_WIDTH = 20

        self.entry_custom = ttkbootstrap.Entry(self.master)#, bootstyle="light")
        self.entry_custom_argument = ttkbootstrap.Entry(self.master)#, bootstyle="light")
        self.entry_custom.pack(side="top", fill="x", padx=10, pady=10)
        self.entry_custom_argument.pack(side="top", fill="x", padx=10, pady=(0, 10))

        self.frame_top = ttkbootstrap.Frame(self.master)
        self.frame_bottom = ttkbootstrap.Frame(self.master)
        self.frame_top.pack(side="top", fill="x")
        self.frame_bottom.pack(side="bottom", fill="x")

        self.button_custom_start = ttkbootstrap.Button(self.frame_bottom, text="启动程序", bootstyle="outline", width=BUTTON_WIDTH)#, command=self.bin_custom_launch)

        self.button_custom_filechoice = ttkbootstrap.Button(self.frame_top, text="文件选择工具", bootstyle="outline", width=BUTTON_WIDTH)#, command=self.bin_custom_choice_file)
        self.button_custom_openpath = ttkbootstrap.Button(self.frame_top, text="打开所在目录", bootstyle="outline", width=BUTTON_WIDTH)#, command=self.bin_custom_open_path)

        self.button_custom_start.pack(side="right", padx=10, pady=10)

        self.button_custom_filechoice.pack(side="left", padx=(10, 10), pady=(0, 10))
        self.button_custom_openpath.pack(side="left", padx=(0, 10), pady=(0, 10))