# -*- coding: utf-8 -*-

import os

import webbrowser
import ttkbootstrap

import core


class ModsWarehouse(object):
    def GUI_install(self, master, *args, **kwds):
        self.master = master
        titles = (('#0', 'SHA / object :: name', 460), ('enabled', 'tags', 380))

        self.Frame_list = ttkbootstrap.Frame(self.master)
        self.Frame_list.pack(side='left', fill='y')

        self.Entry_search = ttkbootstrap.Entry(self.Frame_list)
        self.Treeview_items = ttkbootstrap.Treeview(self.Frame_list, show='tree headings', selectmode='extended', columns=('enabled',))
        self.Scrollbar_items = ttkbootstrap.Scrollbar(self.Frame_list, command=self.Treeview_items.yview)
        self.Frame_Button = ttkbootstrap.Frame(self.master)
        self.Button_download = ttkbootstrap.Button(self.Frame_Button, text='添加到下载列表', width=10, command=self.bin_download)
        self.Button_open_url = ttkbootstrap.Button(self.Frame_Button, text='在浏览器上查看', width=10, command=self.bin_open_url)
        self.Label_preview = ttkbootstrap.Label(self.master, anchor='center', text='无预览图')

        self.Entry_search.pack(side='bottom', fill='x', padx=10, pady=10)
        self.Scrollbar_items.pack(side='right', fill='y', padx=(0, 10), pady=(10, 0))
        self.Treeview_items.pack(side='left', fill='y', padx=(10, 5), pady=(10, 0))
        self.Frame_Button.pack(side='bottom', fill='x', padx=(0, 10), pady=10)
        self.Button_download.pack(side='left', fill='x', expand=1, padx=0, pady=0)
        self.Button_open_url.pack(side='right', fill='x', expand=1, padx=(10, 0), pady=0)
        self.Label_preview.pack(side='top', fill='both', padx=(0, 10), pady=(10, 0), expand=1)


        self.Treeview_items.config()
        self.Treeview_items.config(yscrollcommand=self.Scrollbar_items.set)

        self.Treeview_items.bind('<<TreeviewSelect>>', self.bin_items_TreeviewSelect)
        self.Entry_search.bind('<Return>', self.bin_refresh)
        # self.Entry_search.bind('<Key>', self.bin_refresh)
        for tree, text, width in titles:
            self.Treeview_items.column(tree, width=width, anchor='w')
            self.Treeview_items.heading(tree, text=text)


    def __init__(self, master):
        self.GUI_install(master)


    def __dict_item_conform_one(self, SHA: str, item: dict, search: str = '') -> bool:
        if search == '': return True
        if search in SHA: return True
        if search in item['name']: return True
        if search in item['object']: return True
        if search in item.get('grading', 'x'): return True
        if search in ", ".join(item.get('tags', [])): return True
        else: return False


    def __dict_item_conform(self, SHA: str, item: dict, search: str = '') -> bool:
        search_lst = search.split(' ')
        for search_ in search_lst:
            if not self.__dict_item_conform_one(SHA, item, search_):
                return False
        return True


    def refresh(self, search: str = ''):
        [self.Treeview_items.delete(row) for row in self.Treeview_items.get_children()]
        lst = core.Module.ModsIndex.get_all_SHA_list()
        for SHA in lst:
            item = core.Module.ModsIndex.get_item(SHA)
            if not item.get('get', None): continue
            try:
                if not self.__dict_item_conform(SHA, item, search): continue
                object_ = item['object']
                name = item['name']
                grading = item.get('grading', 'x')
                tags = ', '.join(item.get('tags', []))
                local_ = core.Module.ModsManage.is_local_SHA(SHA)

                islocal = ' [已下载]' if local_ else ''

                text = f'{SHA}\n{object_} :: {name}'
                values = (f'[{tags}]\n[{grading}]{islocal}', )

                image = core.content.ThumbnailGroup.get(object_)

                self.Treeview_items.insert('', 'end', text=text, values=values, image=image, tags=(SHA, ))

            except Exception:
                ...


    def sbin_update_preview(self, SHA: str | None = None):
        if SHA is None:
            self.Label_preview.config(image='')
            self.Label_preview.config(text='无预览图')
            return
        width = self.Label_preview.winfo_width()
        height = self.Label_preview.winfo_height()
        self.__image = core.module.image.get_preview_image(SHA, width, height)
        if self.__image is None: self.sbin_update_preview(None)
        else: self.Label_preview.config(image=self.__image)


    def bin_items_TreeviewSelect(self, *args):
        tags = self.Treeview_items.item(self.Treeview_items.focus())['tags']
        if not tags: SHA = None
        else: SHA = tags[0]
        self.sbin_update_preview(SHA)


    def bin_download(self, *args, **kwds):
        tags = self.Treeview_items.item(self.Treeview_items.focus())['tags']
        if not tags: SHA = None
        else: SHA = tags[0]
        if SHA == None:
            core.UI.Messagebox.showerror(title='数据错误', message='数据值为空\n请先选择需要下载的 Mod')
            return
        else:
            core.control.addTask(f'下载 {SHA}', core.Module.ModsDownload.downloadTask, (SHA, ))


    def bin_open_url(self, *args, **kwds):
        tags = self.Treeview_items.item(self.Treeview_items.focus())['tags']
        if not tags: SHA = None
        else: SHA = tags[0]
        if SHA == None:
            core.UI.Messagebox.showerror(title='数据错误', message='数据值为空\n请先选择需要下载的 Mod')
            return
        else:
            item = core.Module.ModsIndex.get_item(SHA)
            webbrowser.open(item['get'][0]['url'])


    def bin_refresh(self, *args, **kwds):
        key = self.Entry_search.get()
        self.refresh(key)

