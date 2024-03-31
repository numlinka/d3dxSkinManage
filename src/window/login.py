# -*- coding: utf-8 -*-

import os
import datetime

import ttkbootstrap

import core
import module
import window

from constant import L


class Fool (object):
    effective = datetime.datetime.now().strftime("%m-%d") == "04-01"
    frame_width = 0
    frame_height = 0
    widget_width = 0
    widget_height = 0
    x = 0
    y = 0
    XL = 0
    XR = 0
    YT = 0
    YB = 0
    count = 0



class Login(object):
    def __init__(self, master):
        self.master = master

        self.treeview_users = ttkbootstrap.Treeview(self.master, selectmode="extended", show="tree")
        self.treeview_users.column("#0", width=300, anchor="w")
        self.treeview_users.pack(side="left", fill="y", padx=10, pady=10)

        self.label_description = ttkbootstrap.Label(self.master)
        self.label_description.pack(side="top", fill="both", padx=(20, 20), pady=(40, 40))

        self.frame_login = ttkbootstrap.Frame(self.master)
        self.frame_login.pack(fill="both", expand=True, padx=10, pady=10)

        self.button_login = ttkbootstrap.Button(self.frame_login, text="Login", width=25, command=self.bin_login, cursor="hand2")

        if not Fool.effective:
            self.button_login.pack(side="bottom", padx=10, pady=(20, 100))

        else:
            self.button_login.configure(width=15)
            self.frame_login.bind("<Configure>", self._fool_configure_update)

        self.treeview_users.bind("<<TreeviewSelect>>", self.bin_users_TreeviewSelect, True)


    def update_user_list(self):
        self.userList = []
        path = core.env.base.home
        lst = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
        self.userList = lst


    def update_image_group(self):
        self.user_image = module.image.ImageTkThumbnailGroup(40, 40)
        for name in self.userList:
            for suffix in [".png", ".jpg"]:
                path = os.path.join(core.env.base.home, name, f"picture{suffix}")
                if os.path.isfile(path):
                    break
                else:
                    path = None

            if path is None: continue
            self.user_image.add_image(path, name)


    def update_treeview(self):
        for name in self.userList:
            self.treeview_users.insert("", "end", text=f"{name}", tags=(name,), image=self.user_image.get(name))


    def initial(self):
        core.log.info("初始化登录用户列表...", L.WINDOW_LOGIN)
        self.update_user_list()
        self.update_image_group()
        self.update_treeview()


    def bin_users_TreeviewSelect(self, *args):
        name = self.treeview_users.item(self.treeview_users.focus())["text"]
        if not name: return None
        path = os.path.join(core.env.base.home, name, "description.txt")
        if not os.path.isfile(path): return None

        self.label_description["text"] = ""

        try:
            for encodeing in ["utf-8", "gb18030"]:
                with open(path, "r", encoding=encodeing) as fileobject:
                    content = fileobject.read()

                    self.label_description["text"] = content
                    break

        except Exception:
            ...

        self._fool_first_place()


    def bin_login(self, *args):
        name = self.treeview_users.item(self.treeview_users.focus())["text"]
        if not name:
            window.messagebox.showerror(title="用户名为空", message="你没有选择要登录的用户\n不要偷懒好不好")
            return None

        try:
            core.login(name)

        except Exception as e:
            core.window.messagebox.showerror(title="操作异常", message=e)


    def _fool_first_place(self, *_):
        if not Fool.effective: return
        self.frame_login.update_idletasks()
        Fool.frame_width = self.frame_login.winfo_width()
        Fool.frame_height = self.frame_login.winfo_height()

        self.button_login.place(x=Fool.frame_width, y=Fool.frame_height)
        self.frame_login.update_idletasks()
        Fool.widget_width = self.button_login.winfo_width()
        Fool.widget_height = self.button_login.winfo_height()

        Fool.x = (Fool.frame_width - Fool.widget_width) // 2
        Fool.y = (Fool.frame_height - Fool.widget_height) // 2
        self.button_login.place(x=Fool.x, y=Fool.y)
        self._fool_update_range()
        self.frame_login.bind("<Motion>", self._fool_motion, None)


    def _fool_configure_update(self, *_):
        Fool.frame_width = self.frame_login.winfo_width()
        Fool.frame_height = self.frame_login.winfo_height()


    def _fool_update_range(self, *_):
        Fool.XL = Fool.x - Fool.widget_width // 2
        Fool.XR = Fool.x + Fool.widget_width // 2 + Fool.widget_width

        Fool.YT = Fool.y - Fool.widget_height
        Fool.YB = Fool.y + Fool.widget_height + Fool.widget_height


    def _fool_motion(self, event):
        px = event.x
        py = event.y

        if not Fool.XL < px < Fool.XR or not Fool.YT < py < Fool.YB: return

        oxs = (px - Fool.XL, px - Fool.XR)
        oys = (py - Fool.YT, py - Fool.YB)
        ox = oxs[0] if oxs[0] < abs(oxs[1]) else oxs[1]
        oy = oys[0] if oys[0] < abs(oys[1]) else oys[1]

        if abs(ox) > Fool.widget_width // 2:
            Fool.y += oy
        elif abs(oy) > Fool.widget_height // 2:
            Fool.x += ox
        else:
            Fool.y += oy
            Fool.x += ox


        self._fool_update_range()

        if Fool.XL < 0: Fool.x = Fool.frame_width - Fool.widget_width - Fool.widget_width // 2; Fool.count += 100
        if Fool.XR > Fool.frame_width: Fool.x = Fool.widget_width // 2; Fool.count += 100

        if Fool.YT < 0: Fool.y = Fool.frame_height - Fool.widget_height - Fool.widget_height; Fool.count += 100
        if Fool.YB > Fool.frame_height: Fool.y = Fool.widget_height; Fool.count += 100
        self._fool_update_range()

        self.button_login.place(x=Fool.x, y=Fool.y)

        Fool.count += 1
        if Fool.count > 1000:
            result = window.messagebox.askyesno(title="这屌按钮乱跑怎么办", message="是否受不了直接投降？\n\nY - 大丈夫能屈能伸\nN - 我决不会倒下")
            Fool.count = 0
            if not result: return
            self.frame_login.bind("<Motion>", lambda *_: None, None)
