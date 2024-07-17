# Licensed under the GPL 3.0 License.
# d3dxSkinManage by numlinka.

# std
import os
import shutil
import tkinter.filedialog
import tkinter.font

# site
# import win32api
import pyperclip
import ttkbootstrap

# local
import core
import window
import widgets
from constant import *


CMD_UNLOAD = "--X--"


class ModsManage(object):
    def install(self, *args, **kwds):
        titles = (("#0", "对象", 200), ("enabled", "启用 Mod", 240))

        self.FC_WIDTH = 200

        self.value_classification_search = ttkbootstrap.StringVar()
        self.value_objects_search = ttkbootstrap.StringVar()
        self.value_choices_search = ttkbootstrap.StringVar()

        self.frame_classification = ttkbootstrap.Frame(self.master)
        self.frame_objects = ttkbootstrap.Frame(self.master)
        self.frame_choices = ttkbootstrap.Frame(self.master)
        self.frame_preview = ttkbootstrap.Frame(self.master)

        self.treeview_classification = ttkbootstrap.Treeview(self.frame_classification, show="tree headings", selectmode="extended")
        self.treeview_objects = ttkbootstrap.Treeview(self.frame_objects, show="tree headings", selectmode="extended", columns=("enabled",))
        self.treeview_choices = ttkbootstrap.Treeview(self.frame_choices, selectmode="extended", show="tree headings")

        self.scrollbar_classification = ttkbootstrap.Scrollbar(self.frame_classification, command=self.treeview_classification.yview)
        self.scrollbar_objects = ttkbootstrap.Scrollbar(self.frame_objects, command=self.treeview_objects.yview)
        self.scrollbar_choices = ttkbootstrap.Scrollbar(self.frame_choices, command=self.treeview_choices.yview)

        self.entry_classification_search = ttkbootstrap.Entry(self.frame_classification, textvariable=self.value_classification_search)
        self.entry_objects_search = ttkbootstrap.Entry(self.frame_objects, textvariable=self.value_objects_search)
        self.entry_choices_search = ttkbootstrap.Entry(self.frame_choices, textvariable=self.value_choices_search)

        # self.label_explain = ttkbootstrap.Label(self.master, anchor="center", text="无附加描述")
        self.label_SHA = ttkbootstrap.Label(self.frame_preview, anchor="center", text="SHA", cursor="hand2")
        self.label_preview = ttkbootstrap.Label(self.frame_preview, anchor="center", text="无预览图", cursor="plus")

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


        self.frame_classification.pack(side="left", fill="both", padx=(10, 0), pady=10)
        self.frame_objects.pack(side="left", fill="both", padx=(5, 0), pady=10)
        self.frame_choices.pack(side="left", fill="both", padx=(5, 0), pady=10)
        self.frame_preview.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.entry_classification_search.pack(side="bottom", fill="x", padx=0, pady=(2, 0))
        self.treeview_classification.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.scrollbar_classification.pack(side="left", fill="y", padx=(2, 0), pady=0)

        self.entry_objects_search.pack(side="bottom", fill="x", padx=0, pady=(2, 0))
        self.treeview_objects.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.scrollbar_objects.pack(side="left", fill="y", padx=(2, 0), pady=0)

        self.entry_choices_search.pack(side="bottom", fill="x", padx=0, pady=(2, 0))
        self.treeview_choices.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.scrollbar_choices.pack(side="left", fill="y", padx=(2, 0), pady=0)

        self.label_SHA.pack(side="bottom", fill="x", padx=0, pady=0)
        self.label_preview.pack(side="top", fill="both", padx=0, pady=(0, 10), expand=1)
        # self.label_explain.pack(side="bottom", fill="x", padx=(0, 10), pady=(5, 10))
        # self.Button_refresh.pack(side="top", fill="x", padx=(0, 10), pady=(0, 10))


        self.treeview_classification.bind("<<TreeviewSelect>>", lambda *_: core.construct.event.set_event(E.WINDOW_MODS_MANAGE_TS_CLASS))
        self.treeview_objects.bind("<<TreeviewSelect>>", lambda *_: core.construct.event.set_event(E.WINDOW_MODS_MANAGE_TS_OBJECT))
        self.treeview_choices.bind("<<TreeviewSelect>>", lambda *_: core.construct.event.set_event(E.WINDOW_MODS_MANAGE_TS_CHOICE))

        self.treeview_choices.bind("<Double-1>", self.bin_load_mod)
        # self.treeview_choices.bind("<Button-3>", self.bin_show_choices_menu)
        # self.treeview_objects.bind("<Button-3>", self.bin_show_objects_menu)
        # self.entry_search.bind("<Return>", self.update_choices_list)
        self.value_classification_search.trace("w", self.update_classification_list)
        self.value_objects_search.trace("w", self.update_objects_list)
        self.value_choices_search.trace("w", self.update_choices_list)

        # self.treeview_choices.bind("<Motion>", self.bin_treeview_choices_motion)
        self.treeview_choices.bind("<Motion>", self.bin_treeview_choices_motion)
        self.treeview_choices.bind("<Leave>", lambda *_: core.window.annotation_toplevel.withdraw())

        # self.label_preview.bind("<Motion>", lambda *_: core.window.annotation_toplevel.update_position())
        # self.label_preview.bind("<Enter>", lambda *_: self.bin_update_explain())
        # self.label_preview.bind("<Leave>", lambda *_: core.window.annotation_toplevel.withdraw())

        # self.label_explain.bind("<Double-Button-3>",  lambda *_: self.refresh_classification())
        # self.label_explain.bind("<Button-1>",  lambda *_: core.module.mods_manage.refresh())

        self.label_SHA.bind("<Button-1>", lambda *_: pyperclip.copy(self.label_SHA["text"]))

        self.value_classification_item = ""
        self.value_choice_item = ""
        self.value_object_item = ""

        self.treeview_classification_menu = widgets.DynamicMenu(self.treeview_classification, offsets=(10, 10), value_source=self.bin_get_classification_identify)
        self.treeview_objects_menu = widgets.DynamicMenu(self.treeview_objects, offsets=(10, 10), value_source=self.bin_get_objects_identify)
        self.treeview_choices_menu = widgets.DynamicMenu(self.treeview_choices, offsets=(10, 10), value_source=self.bin_get_choices_identify)

        # window.methods.motion.motion_treeview_width(window.mainwindow, self.treeview_objects, self.treeview_objects)
        # window.methods.motion.motion_frame_width(window.mainwindow, self.frame_classification, self.treeview_classification)
        # window.methods.motion.motion_frame_width(window.mainwindow, self.frame_objects, self.treeview_objects)
        # window.methods.motion.motion_frame_width(window.mainwindow, self.frame_choices, self.treeview_choices)


    def initial(self):
        _alt_set = core.window.annotation_toplevel.register

        _alt_set(self.treeview_classification, T.ANNOTATION_MANAGE_CLASSIFICATION)
        _alt_set(self.treeview_objects, T.ANNOTATION_MANAGE_OBJECTS)
        # _alt_set(interface.mods_manage.treeview_choices, T.ANNOTATION_MANAGE_CHOICES)
        _alt_set(self.entry_classification_search, T.ANNOTATION_MANAGE_CLASSIFICATION_SEARCH, 1)
        _alt_set(self.entry_objects_search, T.ANNOTATION_MANAGE_OBJECTS_SEARCH, 1)
        _alt_set(self.entry_choices_search, T.ANNOTATION_MANAGE_CHOICES_SEARCH, 1)
        _alt_set(self.label_preview, T.ANNOTATION_MANAGE_PREVIEW, 2)
        _alt_set(self.label_SHA, T.ANNOTATION_COPY_SHA, 2)
        self.treeview_classification_menu_initial()
        self.treeview_objects_menu_initial()
        self.treeview_choices_menu_initial()


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


    def update_classification_list(self, *_):
        core.log.debug("更新分类列表", L.WINDOS_MODS_MANAGE)

        all_class_list = core.module.mods_manage.get_class_list()
        exist_class_list = self.treeview_classification.get_children()
        search = self.value_classification_search.get()

        to_list = []

        for classname in all_class_list:
            if not core.module.extension.item_text_conform(classname, search): continue
            to_list.append(classname)

        # 剔除已经不存在的分类
        nonexistent = set(exist_class_list) - set(to_list)
        self.treeview_classification.delete(*nonexistent)

        for index, class_ in enumerate(to_list):
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

        self.master.update()
        core.construct.event.set_event(E.WINDOW_MODS_MANAGE_TV_CLASS_UPDATE)


    def update_objects_list(self, *_):
        core.log.debug("更新对象列表", L.WINDOS_MODS_MANAGE)

        class_ = self.sbin_get_select_classification()
        if class_ is None: return

        all_object_list = core.module.mods_manage.get_object_list(class_)
        exist_object_list = self.treeview_objects.get_children()
        search = self.value_objects_search.get()

        to_list = []

        for objectname in all_object_list:
            if not core.module.extension.item_text_conform(objectname, search): continue
            to_list.append(objectname)

        # 剔除已经不存在的对象
        nonexistent = set(exist_object_list) - set(to_list)
        self.treeview_objects.delete(*nonexistent)

        for index, object_name in enumerate(to_list):
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

        self.master.update()
        core.construct.event.set_event(E.WINDOW_MODS_MANAGE_TV_OBJECT_UPDATE)


    def update_choices_list(self, *_):
        core.log.debug("更新选择列表", L.WINDOS_MODS_MANAGE)

        object_ = self.sbin_get_select_objects()
        if object_ is None:
            self.sbin_clear_treeview_choices()
            return

        all_mods_list = core.module.mods_manage.get_object_sha_list(object_)
        exist_mods_list = self.treeview_choices.get_children()
        search = self.value_choices_search.get()

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
        self.master.update()
        core.construct.event.set_event(E.WINDOW_MODS_MANAGE_TV_CHOICE_UPDATE)


    def bin_load_mod(self, *args):
        SHA = self.sbin_get_select_choices()

        if SHA is None: return

        # name = self.treeview_choices.item(self.treeview_choices.focus())["text"]
        name = self.sbin_get_select_choices()

        if SHA == CMD_UNLOAD:
            # tags = self.treeview_objects.item(self.treeview_objects.focus())["tags"]
            # if not tags: return None
            # object_ = tags[0]
            object_ = self.sbin_get_select_objects()
            if not object_: return None
            # core.sync.addtask(f"卸载 {object_}", core.module.mods_manage.unload, (object_, ))
            core.module.mods_manage.unload(object_)

            self.treeview_objects.item(self.treeview_objects.focus(), value=())

        else:
            # core.sync.addtask(f"加载 {name}", core.module.mods_manage.load, (SHA, ))
            core.module.mods_manage.load(SHA)

            self.treeview_objects.item(self.treeview_objects.focus(), value=(name, ))



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
    # 分类列表右键菜单
    # ================================================================================================================================



    def bin_get_classification_identify(self, event):
        result = self.treeview_classification.identify("item", event.x, event.y)
        self.value_classification_item = result
        return result


    def treeview_classification_menu_initial(self):
        _alt = self.treeview_classification_menu.add_label
        _alt("修改分类参照", command=core.additional.modify_classification.modify_classification, order=1000, condition=self._is_valid_classification, need_value=True)
        _alt("添加新的分类", command=self.bin_classification_menu_new_classification, order=1010)


    def _is_valid_classification(self, classification_name):
        return False if classification_name in ["", None, "未分类"] else True


    def bin_classification_menu_new_classification(self, *_):
        core.additional.modify_classification.NewClassification(True)



    # ================================================================================================================================
    # 对象列表右键菜单
    # ================================================================================================================================



    def bin_get_objects_identify(self, event):
        result = self.treeview_objects.identify("item", event.x, event.y)
        self.value_object_item = result
        return result


    def treeview_objects_menu_initial(self):
        _alt = self.treeview_objects_menu.add_label
        _alt("复制对象名称", command=self.bin_objects_menu_copy_object_name, order=1000, condition=self._is_valid_object, need_value=True)


    def _is_valid_object(self, object_name):
        return True if object_name else False


    def bin_objects_menu_copy_object_name(self, *_):
        pyperclip.copy(self.value_object_item)


    # ! 无效函数, 现在它已被弃用
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



    def bin_get_choices_identify(self, event):
        result = self.treeview_choices.identify("item", event.x, event.y)
        self.value_choice_item = result
        return result


    def treeview_choices_menu_initial(self):
        _alt = self.treeview_choices_menu.add_label
        # _alt("编辑 Mod 信息 (旧版)",  self.bin_choices_menu_modify_item_data,   order=1000, condition=self._is_valid_sha, need_value=True)
        _alt("导出 Mod 文件",  self.bin_choices_menu_export_file,        order=1010, condition=self._is_valid_sha, need_value=True)
        _alt("复制 SHA 值",    self.bin_choices_menu_copy_sha,           order=1020, condition=self._is_valid_sha, need_value=True)
        _alt("查看原始文件",   self.bin_choices_menu_view_original_file, order=1030, condition=self._is_valid_sha, need_value=True)
        _alt("查看工作文件",   self.bin_choices_menu_view_work_file,     order=1040, condition=core.module.mods_manage.is_load_sha,        need_value=True)
        _alt("查看缓存文件",   self.bin_choices_menu_view_cache_file,    order=1040, condition=core.module.mods_manage.is_have_cache_load, need_value=True)
        # _alt("删除缓存文件",   self.bin_choices_menu_remove_cache_file,  order=1045, condition=core.module.mods_manage.is_have_cache_load, need_value=True)
        _alt("查看预览图文件", self.bin_choices_menu_add_view_preview,   order=1050, condition=self._is_valid_sha, need_value=True)

        _alt("添加文件夹的形式的 Mod", self.bin_choices_menu_add_mod_from_dir,  200, order=1000)
        _alt("添加压缩包的形式的 Mod", self.bin_choices_menu_add_mod_from_file, 200, order=1010)


    def _is_valid_sha(self, sha):
        return False if sha in ("", CMD_UNLOAD) else True


    # ! 无效函数, 现在它已被弃用
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
        core.additional.modify_item_data.modify_item_data(self.value_choice_item)


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


    def bin_choices_menu_remove_cache_file(self, *_):
        path = os.path.abspath(os.path.join(core.userenv.directory.work_mods, f"{K.DISABLED}-{self.value_choice_item}"))
        if os.path.exists(path):
            shutil.rmtree(path)


    def bin_choices_menu_add_mod_from_file(self, *_):
        path = tkinter.filedialog.askopenfilename(title="选择 Mod 压缩包", filetypes=[("压缩文件", ["*.zip", "*.rar", "*.7z"])])
        if path:
            core.additional.add_mod2.add_mods([path])


    def bin_choices_menu_add_mod_from_dir(self, *_):
        path = tkinter.filedialog.askdirectory(title="选择 Mod 文件夹")
        if path:
            core.additional.add_mod2.add_mods([path])


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
        if not path: return
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
