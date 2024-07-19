# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import tkinter
import ttkbootstrap

# lcoal
import core
from constant import *


class SButton (object):
    def __init__(self, master, objective: str):
        self.master = master
        self.objective = objective

        self.button = ttkbootstrap.Button(self.master, text=self.objective, command=self.command)
        self.pack = self.button.pack


    def command(self, *_):
        core.construct.event.set_event(getattr(E, self.objective))



class SignalEvent (object):
    def __init__(self, master):
        self.master = master

        self.frame1 = ttkbootstrap.Frame(self.master)
        self.frame2 = ttkbootstrap.Frame(self.master)
        self.frame3 = ttkbootstrap.Frame(self.master)

        self.frame1.pack(side="left", fill="y", padx=(10, 5), pady=10)
        self.frame2.pack(side="left", fill="y", padx=(0, 10), pady=10)

        _len = len(E.__all__)
        half = _len // 2 + _len % 2
        for index, TEXT in enumerate(E.__all__):
            if index // half == 0:
                frame = self.frame1

            else:
                frame = self.frame2

            if index % half == 0:
                pady = 0

            else:
                pady = (5, 0)

            SButton(frame, TEXT).pack(fill="x", pady=pady)
