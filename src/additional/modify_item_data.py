# -*- coding: utf-8 -*-

# std
import os
import threading

# install
import win32gui
import ttkbootstrap

# project
import core


class selfstatus (object):
    action = threading.Lock()


class ModifyItemData (object):
    def __init__(self, SHA):
        result = selfstatus.action.acquire(timeout=0.01)
        if not result:
            core.UI.Messagebox.showerror(title='互斥锁请求超时', message='互斥锁正在被其他线程占用\n上一次操作未结束或锁没有被正确释放\n亦或是你想测试这个操作是不是线程安全的')
            return

        self.SHA = SHA

        self.windows = ttkbootstrap.Toplevel('修改 SHA 信息')

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

        self.Button_ok = ttkbootstrap.Button(self.windows, text='保存', width=10, bootstyle="info-outline", command=self.bin_ok)
        self.Button_cancel = ttkbootstrap.Button(self.windows, text='取消', width=10, bootstyle="success-outline", command=self.bin_cancel)
        self.Button_delete = ttkbootstrap.Button(self.windows, text='删除', width=10, bootstyle="danger-outline", command=self.bin_delete)
        self.Button_remove = ttkbootstrap.Button(self.windows, text='仅删除 Mod 文件', bootstyle="warning-outline", command=self.bin_remove)

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
        self.Button_cancel.pack(side='right', padx=(10, 0), pady=(0, 10))
        self.Button_delete.pack(side='right', padx=(10, 0), pady=(0, 10))
        self.Button_remove.pack(side='right', fill='x', expand=True, padx=(10, 0), pady=(0, 10))

        self.Label_except.pack(side='right', fill='x', expand=True, padx=(10, 0), pady=(0, 10))

        self.windows.protocol('WM_DELETE_WINDOW', self.bin_cancel)

        self.windows.update()

        width = self.windows.winfo_width()
        height = self.windows.winfo_height()

        _x, _y = win32gui.GetCursorInfo()[2]

        x = _x - width // 2
        y = _y - height // 2 - 20

        if x < 0: x = 0
        if y < 0: y = 0

        self.windows.geometry(f'+{x}+{y}')
        self.windows.resizable(False, False)


        data = core.Module.ModsIndex.get_item(self.SHA)

        self.old_object = data['object']
        self.old_name = data['name']
        self.old_explain = data.get('explain', '')
        self.old_grading = data.get('grading', '')
        self.old_tags = ' '.join(data.get('tags', []))

        self.Entry_object.insert(0, self.old_object)
        self.Entry_name.insert(0, self.old_name)
        self.Entry_explain.insert(0, self.old_explain)
        self.Combobox_grading.insert(0, self.old_grading)
        self.Entry_tags.insert(0, self.old_tags)


    def bin_ok(self, **args):
        s_object = self.Entry_object.get()
        s_name = self.Entry_name.get()
        s_grading = self.Combobox_grading.get()
        s_explain = self.Entry_explain.get()
        s_tags = self.Entry_tags.get()

        self.new_object = s_object.strip()
        self.new_name = s_name.strip()
        self.new_grading = s_grading[0] if s_grading else ''
        self.new_explain = s_explain.strip()
        self.new_tags = [x for x in s_tags.split(' ') if x]

        if not self.new_object:
            self.Label_except['text'] = '未填写 作用对象'
            return

        if not self.new_name:
            self.Label_except['text'] = '未填写 模组名称'
            return

        if not self.new_grading:
            self.Label_except['text'] = '未填写 年龄分级'
            return

        if self.new_grading not in ['G', 'P', 'R']:
            self.Label_except['text'] = '年龄分级 只能是 G P R 其中之一'
            return

        newdata = {
            'object': self.new_object,
            'name': self.new_name,
            'explain': self.new_explain,
            'grading': self.new_grading,
            'tags': self.new_tags
        }

        core.Module.ModsManage.unload(self.old_object)

        core.Module.ModsIndex.item_data_update(self.SHA, newdata)
        self.bin_cancel()

        core.Module.ModsManage.refresh()
        core.UI.ModsManage.bin_objects_TreeviewSelect()


    def bin_cancel(self, *args):
        self.windows.destroy()
        selfstatus.action.release()


    def bin_delete(self, *args):
        core.Module.ModsManage.unload(self.old_object)

        core.Module.ModsIndex.item_data_del(self.SHA)

        try:
            os.remove(os.path.join(core.environment.resources.mods, self.SHA))

        except Exception:
            ...

        self.bin_cancel()

        core.Module.ModsManage.refresh()
        core.UI.ModsManage.bin_objects_TreeviewSelect()


    def bin_remove(self, *args):
        core.Module.ModsManage.unload(self.old_object)

        try:
            os.remove(os.path.join(core.environment.resources.mods, self.SHA))

        except Exception:
            ...

        self.bin_cancel()

        core.Module.ModsManage.refresh()
        core.UI.ModsManage.bin_objects_TreeviewSelect()


def modify_item_data(*args):
    choice = core.UI.ModsManage.sbin_get_select_choices()
    if choice is None: return
    ModifyItemData(choice)
