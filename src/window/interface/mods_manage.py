# -*- coding: utf-8 -*-

import os
import tkinter.filedialog
import tkinter.font

import win32api
import pyperclip
import ttkbootstrap

import core
from constant import *

CMD_UNLOAD = "--X--"


class ModsManage(object):
    def install(self, *args, **kwds):
        titles = (("#0", "对象", 200), ("enabled", "启用 Mod", 240))

        self.FC_WIDTH = 200

        self.value_entry_search = ttkbootstrap.StringVar()
        self.frame_choice = ttkbootstrap.Frame(self.master)

        self.treeview_classification = ttkbootstrap.Treeview(self.master, show="tree headings", selectmode="extended")
        self.treeview_objects = ttkbootstrap.Treeview(self.master, show="tree headings", selectmode="extended", columns=("enabled",))
        self.treeview_choices = ttkbootstrap.Treeview(self.frame_choice, selectmode="extended", show="tree headings")

        self.scrollbar_classification = ttkbootstrap.Scrollbar(self.master, command=self.treeview_classification.yview)
        self.scrollbar_objects = ttkbootstrap.Scrollbar(self.master, command=self.treeview_objects.yview)
        self.scrollbar_choices = ttkbootstrap.Scrollbar(self.frame_choice, command=self.treeview_choices.yview)

        self.entry_search = ttkbootstrap.Entry(self.frame_choice, textvariable=self.value_entry_search)

        # self.label_explain = ttkbootstrap.Label(self.master, anchor="center", text="无附加描述")
        self.label_SHA = ttkbootstrap.Label(self.master, anchor="center", text="SHA", cursor="hand2")
        self.label_preview = ttkbootstrap.Label(self.master, anchor="center", text="无预览图", cursor="plus")

        self.treeview_classification.config(yscrollcommand=self.scrollbar_classification.set)
        self.treeview_objects.config(yscrollcommand=self.scrollbar_objects.set)
        self.treeview_choices.config(yscrollcommand=self.scrollbar_choices.set)

        self.treeview_classification.column("#0", width=200, anchor="w")
        self.treeview_choices.column("#0", width=300, anchor="w")
        self.treeview_classification.heading("#0", text="分类")
        self.treeview_choices.heading("#0", text="选择")

        for tree, text, width in titles:
            self.treeview_objects.column(tree, width=width, anchor="w")
            self.treeview_objects.heading(tree, text=text)


        self.treeview_classification.pack(side="left", fill="y", padx=(10, 0), pady=10)
        self.scrollbar_classification.pack(side="left", fill="y", padx=(2, 5), pady=10)
        self.treeview_objects.pack(side="left", fill="y", padx=(0, 0), pady=10)
        self.scrollbar_objects.pack(side="left", fill="y", padx=(2, 5), pady=10)
        self.frame_choice.pack(side="left", fill="y")
        self.entry_search.pack(side="bottom", fill="x", padx=(0, 10), pady=(5, 10))
        self.treeview_choices.pack(side="left", fill="y", padx=(0, 0), pady=(10, 0))
        self.scrollbar_choices.pack(side="left", fill="y", padx=(2, 10), pady=(10, 0))
        self.label_SHA.pack(side="bottom", fill="x", padx=(0, 10), pady=(10, 5))
        self.label_preview.pack(side="top", fill="both", padx=(0, 10), pady=(10, 0), expand=1)
        # self.label_explain.pack(side="bottom", fill="x", padx=(0, 10), pady=(5, 10))
        # self.Button_refresh.pack(side="top", fill="x", padx=(0, 10), pady=(0, 10))


        self.treeview_classification.bind("<<TreeviewSelect>>", lambda *_: core.construct.event.set_event(E.WINDOW_MODS_MANAGE_TS_CLASS))
        self.treeview_objects.bind("<<TreeviewSelect>>", lambda *_: core.construct.event.set_event(E.WINDOW_MODS_MANAGE_TS_OBJECT))
        self.treeview_choices.bind("<<TreeviewSelect>>", lambda *_: core.construct.event.set_event(E.WINDOW_MODS_MANAGE_TS_CHOICE))

        self.treeview_choices.bind("<Double-1>", self.bin_load_mod)
        self.treeview_choices.bind("<Button-3>", self.bin_show_choices_menu)
        self.treeview_objects.bind("<Button-3>", self.bin_show_objects_menu)
        # self.entry_search.bind("<Return>", self.update_choices_list)
        self.value_entry_search.trace("w", self.update_choices_list)

        # self.treeview_choices.bind("<Motion>", self.bin_treeview_choices_motion)
        self.treeview_choices.bind("<Motion>", self.bin_treeview_choices_motion)
        self.treeview_choices.bind("<Leave>", lambda *_: core.window.annotation_toplevel.withdraw())

        # self.label_preview.bind("<Motion>", lambda *_: core.window.annotation_toplevel.update_position())
        # self.label_preview.bind("<Enter>", lambda *_: self.bin_update_explain())
        # self.label_preview.bind("<Leave>", lambda *_: core.window.annotation_toplevel.withdraw())

        # self.label_explain.bind("<Double-Button-3>",  lambda *_: self.refresh_classification())
        # self.label_explain.bind("<Button-1>",  lambda *_: core.module.mods_manage.refresh())

        self.label_SHA.bind("<Button-1>", lambda *_: pyperclip.copy(self.label_SHA["text"]))

        self.value_choice_item = ""
        self.value_object_item = ""


    def initial(self):
        _alt_set = core.window.annotation_toplevel.register

        _alt_set(self.treeview_classification, T.ANNOTATION_MANAGE_CLASSIFICATION)
        _alt_set(self.treeview_objects, T.ANNOTATION_MANAGE_OBJECTS)
        # _alt_set(interface.mods_manage.treeview_choices, T.ANNOTATION_MANAGE_CHOICES)
        _alt_set(self.entry_search, T.ANNOTATION_MANAGE_SEARCH, 1)
        _alt_set(self.label_SHA, T.ANNOTATION_COPY_SHA, 2)


    def __init__(self, master):
        self.master = master
        self.install(master)


    def sbin_clear_treeview_classification(self):
        self.treeview_classification.delete(*self.treeview_classification.get_children())


    def sbin_clear_treeview_objects(self):
        self.treeview_objects.delete(*self.treeview_objects.get_children())


    def sbin_clear_treeview_choices(self):
        self.treeview_choices.delete(*self.treeview_choices.get_children())


    def sbin_update_preview(self, SHA: str | None = ...) -> None:
        core.log.debug(f"更新预览图 {SHA}", L.WINDOS_MODS_MANAGE)

        if SHA is Ellipsis:
            SHA = self.sbin_get_select_choices()
            SHA = Ellipsis if SHA is None else SHA

        if SHA is Ellipsis:
            object_ = self.sbin_get_select_objects()
            SHA = core.module.mods_manage.get_load_object_sha(object_)

        if SHA is None:
            self.label_preview.config(image="")
            self.label_preview.config(text="无预览图")
            self.label_SHA.config(text="SHA")
            # self.label_explain.config(text="无附加描述")
            return

        width = self.label_preview.winfo_width()
        height = self.label_preview.winfo_height()
        self.__image = core.module.image.get_preview_image(SHA, width, height)

        if self.__image is None:
            self.label_preview.config(image="")
            self.label_preview.config(text="无预览图")

        else:
            self.label_preview.config(image=self.__image)

        self.label_SHA.config(text=SHA)
        # item = core.module.mods_index.get_item(SHA)
        # if isinstance(item, dict): text = item.get("explain", "")
        # else: text = "无附加描述"
        # self.label_explain.config(text=text if text else "无附加描述")


    def bin_treeview_choices_motion(self, event):
        core.window.annotation_toplevel.update_position()
        iid = self.treeview_choices.identify("item", event.x, event.y)
        if iid == "":
            core.window.annotation_toplevel.withdraw()
            core.window.annotation_toplevel.deiconify_content(T.ANNOTATION_MANAGE_CHOICES, 3)
            return

        if iid == CMD_UNLOAD:
            core.window.annotation_toplevel.deiconify_content("卸载", 1)
            return

        item = core.module.mods_index.get_item(iid)
        if isinstance(item, dict):
            text = ""

            name = item.get(K.INDEX.NAME)
            author = item.get(K.INDEX.AUTHOR, "<未知>")
            author = "<未知>" if author == "" else author
            atags = " ".join(item.get(K.INDEX.TAGS, []))
            explath = item.get(K.INDEX.EXPLAIN, "<无附加描述>")
            explath = "<无附加描述>" if explath == "" else explath

            text += f"名称：{name}\n"
            text += f"作者：{author}\n\n{explath}"
            if atags: text += f"\n\n{atags}"

            core.window.annotation_toplevel.deiconify_content(text, 1)


    def bin_update_explain(self):
        SHA = self.label_SHA["text"]
        item = core.module.mods_index.get_item(SHA)
        if isinstance(item, dict):
            text = ""

            name = item.get(K.INDEX.NAME)
            author = item.get(K.INDEX.AUTHOR, "<未知>")
            author = "<未知>" if author == "" else author
            atags = " ".join(item.get(K.INDEX.TAGS, []))
            explath = item.get(K.INDEX.EXPLAIN, "<无附加描述>")
            explath = "<无附加描述>" if explath == "" else explath

            text += f"名称：{name}\n"
            text += f"作者：{author}\n\n{explath}"
            if atags: text += f"\n\n{atags}"

            core.window.annotation_toplevel.deiconify_content(text, 1)

        else:
            # text = "无附加描述"
            ...
        # self.label_explain.config(text=text if text else "无附加描述")


    def update_classification_list(self):
        core.log.debug("更新分类列表", L.WINDOS_MODS_MANAGE)

        class_list = core.module.mods_manage.get_class_list()
        exist_class_list = self.treeview_classification.get_children()

        # 剔除已经不存在的分类
        nonexistent = set(exist_class_list) - set(class_list)
        self.treeview_classification.delete(*nonexistent)

        for index, class_ in enumerate(class_list):
            lst = core.module.mods_manage.get_object_list(class_)
            amount = len(lst)

            if class_ in exist_class_list:
                self.treeview_classification.item(
                    class_,
                    text=f"{class_}\n[{amount}]",
                    image=core.window.treeview_thumbnail.get(class_)
                )

            else:
                self.treeview_classification.insert(
                    "", index, class_,
                    text=f"{class_}\n[{amount}]",
                    tags=(class_),
                    image=core.window.treeview_thumbnail.get(class_)
                )


    def update_objects_list(self, *agrs):
        core.log.debug("更新对象列表", L.WINDOS_MODS_MANAGE)

        class_ = self.sbin_get_select_classification()
        if class_ is None: return

        object_list = core.module.mods_manage.get_object_list(class_)
        exist_object_list = self.treeview_objects.get_children()

        # 剔除已经不存在的对象
        nonexistent = set(exist_object_list) - set(object_list)
        self.treeview_objects.delete(*nonexistent)

        for index, object_name in enumerate(object_list):
            local_ = len(core.module.mods_manage.get_object_sha_list(object_name))
            all_ = len(core.module.mods_index.get_object_sha_list(object_name))

            SHA = core.module.mods_manage.get_load_object_sha(object_name)

            if SHA is None:
                value = ()

            else:
                data = core.module.mods_index.get_item(SHA)
                n = data["name"]
                g = data["grading"]
                a = data.get(K.INDEX.AUTHOR, "-")
                a = "-" if not a else a
                atags = " ".join(data.get("tags", []))
                value = (f"[{g}] {n}\n{a} {atags}",)

            if object_name in exist_object_list:
                self.treeview_objects.item(
                    object_name,
                    text=f"{object_name}\n[{local_}/{all_}]",
                    values=value,
                    tags=object_name,
                    image=core.window.treeview_thumbnail.get(object_name)
                )

            else:
                self.treeview_objects.insert(
                    "", index, object_name,
                    text=f"{object_name}\n[{local_}/{all_}]",
                    values=value,
                    tags=object_name,
                    image=core.window.treeview_thumbnail.get(object_name)
                )


    def update_choices_list(self, *args):
        core.log.debug("更新选择列表", L.WINDOS_MODS_MANAGE)

        object_ = self.sbin_get_select_objects()
        if object_ is None:
            self.sbin_clear_treeview_choices()
            return

        all_mods_list = core.module.mods_manage.get_object_sha_list(object_)
        exist_mods_list = self.treeview_choices.get_children()
        search = self.value_entry_search.get()

        to_list = []
        to_data = {}

        for SHA in all_mods_list:
            item = core.module.mods_index.get_item(SHA)
            if not core.module.extension.item_dict_conform(SHA, item, search): continue
            to_list.append(SHA)
            to_data[SHA] = item

        # 剔除已经不存在的 Mod
        nonexistent = set(exist_mods_list) - set(to_data)
        self.treeview_choices.delete(*nonexistent)

        for index, SHA in enumerate(to_data):
            item = core.module.mods_index.get_item(SHA)
            name = item["name"]
            grading = item["grading"]
            a = item.get(K.INDEX.AUTHOR, "-")
            a = "-" if not a else a
            atags = " ".join(item.get("tags", []))

            if SHA in exist_mods_list:
                self.treeview_choices.item(
                    SHA,
                    text=f"[{grading}] {name}\n{a} {atags}", 
                    tags=(SHA, )
                )

            else:
                self.treeview_choices.insert(
                    "", index, SHA,
                    text=f"[{grading}] {name}\n{a} {atags}", 
                    tags=(SHA, )
                )

        self.treeview_choices.insert(
            "", 0, CMD_UNLOAD,
            text=f"- [X] 卸载该对象 -",
            tags=(CMD_UNLOAD)
        )

        # SHA = core.module.mods_manage.get_load_object_sha(object_)
        # if SHA is None: self.sbin_update_preview(None)
        # else: self.sbin_update_preview(SHA)


    def bin_load_mod(self, *args):
        SHA = self.sbin_get_select_choices()

        if SHA is None: return

        name = self.treeview_choices.item(self.treeview_choices.focus())["text"]

        if SHA == CMD_UNLOAD:
            self.treeview_objects.item(self.treeview_objects.focus(), value=())
            tags = self.treeview_objects.item(self.treeview_objects.focus())["tags"]
            if not tags: return None
            object_ = tags[0]
            core.module.mods_manage.unload(object_)

        else:
            self.treeview_objects.item(self.treeview_objects.focus(), value=(name, ))
            core.module.mods_manage.load(SHA)


    def bin_refresh(self, *args):
        self.sbin_clear_treeview_classification()
        self.sbin_clear_treeview_objects()
        self.sbin_clear_treeview_choices()
        self.sbin_update_preview(None)
        self.update_classification_list()


    def sbin_get_select_classification(self):
        answer = self.treeview_classification.focus()
        return answer if answer else None


    def sbin_get_select_objects(self):
        answer = self.treeview_objects.focus()
        return answer if answer else None


    def sbin_get_select_choices(self):
        answer = self.treeview_choices.focus()
        return answer if answer else None


    def on_mouse_move(self, event):
        core.window.annotation_toplevel.update_position()



    # ================================================================================================================================
    # 对象列表右键菜单
    # ================================================================================================================================



    def bin_show_objects_menu(self, event):
        self.value_object_item = self.treeview_objects.identify("item", event.x, event.y)

        try:
            default_font = tkinter.font.nametofont("TkDefaultFont")
            menu = ttkbootstrap.Menu(self.treeview_choices, tearoff=False, font=(default_font.actual("family"), default_font.actual("size")))

        except Exception as e:
            menu = ttkbootstrap.Menu(self.treeview_choices, tearoff=False)

        if self.value_object_item != "":
            menu.add_command(label="复制对象名称", command=lambda: pyperclip.copy(self.value_object_item))

            menu.post(event.x_root+10 , event.y_root+10)



    # ================================================================================================================================
    # 选择列表右键菜单
    # ================================================================================================================================



    def bin_show_choices_menu(self, event):
        self.value_choice_item = self.treeview_choices.identify("item", event.x, event.y)

        try:
            default_font = tkinter.font.nametofont("TkDefaultFont")
            menu = ttkbootstrap.Menu(self.treeview_choices, tearoff=False, font=(default_font.actual("family"), default_font.actual("size")))

        except Exception as e:
            menu = ttkbootstrap.Menu(self.treeview_choices, tearoff=False)

        sha = self.value_choice_item

        if sha != "":
            menu.add_command(label="编辑 Mod 信息", command=self.bin_choices_menu_modify_item_data)
            menu.add_command(label="导出 Mod 文件", command=self.bin_choices_menu_export_file)
            menu.add_command(label="复制 SHA 值", command=self.bin_choices_menu_copy_sha)
            menu.add_command(label="查看原始文件", command=self.bin_choices_menu_view_original_file)

            if core.module.mods_manage.is_load_sha(sha):
                menu.add_command(label="查看工作文件", command=self.bin_choices_menu_view_work_file)

            if core.module.mods_manage.is_have_cache_load(sha):
                menu.add_command(label="查看缓存文件", command=self.bin_choices_menu_view_cache_file)

            menu.add_command(label="查看预览图文件", command=self.bin_choices_menu_add_view_preview)

            menu.add_separator()

        menu.add_command(label="添加文件夹的形式的 Mod", command=self.bin_choices_menu_add_mod_from_dir)
        menu.add_command(label="添加压缩包的形式的 Mod", command=self.bin_choices_menu_add_mod_from_file)

        menu.post(event.x_root+10 , event.y_root+10)


    def bin_choices_menu_modify_item_data(self, *_):
        core.additional.modify_item_data.ModifyItemData(self.value_choice_item)


    def bin_choices_menu_view_original_file(self, *_):
        path = os.path.abspath(os.path.join(core.env.directory.resources.mods, self.value_choice_item))
        # win32api.ShellExecute(None, "open", "explorer", f"/select,{path}", path, 1)
        core.external.view_file(path)


    def bin_choices_menu_view_work_file(self, *_):
        path = os.path.abspath(os.path.join(core.userenv.directory.work_mods, self.value_choice_item))
        # win32api.ShellExecute(None, "open", "explorer", f"{path}", path, 1)
        core.external.view_directory(path)


    def bin_choices_menu_view_cache_file(self, *_):
        path = os.path.abspath(os.path.join(core.userenv.directory.work_mods, f"{K.DISABLED}-{self.value_choice_item}"))
        # win32api.ShellExecute(None, "open", "explorer", f"{path}", path, 1)
        core.external.view_directory(path)


    def bin_choices_menu_add_mod_from_file(self, *_):
        path = tkinter.filedialog.askopenfilename(title="选择 Mod 压缩包", filetypes=[("压缩文件", ["*.zip", "*.rar", "*.7z"])])
        if path: core.additional.add_mod.AddMods(path)


    def bin_choices_menu_add_mod_from_dir(self, *_):
        path = tkinter.filedialog.askdirectory(title="选择 Mod 文件夹")
        if path:
            core.construct.taskpool.addtask(core.additional.add_mod.add_mod_is_dir, (path,), answer=False)


    def bin_choices_menu_export_file(self, *_):
        SHA = self.value_choice_item
        data = core.module.mods_index.get_item(SHA)
        suffix = data[K.INDEX.TYPE]
        suffix = suffix if suffix.startswith(".") else f".{suffix}"
        name = data[K.INDEX.NAME]

        path = tkinter.filedialog.asksaveasfilename(
            title="导出 Mod 文件",
            initialfile=name,
            defaultextension=suffix,
            filetypes=[("压缩文件", suffix)]
            )
        path = path if path.endswith(suffix) else f"{path}{suffix}"

        with open(os.path.join(core.env.directory.resources.mods, SHA), "rb") as rfobj:
            content = rfobj.read()

        with open(path, "wb") as wfobj:
            wfobj.write(content)


    def bin_choices_menu_copy_sha(self, *_):
        pyperclip.copy(self.value_choice_item)


    def bin_choices_menu_add_view_preview(self, *_):
        SHA = self.value_choice_item
        for suffix in ['.png', '.jpg']:
            target = os.path.join(core.env.directory.resources.preview, f'{SHA}{suffix}')
            if os.path.isfile(target):
                core.external.view_file(target)
                return

        else:
            core.window.messagebox.showerror(title="目标不存在", message="该 Item 没有预览图文件")
