# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# site
import ttkbootstrap


class GanePath (object):
    def __init__(self, master):
        self.master = master

        BUTTON_WIDTH = 20

        self.entry_gamepath = ttkbootstrap.Entry(self.master)#, bootstyle="light")
        self.entry_game_argument = ttkbootstrap.Entry(self.master)#, bootstyle="light")
        self.entry_gamepath.pack(side="top", fill="x", padx=10, pady=10)
        self.entry_game_argument.pack(side="top", fill="x", padx=10, pady=(0, 10))

        self.frame_top = ttkbootstrap.Frame(self.master)
        self.frame_bottom = ttkbootstrap.Frame(self.master)
        self.frame_top.pack(side="top", fill="x")
        self.frame_bottom.pack(side="bottom", fill="x")

        self.button_gamestart = ttkbootstrap.Button(self.frame_bottom, text="启动游戏", bootstyle="outline", width=BUTTON_WIDTH)#, command=self.bin_launch_game)

        self.button_filechoice = ttkbootstrap.Button(self.frame_top, text="文件选择工具", bootstyle="outline", width=BUTTON_WIDTH)#, command=self.bin_choice_file)
        self.button_open_game = ttkbootstrap.Button(self.frame_top, text="打开游戏目录", bootstyle="outline", width=BUTTON_WIDTH)#, command=self.bin_open_game)
        # self.button_unity_argument = ttkbootstrap.Button(self.labelframe_gamepath, text="Unity 通用启动参数", bootstyle="outline", width=BUTTON_WIDTH)

        self.button_gamestart.pack(side="right", padx=10, pady=10)

        self.button_filechoice.pack(side="left", padx=(10, 10), pady=(0, 10))
        self.button_open_game.pack(side="left", padx=(0, 10), pady=(0, 10))