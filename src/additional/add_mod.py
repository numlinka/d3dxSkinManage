# -*- coding: utf-8 -*-

# std
import os
import json
import time
import hashlib

# install
import win32gui
import webbrowser
import ttkbootstrap

# project
import core
from constant import *



class AddModInputCache(object):
    object_ = ''
    grading = ''
    explain = ''
    tags = ''
    author = ''



class AddMods(object):
    def __init__(self, filepath: str, filename: str = None):
        self.filepath = filepath
        self.basename = os.path.basename(filepath)
        self.suffix = self.basename[self.basename.rfind('.') + 1:]
        self.prefix = self.basename[:self.basename.rfind('.')] if not isinstance(filename, str) else filename

        with open(self.filepath, 'rb') as fileobject:
            self.content = fileobject.read()
            sha1 = hashlib.sha1()
            sha1.update(self.content)
            self.SHA = sha1.hexdigest().upper()


        # 如果 index 里面已经存储过该 SHA 的数据则直接保存 Mod 文件
        if core.module.mods_index.get_item(self.SHA) is not None:
            try:
                with open(os.path.join(core.env.directory.resources.mods, self.SHA), 'wb') as fileobject:
                    fileobject.write(self.content)

            except Exception:
                core.window.messagebox.showerror(title='未知错误', message='Mod 文件保存错误\n未知错误')
                return

            core.construct.event.set_event(E.MODS_INDEX_UPDATE)
            return


        self.object_ = core.window.interface.mods_manage.sbin_get_select_objects()
        self.object_ = self.object_ if self.object_ else ''

        self.windows = ttkbootstrap.Toplevel('添加 Mod')
        self.windows.transient(core.window.mainwindow)
        # self.windows.grab_set()

        try:
            self.windows.iconbitmap(default=core.env.file.local.iconbitmap)
            self.windows.iconbitmap(bitmap=core.env.file.local.iconbitmap)
        except Exception:
            ...

        width = 60

        self.Label_SHA = ttkbootstrap.Label(self.windows, text=f'SHA: {self.SHA}')

        self.Frame_object = ttkbootstrap.Frame(self.windows)
        self.Combobox_object = ttkbootstrap.Combobox(self.Frame_object, width=width)
        self.Label_object = ttkbootstrap.Label(self.Frame_object, text='作用对象：')

        self.Frame_name = ttkbootstrap.Frame(self.windows)
        self.Entry_name = ttkbootstrap.Entry(self.Frame_name, width=width)
        self.Label_name = ttkbootstrap.Label(self.Frame_name, text='模组名称：')

        self.Frame_grading = ttkbootstrap.Frame(self.windows)
        self.Combobox_grading = ttkbootstrap.Combobox(self.Frame_grading,
                                                      values=['G - 大众级', 'P - 指导级', 'R - 成人级'])
        self.Label_grading = ttkbootstrap.Label(self.Frame_grading, text='年龄分级：')

        self.Frame_author = ttkbootstrap.Frame(self.windows)
        self.Entry_author = ttkbootstrap.Entry(self.Frame_author, width=width)
        self.Label_author = ttkbootstrap.Label(self.Frame_author, text='模组作者：')

        self.Frame_explain = ttkbootstrap.Frame(self.windows)
        self.Entry_explain = ttkbootstrap.Entry(self.Frame_explain, width=width)
        self.Label_explain = ttkbootstrap.Label(self.Frame_explain, text='附加描述：')

        self.Frame_tags = ttkbootstrap.Frame(self.windows)
        self.Entry_tags = ttkbootstrap.Entry(self.Frame_tags, width=width)
        self.Label_tags = ttkbootstrap.Label(self.Frame_tags, text='类型标签：')

        self.Frame_url = ttkbootstrap.Frame(self.windows)
        self.Entry_url = ttkbootstrap.Entry(self.Frame_url, width=width)
        self.Label_url = ttkbootstrap.Label(self.Frame_url, text='下载地址：')

        self.Frame_mode = ttkbootstrap.Frame(self.windows)
        self.Combobox_mode = ttkbootstrap.Combobox(self.Frame_mode, values=['get', 'lanzou'])
        self.Label_mode = ttkbootstrap.Label(self.Frame_mode, text='下载模式：')

        self.Button_ok = ttkbootstrap.Button(self.windows, text='确定', width=10, command=self.bin_ok)
        self.Button_help = ttkbootstrap.Button(self.windows, text='帮助', width=10, command=self.bin_open_help)

        self.Label_except = ttkbootstrap.Label(self.windows, anchor='w', text='', foreground='red')

        self.Label_SHA.pack(side='top', fill='x', padx=10, pady=10)

        self.Frame_object.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_object.pack(side='left', padx=(0, 5))
        self.Combobox_object.pack(side='left', fill='x', expand=1)

        self.Frame_name.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_name.pack(side='left', padx=(0, 5))
        self.Entry_name.pack(side='left', fill='x', expand=1)

        self.Frame_grading.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_grading.pack(side='left', padx=(0, 5))
        self.Combobox_grading.pack(side='left', fill='x', expand=1)

        self.Frame_author.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_author.pack(side='left', padx=(0, 5))
        self.Entry_author.pack(side='left', fill='x', expand=1)

        self.Frame_explain.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_explain.pack(side='left', padx=(0, 5))
        self.Entry_explain.pack(side='left', fill='x', expand=1)

        self.Frame_tags.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_tags.pack(side='left', padx=(0, 5))
        self.Entry_tags.pack(side='left', fill='x', expand=1)

        # self.Frame_url.pack(side='top', fill='x', padx=10, pady=(0, 10))
        # self.Label_url.pack(side='left', padx=(0, 5))
        # self.Entry_url.pack(side='left', fill='x', expand=1)

        # self.Frame_mode.pack(side='top', fill='x', padx=10, pady=(0, 10))
        # self.Label_mode.pack(side='left', padx=(0, 5))
        # self.Combobox_mode.pack(side='left', fill='x', expand=1)

        self.Button_ok.pack(side='right', padx=10, pady=(0, 10))
        self.Button_help.pack(side='right', padx=(10, 0), pady=(0, 10))

        self.Label_except.pack(side='right', fill='x', expand=True, padx=(10, 0), pady=(0, 10))

        _alt_set = core.window.annotation_toplevel.register
        _alt_set(self.Label_SHA, T.ANNOTATION_SHA)
        _alt_set(self.Combobox_object, T.ANNOTATION_OBJECT)
        _alt_set(self.Entry_name, T.ANNOTATION_NAME)
        _alt_set(self.Entry_author, T.ANNOTATION_AUTHOR)
        _alt_set(self.Combobox_grading, T.ANNOTATION_GRADING)
        _alt_set(self.Entry_explain, T.ANNOTATION_EXPLAIN)
        _alt_set(self.Entry_tags, T.ANNOTATION_TAGS)
        _alt_set(self.Button_ok, T.ANNOTATION_ADD_MOD_OK)
        _alt_set(self.Button_help, T.ANNOTATION_ADD_MOD_HELP)


        core.window.mainwindow.update()

        width = self.windows.winfo_width()
        height = self.windows.winfo_height()

        _x, _y = win32gui.GetCursorInfo()[2]

        x = _x - width // 2
        y = _y - height // 2 - 20

        if x < 0: x = 0
        if y < 0: y = 0

        self.windows.geometry(f'+{x}+{y}')

        self.windows.resizable(False, False)

        # 如果 SHA 是全新的则根据操作环境推断

        class_name = core.window.interface.mods_manage.sbin_get_select_classification()
        if class_name is not None:
            object_list = core.module.mods_manage.get_reference_object_list(class_name)
            self.Combobox_object.config(values=object_list)

        if self.object_:
            self.Combobox_object.insert(0, self.object_)
        else:
            self.Combobox_object.insert(0, AddModInputCache.object_)

        self.Entry_name.insert(0, self.prefix)

        if AddModInputCache.grading:
            self.Combobox_grading.insert(0, AddModInputCache.grading)
        else:
            self.Combobox_grading.insert(0, 'G - 大众级')

        self.Entry_author.insert(0, AddModInputCache.author)
        self.Entry_explain.insert(0, AddModInputCache.explain)
        self.Entry_tags.insert(0, AddModInputCache.tags)


    def bin_open_help(self, *args, **kwds):
        webbrowser.open('http://d3dxskinmanage.numlinka.com/#/enhance/001')


    def bin_ok(self, *args, **kwds):
        s_object = self.Combobox_object.get()
        s_name = self.Entry_name.get()
        s_grading = self.Combobox_grading.get()
        s_author = self.Entry_author.get()
        s_explain = self.Entry_explain.get()
        s_tags = self.Entry_tags.get()

        z_object = s_object.strip()
        z_name = s_name.strip()
        z_grading = s_grading[0] if s_grading else ''
        z_author = s_author.strip()
        z_explain = s_explain.strip()
        z_tags = [x for x in s_tags.split(' ') if x]

        if not z_object:
            self.Label_except['text'] = '未填写 作用对象'
            return

        if not z_name:
            self.Label_except['text'] = '未填写 模组名称'
            return

        if not z_grading:
            self.Label_except['text'] = '未填写 年龄分级'
            return

        if z_grading not in ['G', 'P', 'R']:
            self.Label_except['text'] = '年龄分级 只能是 G P R 其中之一'
            return

        filepath = os.path.join(core.userenv.directory.mods_index, 'self-index.json')

        datacontent = {
            'object': z_object,
            'type': self.suffix,
            'name': z_name,
            'author': z_author,
            'grading': z_grading,
            'explain': z_explain,
            'tags': z_tags
        }

        try:
            with open(os.path.join(core.env.directory.resources.mods, self.SHA), 'wb') as fileobject:
                fileobject.write(self.content)

        except Exception:
            core.window.messagebox.showerror(title='未知错误', message='Mod 文件保存错误\n未知错误')
            return

        core.module.mods_index.item_data_new(filepath, self.SHA, datacontent)
        self.windows.destroy()

        # 保存输入记忆
        AddModInputCache.object_ = z_object
        AddModInputCache.grading = s_grading
        AddModInputCache.tags = s_tags
        AddModInputCache.explain = z_explain
        AddModInputCache.author = z_author
        core.window.annotation_toplevel.withdraw()



def add_mod_is_dir(dirpath: str):
    basename = os.path.basename(dirpath)
    tempfilename = hex(int(time.time() * 10 ** 8)) + '.7z'
    tempfilepath = os.path.join(core.env.directory.resources.cache, tempfilename)
    core.external.a7z(os.path.join(dirpath, '*'), tempfilepath)
    AddMods(tempfilepath, basename)
    os.remove(tempfilepath)
