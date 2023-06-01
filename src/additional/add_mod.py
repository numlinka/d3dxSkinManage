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



class AddModInputCache(object):
    object_ = ''
    grading = ''
    explain = ''
    tags = ''



class AddMods(object):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.basename = os.path.basename(filepath)
        self.suffix = self.basename[self.basename.rfind('.') + 1:]
        self.prefix = self.basename[:self.basename.rfind('.')]

        with open(self.filepath, 'rb') as fileobject:
            self.content = fileobject.read()
            sha1 = hashlib.sha1()
            sha1.update(self.content)
            self.SHA = sha1.hexdigest().upper()

        self.object_ = core.UI.ModsManage.sbin_get_select_objects()
        self.object_ = self.object_ if self.object_ else ''

        self.windows = ttkbootstrap.Toplevel('添加 Mod')

        try:
            self.windows.iconbitmap(default=core.environment.local.iconbitmap)
            self.windows.iconbitmap(bitmap=core.environment.local.iconbitmap)
        except Exception:
            ...

        width = 60

        self.Label_SHA = ttkbootstrap.Label(self.windows, text=f'SHA: {self.SHA}')

        self.Frame_object = ttkbootstrap.Frame(self.windows)
        self.Entry_object = ttkbootstrap.Entry(self.Frame_object, width=width)
        self.Label_object = ttkbootstrap.Label(self.Frame_object, text='作用对象：')

        self.Frame_name = ttkbootstrap.Frame(self.windows)
        self.Entry_name = ttkbootstrap.Entry(self.Frame_name, width=width)
        self.Label_name = ttkbootstrap.Label(self.Frame_name, text='模组名称：')

        self.Frame_grading = ttkbootstrap.Frame(self.windows)
        self.Combobox_grading = ttkbootstrap.Combobox(self.Frame_grading,
                                                      values=['G - 大众级', 'P - 指导级', 'R - 成人级'])
        self.Label_grading = ttkbootstrap.Label(self.Frame_grading, text='年龄分级：')

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
        self.Entry_object.pack(side='left', fill='x', expand=1)

        self.Frame_name.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_name.pack(side='left', padx=(0, 5))
        self.Entry_name.pack(side='left', fill='x', expand=1)

        self.Frame_grading.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_grading.pack(side='left', padx=(0, 5))
        self.Combobox_grading.pack(side='left', fill='x', expand=1)

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

        core.UI.Windows.update()
        time.sleep(0.01)

        width = self.windows.winfo_width()
        height = self.windows.winfo_height()

        _x, _y = win32gui.GetCursorInfo()[2]

        x = _x - width // 2
        y = _y - height // 2 - 20

        if x < 0: x = 0
        if y < 0: y = 0

        self.windows.geometry(f'+{x}+{y}')

        self.windows.resizable(False, False)

        # 输入初始值
        if self.object_:
            self.Entry_object.insert(0, self.object_)
        else:
            self.Entry_object.insert(0, AddModInputCache.object_)

        self.Entry_name.insert(0, self.prefix)

        if AddModInputCache.grading:
            self.Combobox_grading.insert(0, AddModInputCache.grading)
        else:
            self.Combobox_grading.insert(0, 'G - 大众级')

        self.Entry_explain.insert(0, AddModInputCache.explain)
        self.Entry_tags.insert(0, AddModInputCache.tags)

    def bin_open_help(self, *args, **kwds):
        webbrowser.open('http://d3dxskinmanage.numlinka.com/#/enhance/001')

    def bin_ok(self, *args, **kwds):
        s_object = self.Entry_object.get()
        s_name = self.Entry_name.get()
        s_grading = self.Combobox_grading.get()
        s_explain = self.Entry_explain.get()
        s_tags = self.Entry_tags.get()

        z_object = s_object.strip()
        z_name = s_name.strip()
        z_grading = s_grading[0] if s_grading else ''
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

        filepath = os.path.join(core.environment.user.modsIndex, 'self-index.json')
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as fileobject:
                    filecontent = fileobject.read()

                datacontent = json.loads(filecontent)

            except Exception:
                core.UI.Messagebox.showerror(title='数据序列化错误', message='索引文件数据反序列化错误\n请检查 self-index.json 文件是否损坏')
                return

        else:
            datacontent = {}

        if 'mods' not in datacontent: datacontent['mods'] = {}
        datacontent['mods'][self.SHA] = {
            'object': z_object,
            'type': self.suffix,
            'name': z_name,
            'explain': z_explain,
            'grading': z_grading,
            'tags': z_tags
        }

        newfilecontent = json.dumps(datacontent, ensure_ascii=False, sort_keys=False, indent=4)

        try:
            with open(filepath, 'w', encoding='utf-8') as fileobject:
                fileobject.write(newfilecontent)

        except Exception:
            core.UI.Messagebox.showerror(title='未知错误', message='数据文件保存错误\n未知错误')
            return

        try:
            with open(os.path.join(core.environment.resources.mods, self.SHA), 'wb') as fileobject:
                fileobject.write(self.content)

        except Exception:
            core.UI.Messagebox.showerror(title='未知错误', message='Mod 文件保存错误\n未知错误')
            return

        self.windows.destroy()
        core.control.addTask('重载私有索引文件', core.Module.IndexManage.load_file,
                             ('self-index.json', 'json', 'cover'))
        core.control.addTask('重载 Mods 管理', core.Module.ModsManage.refresh)

        if self.object_ == z_object:
            core.control.addTask('刷新对象列表', core.UI.ModsManage.bin_objects_TreeviewSelect)

        else:
            core.control.addTask('刷新分类列表', core.UI.ModsManage.reload_classification)

        # 保存输入记忆
        AddModInputCache.object_ = z_object
        AddModInputCache.grading = s_grading
        AddModInputCache.tags = s_tags
        AddModInputCache.explain = z_explain
