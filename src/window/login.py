# -*- coding: utf-8 -*-

import os

import ttkbootstrap

import core
import module
import window

from constant import L


class Login(object):
    def __init__(self, master):
        self.master = master

        self.treeview_users = ttkbootstrap.Treeview(self.master, selectmode="extended", show="tree")
        self.treeview_users.column("#0", width=300, anchor="w")
        self.treeview_users.pack(side="left", fill="y", padx=20, pady=20)

        self.button_login = ttkbootstrap.Button(self.master, text="Login", width=25, command=self.bin_login, cursor="hand2")
        self.button_login.pack(side="bottom", padx=10, pady=(20, 100))

        self.label_description = ttkbootstrap.Label(self.master)
        self.label_description.pack(side="top", fill="both", padx=(20, 40), pady=(60, 40))

        self.treeview_users.bind("<<TreeviewSelect>>", self.bin_users_TreeviewSelect)


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


    def bin_login(self, *args):
        name = self.treeview_users.item(self.treeview_users.focus())["text"]
        if not name:
            window.messagebox.showerror(title="用户名为空", message="你没有选择要登录的用户\n不要偷懒好不好")
            return None

        try:
            core.login(name)

        except Exception as e:
            core.window.messagebox.showerror(title="操作异常", message=e)
