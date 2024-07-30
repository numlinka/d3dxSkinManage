# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import webbrowser
import ttkbootstrap

# local
import core
from constant import *
from libs.dispatch import tkasyncmain


class About (object):
    def install(self, master):
        self.master = master

        self.frame_about = ttkbootstrap.Frame(self.master)
        self.frame_afdian = ttkbootstrap.Frame(self.master)
        self.frame_channel = ttkbootstrap.Frame(self.master)
        self.frame_afdian.pack(side="bottom", fill="x", padx=10, pady=10)
        # self.frame_channel.pack(side="bottom", fill="x", padx=10, pady=(10, 0))
        self.frame_about.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 0))

        # self.what_to_look_at = ttkbootstrap.Label(self.frame, text=T.TEXT_ADOUT)
        self.what_to_look_at = ttkbootstrap.Text(self.frame_about)
        self.scrollbar_about = ttkbootstrap.Scrollbar(self.what_to_look_at, command=self.what_to_look_at.yview)
        self.what_to_look_at.config(yscrollcommand=self.scrollbar_about.set)
        self.what_to_look_at.insert(0.0, T.TEXT_ABOUT)
        self.what_to_look_at.config(state="disabled")

        self.what_to_look_at.pack(side="top", fill="both", expand=True)

        self.label_sponsor = ttkbootstrap.Label(self.frame_afdian, text="爱发电赞助地址: ", font=("黑体", 16))
        self.label_afdian = ttkbootstrap.Label(self.frame_afdian, text=">> numLinka >>>", font=("黑体", 16), foreground="medium purple", cursor="hand2")
        self.label_afdian_ticca = ttkbootstrap.Label(self.frame_afdian, text=">> 黎愔 >>>", font=("黑体", 16), foreground="medium purple", cursor="hand2")

        self.label_sponsor.pack(side="left")
        self.label_afdian.pack(side="left")
        self.label_afdian_ticca.pack(side="left", padx=(25, 0))

        self.label_afdian.bind("<Button-1>", self.bin_open_afdian)
        self.label_afdian_ticca.bind("<Button-1>", self.bin_open_afdian_ticca)

        self.what_to_look_at.bind("<Enter>", lambda *_: self.scrollbar_about.pack(side="right", fill="y"), "+")
        self.what_to_look_at.bind("<Leave>", lambda *_: self.scrollbar_about.pack_forget(), "+")


    def __init__(self, master):
        self.master = master
        try: self.install(master)
        except Exception: ...


    def bin_open_afdian(self, *_):
        webbrowser.open(core.env.Link.afdian)


    def bin_open_afdian_ticca(self, *_):
        webbrowser.open(core.env.Link.afdian_ticca)
