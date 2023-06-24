# -*- coding: utf-8 -*-

import os

import ttkbootstrap

import core
import module
import windows


class Login(object):
    def __init__(self, master):
        self.master = master

        self.Treeview_users = ttkbootstrap.Treeview(self.master, selectmode='extended', show='tree')
        self.Treeview_users.column('#0', width=300, anchor='w')
        self.Treeview_users.pack(side='left', fill='y', padx=20, pady=20)

        self.Button_login = ttkbootstrap.Button(self.master, text='Login', width=25, command=self.bin_login)
        self.Button_login.pack(side='bottom', padx=10, pady=(20, 100))

        self.Label_description = ttkbootstrap.Label(self.master)
        self.Label_description.pack(side='top', fill='both', padx=(20, 40), pady=(60, 40))

        self.Treeview_users.bind('<<TreeviewSelect>>', self.bin_users_TreeviewSelect)

    def update_userList(self):
        self.userList = []
        path = core.environment.root.home
        lst = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
        self.userList = lst

    def update_imageGroup(self):
        self.userImage = module.image.ImageTkThumbnailGroup(40, 40)
        for name in self.userList:
            for suffix in ['.png', '.jpg']:
                path = os.path.join(core.environment.root.home, name, f'picture{suffix}')
                if os.path.isfile(path):
                    break
                else:
                    path = None

            if path is None: continue
            self.userImage.add_image(path, name)

    def update_treeview(self):
        for name in self.userList:
            self.Treeview_users.insert('', 'end', text=f'{name}', tags=(name,), image=self.userImage.get(name))

    def initial(self):
        self.update_userList()
        self.update_imageGroup()
        self.update_treeview()

    def bin_users_TreeviewSelect(self, *args):
        name = self.Treeview_users.item(self.Treeview_users.focus())['text']
        if not name: return None
        path = os.path.join(core.environment.root.home, name, 'description.txt')
        if not os.path.isfile(path): return None

        self.Label_description['text'] = ''

        try:
            for encodeing in ['utf-8', 'gb18030']:
                with open(path, 'r', encoding=encodeing) as fileobject:
                    content = fileobject.read()

                    self.Label_description['text'] = content
                    break

        except Exception:
            ...

    def bin_login(self, *args):
        name = self.Treeview_users.item(self.Treeview_users.focus())['text']
        if not name:
            windows.Messagebox.showerror(title='用户名为空', message='你没有选择要登录的用户\n不要偷懒好不好')
            return None

        core.login(name)
