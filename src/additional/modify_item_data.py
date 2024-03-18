# -*- coding: utf-8 -*-

# std
import os
import tkinter.filedialog
import threading

# install
import win32gui
import ttkbootstrap

# project
import core
from constant import *
import widgets


class selfstatus (object):
    action = threading.Lock()


class ModifyItemData (object):
    def __init__(self, master = ..., SHA: str = ...):
        result = selfstatus.action.acquire(timeout=0.01)
        if not result:
            core.window.messagebox.showerror(title='互斥锁请求超时', message='互斥锁正在被其他线程占用\n上一次操作未结束或锁没有被正确释放\n亦或是你想测试这个操作是不是线程安全的')
            return

        self.SHA = SHA
        self.master = master

        self._initial()


    def _initial(self):
        if self.master is Ellipsis:
            self.window = ttkbootstrap.Toplevel('修改 SHA 信息 - new construction options')
            core.window.methods.fake_withdraw(self.window)
            self.window.transient(core.window.mainwindow)
            # self.windows.grab_set()
            self.window.focus_set()
            # self.windows = tkinter.Toplevel(core.window.mainwindow)

            try:
                self.window.iconbitmap(default=core.env.file.local.iconbitmap)
                self.window.iconbitmap(bitmap=core.env.file.local.iconbitmap)
            except Exception:
                ...

            self.master = self.window
            self._initial_widget()
            self._final_window_update()

        else:
            self._initial_widget()


    def _initial_widget(self):
        width = 60

        self.kv_author = ttkbootstrap.StringVar()

        self.Label_SHA = ttkbootstrap.Label(self.master, text=f'SHA: {self.SHA}')

        self.Frame_object = ttkbootstrap.Frame(self.master)
        self.Entry_object = ttkbootstrap.Entry(self.Frame_object, width=width)
        self.Label_object = ttkbootstrap.Label(self.Frame_object, text='作用对象：')

        self.Frame_name = ttkbootstrap.Frame(self.master)
        self.Entry_name = ttkbootstrap.Entry(self.Frame_name, width=width)
        self.Label_name = ttkbootstrap.Label(self.Frame_name, text='模组名称：')

        self.Frame_author = ttkbootstrap.Frame(self.master)
        self.Entry_author = ttkbootstrap.Combobox(self.Frame_author, width=width, values=core.module.author_manage.get_authors_list(), textvariable=self.kv_author)
        self.Label_author = ttkbootstrap.Label(self.Frame_author, text='模组作者：')

        self.Frame_grading = ttkbootstrap.Frame(self.master)
        self.Combobox_grading = ttkbootstrap.Combobox(self.Frame_grading,
                                                      values=['G - 大众级', 'P - 指导级', 'R - 成人级', 'X - 限制级'])
        self.Label_grading = ttkbootstrap.Label(self.Frame_grading, text='年龄分级：')

        self.Frame_explain = ttkbootstrap.Frame(self.master)
        self.Entry_explain = ttkbootstrap.Entry(self.Frame_explain, width=width)
        self.Label_explain = ttkbootstrap.Label(self.Frame_explain, text='附加描述：')

        self.Frame_tags = ttkbootstrap.Frame(self.master)
        self.Entry_tags = ttkbootstrap.Entry(self.Frame_tags, width=width)
        self.Label_tags = ttkbootstrap.Label(self.Frame_tags, text='类型标签：')
        self.Button_tags = ttkbootstrap.Button(self.Frame_tags, text='+', bootstyle="success-outline", command=self.set_tags)

        self.Frame_get_1 = ttkbootstrap.Frame(self.master)
        self.Entry_url_1 = ttkbootstrap.Entry(self.Frame_get_1, width=width)
        self.Label_url_1 = ttkbootstrap.Label(self.Frame_get_1, text='下载地址：')
        self.Combobox_mode_1 = ttkbootstrap.Combobox(self.Frame_get_1, values=['get', 'lanzou'])

        self.Frame_get_2 = ttkbootstrap.Frame(self.master)
        self.Entry_url_2 = ttkbootstrap.Entry(self.Frame_get_2, width=width)
        self.Label_url_2 = ttkbootstrap.Label(self.Frame_get_2, text='下载地址：')
        self.Combobox_mode_2 = ttkbootstrap.Combobox(self.Frame_get_2, values=['get', 'lanzou'])

        self.Frame_get_3 = ttkbootstrap.Frame(self.master)
        self.Entry_url_3 = ttkbootstrap.Entry(self.Frame_get_3, width=width)
        self.Label_url_3 = ttkbootstrap.Label(self.Frame_get_3, text='下载地址：')
        self.Combobox_mode_3 = ttkbootstrap.Combobox(self.Frame_get_3, values=['get', 'lanzou'])

        self.Button_ok = ttkbootstrap.Button(self.master, text='保存', width=10, bootstyle="info-outline", command=self.bin_ok)
        self.Button_cancel = ttkbootstrap.Button(self.master, text='取消', width=10, bootstyle="success-outline", command=self.bin_cancel)
        self.Button_remove = ttkbootstrap.Button(self.master, text='删除', width=10, bootstyle="warning-outline", command=self.bin_remove)
        self.Button_delete = ttkbootstrap.Button(self.master, text='完全移除', width=10, bootstyle="danger-outline", command=self.bin_delete)

        self.Label_except = ttkbootstrap.Label(self.master, anchor='w', text='', foreground='red')

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

        self.Frame_author.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_author.pack(side='left', padx=(0, 5))
        self.Entry_author.pack(side='left', fill='x', expand=1)

        self.Frame_explain.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_explain.pack(side='left', padx=(0, 5))
        self.Entry_explain.pack(side='left', fill='x', expand=1)

        self.Frame_tags.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_tags.pack(side='left', padx=(0, 5))
        self.Entry_tags.pack(side='left', fill='x', expand=1)
        self.Button_tags.pack(side='left', padx=(5, 0))

        self.Frame_get_1.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_url_1.pack(side='left', padx=(0, 5))
        self.Combobox_mode_1.pack(side='right')
        self.Entry_url_1.pack(side='left', fill='x', expand=1)

        self.Frame_get_2.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_url_2.pack(side='left', padx=(0, 5))
        self.Combobox_mode_2.pack(side='right')
        self.Entry_url_2.pack(side='left', fill='x', expand=1)

        self.Frame_get_3.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Label_url_3.pack(side='left', padx=(0, 5))
        self.Combobox_mode_3.pack(side='right')
        self.Entry_url_3.pack(side='left', fill='x', expand=1)

        # self.Frame_mode.pack(side='top', fill='x', padx=10, pady=(0, 10))
        # self.Label_mode.pack(side='left', padx=(0, 5))
        # self.Combobox_mode.pack(side='left', fill='x', expand=1)

        self.Button_ok.pack(side='right', padx=10, pady=(0, 10))
        self.Button_cancel.pack(side='right', padx=(10, 0), pady=(0, 10))
        self.Button_remove.pack(side='right', padx=(10, 0), pady=(0, 10))
        self.Button_delete.pack(side='right', padx=(10, 0), pady=(0, 10))

        self.Label_except.pack(side='right', fill='x', expand=True, padx=(10, 0), pady=(0, 10))

        self.master.protocol('WM_DELETE_WINDOW', self.bin_cancel)

        _alt_set = core.window.annotation_toplevel.register
        _alt_set(self.Label_SHA, T.ANNOTATION_SHA, 2)
        _alt_set(self.Entry_object, T.ANNOTATION_OBJECT, 2)
        _alt_set(self.Entry_name, T.ANNOTATION_NAME, 2)
        _alt_set(self.Entry_author, T.ANNOTATION_AUTHOR, 2)
        _alt_set(self.Combobox_grading, T.ANNOTATION_GRADING, 2)
        _alt_set(self.Entry_explain, T.ANNOTATION_EXPLAIN, 2)
        _alt_set(self.Entry_tags, T.ANNOTATION_TAGS, 2)
        _alt_set(self.Entry_url_1, T.ANNOTATION_GET_URL, 2)
        _alt_set(self.Entry_url_2, T.ANNOTATION_GET_URL, 2)
        _alt_set(self.Entry_url_3, T.ANNOTATION_GET_URL, 2)
        _alt_set(self.Combobox_mode_1, T.ANNOTATION_GET_MODE, 2)
        _alt_set(self.Combobox_mode_2, T.ANNOTATION_GET_MODE, 2)
        _alt_set(self.Combobox_mode_3, T.ANNOTATION_GET_MODE, 2)
        _alt_set(self.Button_ok, T.ANNOTATION_MODIFY_ITEM_OK, 2)
        _alt_set(self.Button_cancel, T.ANNOTATION_MODIFY_ITEM_CANCEL, 2)
        _alt_set(self.Button_remove, T.ANNOTATION_MODIFY_ITEM_REMOVE, 1)
        _alt_set(self.Button_delete, T.ANNOTATION_MODIFY_ITEM_DELETE, 1)

        data = core.module.mods_index.get_item(self.SHA)

        self.old_object = data['object']
        self.old_name = data['name']
        self.old_explain = data.get('explain', '').replace("\n", "\\n")
        self.old_grading = data.get('grading', '')
        self.old_author = data.get('author', '')
        self.old_tags = ' '.join(data.get('tags', []))

        self.Entry_object.insert(0, self.old_object)
        self.Entry_name.insert(0, self.old_name)
        self.Entry_explain.insert(0, self.old_explain)
        self.Entry_author.insert(0, self.old_author)
        self.Combobox_grading.insert(0, self.old_grading)
        self.Entry_tags.insert(0, self.old_tags)

        self.old_gets = data.get('get', [])

        for index_, get_ in enumerate(self.old_gets):
            if index_ == 0:
                self.Entry_url_1.insert(0, get_.get('url', ''))
                self.Combobox_mode_1.insert(0, get_.get('mode', ''))

            elif index_ == 1:
                self.Entry_url_2.insert(0, get_.get('url', ''))
                self.Combobox_mode_2.insert(0, get_.get('mode', ''))

            elif index_ == 2:
                self.Entry_url_3.insert(0, get_.get('url', ''))
                self.Combobox_mode_3.insert(0, get_.get('mode', ''))

            else:
                core.window.messagebox.showwarning(title='数据超出处理长度', message='get 数据数量超出处理长度\n修改会导致超出的部分数据丢失')

        self.kv_author.trace_add("write", self._event_author_name_updated)


    def _event_author_name_updated(self, *_):
        self.Entry_author.configure(values=core.module.author_manage.get_key_authors(self.kv_author.get()))
        # self.Entry_author.open() # ? 为什么这里有一个意义不明的调用


    def _final_window_update(self):
        self.master.update()
        core.window.methods.center_window_for_window(self.master, core.window.mainwindow)
        self.master.resizable(False, False)


    def set_tags(self, *_):
        o_tags = core.module.tags_manage.get_tags()
        s_tags = self.Entry_tags.get()
        res = widgets.dialogs.select2ags("选择标签", o_tags, s_tags, parent=self.master)
        self.Entry_tags.delete(0, 'end')
        self.Entry_tags.insert(0, res)


    def bin_ok(self, **args):
        s_object = self.Entry_object.get()
        s_name = self.Entry_name.get()
        s_grading = self.Combobox_grading.get()
        s_explain = self.Entry_explain.get()
        s_author = self.Entry_author.get()
        s_tags = self.Entry_tags.get()

        self.new_object = s_object.strip()
        self.new_name = s_name.strip()
        self.new_grading = s_grading[0] if s_grading else ''
        self.new_explain = s_explain.strip().replace("\\n", "\n")
        self.new_tags = [x for x in s_tags.split(' ') if x]
        self.new_author = s_author.strip()

        s_get = [
            {
                'url': self.Entry_url_1.get().strip(),
                'mode': self.Combobox_mode_1.get().strip()
            },
            {
                'url': self.Entry_url_2.get().strip(),
                'mode': self.Combobox_mode_2.get().strip()
            },
            {
                'url': self.Entry_url_3.get().strip(),
                'mode': self.Combobox_mode_3.get().strip()
            },
        ]

        self.new_get = []

        for data_ in s_get:
            if not data_['url']:
                continue

            else:
                self.new_get.append(data_)

        if not self.new_object:
            self.Label_except['text'] = '未填写 作用对象'
            return

        if not self.new_name:
            self.Label_except['text'] = '未填写 模组名称'
            return

        if not self.new_grading:
            self.Label_except['text'] = '未填写 年龄分级'
            return

        if self.new_grading not in ['G', 'P', 'R', 'X']:
            self.Label_except['text'] = '年龄分级 只能是 G P R X 其中之一'
            return

        for data_ in self.new_get:
            if data_['mode'] not in ['get', 'lanzou']:
                self.Label_except['text'] = '下载模式只能是 get 或 lanzou'
                return

        newdata = {
            'object': self.new_object,
            'name': self.new_name,
            'explain': self.new_explain,
            'grading': self.new_grading,
            'author': self.new_author,
            'get': self.new_get,
            'tags': self.new_tags
        }

        if self.old_object != self.new_object:
            core.module.mods_manage.unload(self.old_object)

        core.module.mods_index.item_data_update(self.SHA, newdata)
        self.bin_cancel()


    def bin_cancel(self, *args):
        self.master.destroy()
        core.window.annotation_toplevel.withdraw()
        selfstatus.action.release()


    def bin_delete(self, *args):
        # core.module.mods_manage.unload(self.old_object)
        result = core.module.mods_manage.remove(self.SHA)
        if result is not None:
            core.window.messagebox.showinfo(title=result[0], message=result[1])
            return

        core.module.mods_index.item_data_del(self.SHA)

        try:
            os.remove(os.path.join(core.env.directory.resources.mods, self.SHA))

        except Exception:
            ...

        core.construct.event.set_event(E.MODS_INDEX_UPDATE)
        self.bin_cancel()


    def bin_remove(self, *args):
        result = core.module.mods_manage.remove(self.SHA)
        if result is not None:
            core.window.messagebox.showinfo(title=result[0], message=result[1])
            return

        try:
            os.remove(os.path.join(core.env.directory.resources.mods, self.SHA))

        except Exception:
            ...

        core.construct.event.set_event(E.MODS_INDEX_UPDATE)
        self.bin_cancel()


def modify_item_data(sha: str = None):
    if isinstance(sha, str):
        ...

    else:
        sha = core.window.interface.mods_manage.value_choice_item
        if not core.window.interface.mods_manage._is_valid_sha(sha):
            sha = core.window.interface.mods_manage.sbin_get_select_choices()
            if sha is None: return
    if core.module.mods_index.get_item(sha) is None: return
    ModifyItemData(SHA=sha)
