# -*- coding: utf-8 -*-

import tkinter
import ttkbootstrap

import core


class ModsManage(object):
    def GUI_initial(self, *args, **kwds):
        titles = (('#0', '对象', 200), ('enabled', '启用 Mod', 240))

        self.Treeview_classification = ttkbootstrap.Treeview(self.master, show='tree headings', selectmode='extended')
        self.Treeview_objects = ttkbootstrap.Treeview(self.master, show='tree headings', selectmode='extended', columns=('enabled',))
        self.Treeview_choices = ttkbootstrap.Treeview(self.master, selectmode='extended', show='tree headings')

        self.Scrollbar_classification = ttkbootstrap.Scrollbar(self.master, command=self.Treeview_classification.yview)
        self.Scrollbar_objects = ttkbootstrap.Scrollbar(self.master, command=self.Treeview_objects.yview)
        self.Scrollbar_choices = ttkbootstrap.Scrollbar(self.master, command=self.Treeview_choices.yview)

        self.Label_explain = ttkbootstrap.Label(self.master, anchor='center', text='无附加描述')
        self.Label_SHA = ttkbootstrap.Label(self.master, anchor='center', text='SHA')
        self.Label_preview = ttkbootstrap.Label(self.master, anchor='center', text='无预览图')

        self.Button_refresh = ttkbootstrap.Button(self.master, text='刷新列表', command=self.bin_refresh)


        self.Treeview_classification.config(yscrollcommand=self.Scrollbar_classification.set)
        self.Treeview_objects.config(yscrollcommand=self.Scrollbar_objects.set)
        self.Treeview_choices.config(yscrollcommand=self.Scrollbar_choices.set)

        self.Treeview_classification.column('#0', width=200, anchor='w')
        self.Treeview_classification.heading('#0', text='分类')
        self.Treeview_choices.heading('#0', text='选择')

        for tree, text, width in titles:
            self.Treeview_objects.column(tree, width=width, anchor='w')
            self.Treeview_objects.heading(tree, text=text)


        self.Treeview_classification.pack(side='left', fill='y', padx=(10, 0), pady=10)
        self.Scrollbar_classification.pack(side='left', fill='y', padx=(2, 5), pady=10)
        self.Treeview_objects.pack(side='left', fill='y', padx=(0, 0), pady=10)
        self.Scrollbar_objects.pack(side='left', fill='y', padx=(2, 5), pady=10)
        self.Treeview_choices.pack(side='left', fill='y', padx=(0, 0), pady=10)
        self.Scrollbar_choices.pack(side='left', fill='y', padx=(2, 10), pady=10)
        self.Label_SHA.pack(side='top',fill='x', padx=(0, 10), pady=(10, 5))
        self.Label_explain.pack(side='bottom', fill='x', padx=(0, 10), pady=(5, 10))
        self.Label_preview.pack(side='top', fill='both', padx=(0, 10), pady=0, expand=1)
        # self.Button_refresh.pack(side='top', fill='x', padx=(0, 10), pady=(0, 10))

    def GUI_eventex(self, *agrs, **kwds):
        self.Treeview_classification.bind('<<TreeviewSelect>>', self.bin_classification_TreeviewSelect)
        self.Treeview_objects.bind('<<TreeviewSelect>>', self.bin_objects_TreeviewSelect)
        self.Treeview_choices.bind('<<TreeviewSelect>>', self.bin_choices_TreeviewSelect)
        # self.root_Treeview_choice.bind('<Double-Button-3>', self.bin_open_path_available)



    def GUI_install(self, master, *args, **kwds):
        self.master = master
        self.GUI_initial()
        self.GUI_eventex()
        # self.sbin_install()


    def __init__(self, master):
        self.GUI_install(master)


    def sbin_clear_Treeview_classification(self):
        [self.Treeview_classification.delete(row) for row in self.Treeview_classification.get_children()]


    def sbin_clear_Treeview_objects(self):
        [self.Treeview_objects.delete(row) for row in self.Treeview_objects.get_children()]


    def sbin_clear_Treeview_choices(self):
        [self.Treeview_choices.delete(row) for row in self.Treeview_choices.get_children()]


    def sbin_update_preview(self, SHA: str | None) -> None:
        if SHA is None:
            self.Label_preview.config(image='')
            self.Label_preview.config(text='无预览图')
            self.Label_SHA.config(text='SHA')
            self.Label_explain.config(text='无附加描述')
            return

        width = self.Label_preview.winfo_width()
        height = self.Label_preview.winfo_height()
        self.__image = core.module.image.get_preview_image(SHA, width, height)

        if self.__image is None:
            self.Label_preview.config(image='')
            self.Label_preview.config(text='无预览图')

        else:
            self.Label_preview.config(image=self.__image)

        self.Label_SHA.config(text=SHA)
        item = core.Module.ModsIndex.get_item(SHA)
        if isinstance(item, dict): text = item.get('explain', '')
        else: text = '无附加描述'
        self.Label_explain.config(text=text if text else '无附加描述')


    def reload_classification(self):
        self.sbin_clear_Treeview_classification()

        class_list = core.Module.ModsManage.get_class_list()
        for class_ in class_list:
            lst = core.Module.ModsManage.get_object_list(class_)
            amount = len(lst)
            self.Treeview_classification.insert('', 'end', text=f'{class_}\n[{amount}]', tags=(class_), image=core.content.ThumbnailGroup.get(class_))


    def bin_classification_TreeviewSelect(self, *agrs):
        self.sbin_clear_Treeview_objects()

        class_ = self.sbin_get_select_classification()
        if class_ is None: return

        object_list = core.Module.ModsManage.get_object_list(class_)

        for name in object_list:
            c = len(core.Module.ModsManage.get_object_SHA_list(name))
            a = len(core.Module.ModsIndex.get_object_SHA_list(name))

            SHA = core.Module.ModsManage.get_load_object_SHA(name)
            if SHA is None: value = ()

            else:
                data = core.Module.ModsIndex.get_item(SHA)
                n = data['name']
                g = data['grading']
                atags = '[' + ' '.join(data.get('tags', [])) + ']'
                value = (f'{n}\n[{g}] {atags}', )

            self.Treeview_objects.insert('', 'end', text=f'{name}\n[{c}/{a}]', values=value, tags=(name), image=core.content.ThumbnailGroup.get(name))


    def bin_objects_TreeviewSelect(self, *args):
        self.sbin_clear_Treeview_choices()

        self.Treeview_choices.insert('', 'end', text=f'- [X] 卸载该对象 -', tags=('--X--'))

        object_ = self.sbin_get_select_objects()

        if object_ is None: return

        lst = core.Module.ModsManage.get_object_SHA_list(object_)

        for SHA in lst:
            item = core.Module.ModsIndex.get_item(SHA)
            name = item['name']
            grading = item['grading']
            atags = '[' + ' '.join(item.get('tags', [])) + ']'

            self.Treeview_choices.insert('', 'end', text=f'{name}\n[{grading}] {atags}', tags=(SHA))

        SHA = core.Module.ModsManage.get_load_object_SHA(object_)
        if SHA is None: self.sbin_update_preview(None)
        else: self.sbin_update_preview(SHA)


    def bin_choices_TreeviewSelect(self, *args):
        SHA = self.sbin_get_select_choices()

        if SHA is None: return

        name = self.Treeview_choices.item(self.Treeview_choices.focus())['text']

        if SHA == '--X--':
            self.Treeview_objects.item(self.Treeview_objects.focus(), value=())
            tags = self.Treeview_objects.item(self.Treeview_objects.focus())['tags']
            if not tags: return None
            object_ = tags[0]
            core.Module.ModsManage.unload(object_)
            self.sbin_update_preview(None)

        else:
            self.Treeview_objects.item(self.Treeview_objects.focus(), value=(name, ))
            core.Module.ModsManage.load(SHA)
            self.sbin_update_preview(SHA)


    def bin_refresh(self, *args):
        self.sbin_clear_Treeview_classification()
        self.sbin_clear_Treeview_objects()
        self.sbin_clear_Treeview_choices()
        self.sbin_update_preview(None)
        self.reload_classification()


    def sbin_get_select_classification(self):
        tags = self.Treeview_classification.item(self.Treeview_classification.focus())['tags']
        if not tags: return None
        class_ = tags[0]

        return class_


    def sbin_get_select_objects(self):
        tags = self.Treeview_objects.item(self.Treeview_objects.focus())['tags']
        if not tags: return None
        object_ = tags[0]

        return object_


    def sbin_get_select_choices(self):
        tags = self.Treeview_choices.item(self.Treeview_choices.focus())['tags']
        if not tags: return None
        SHA = tags[0]

        return SHA
