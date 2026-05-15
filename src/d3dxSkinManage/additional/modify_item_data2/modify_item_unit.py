# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import os
import tkinter

# site
import ttkbootstrap
from ttkbootstrap.constants import *

# libs
from libs import strutils

# local
import core
import module
import window
import widgets
from constant import T
from constant.E import *


option_list_grading = ["G - 大众级", "P - 指导级", "R - 成人级", "X - 限制级"]



class ModifyItemUnit (object):
    def __init__(self, sha: str, master: tkinter.Misc, callback, masterwindow: ttkbootstrap.Window = None):
        self.sha = sha
        self.master = master
        self.callback = callback
        self.masterwindow = masterwindow

        self.name = sha
        self.state = ""
        self.close = False
        self.old_object = ""

        self.v_object  = ttkbootstrap.StringVar()
        self.v_name    = ttkbootstrap.StringVar()
        self.v_grading = ttkbootstrap.StringVar()
        self.v_author  = ttkbootstrap.StringVar()
        self.v_explain = ttkbootstrap.StringVar()
        self.v_tags    = ttkbootstrap.StringVar()

        # self.v_get1_url = ttkbootstrap.StringVar()
        # self.v_get2_url = ttkbootstrap.StringVar()
        # self.v_get3_url = ttkbootstrap.StringVar()

        # self.v_get1_mode = ttkbootstrap.StringVar()
        # self.v_get2_mode = ttkbootstrap.StringVar()
        # self.v_get3_mode = ttkbootstrap.StringVar()

        self.v_object.trace_add("write", self._object_update)
        self.v_name.trace_add("write", self._name_update)
        self.install()


    def _state_update(self, *, name: str = ..., state: str = ...):
        if isinstance(name, str): self.name = name
        if isinstance(state, str): self.state = state
        self.callback(self.sha)


    def _set_mistake(self, text: str = ""):
        self.mistake.configure(text=text, bootstyle=DANGER)


    def _set_warn(self, text: str = ""):
        self.warn.configure(text=text, bootstyle=WARNING)


    def _object_update(self, *_):
        object_ = self.v_object.get()
        self._state_update(name=object_)
        if not module.mods_manage.object_name_class_prediction(object_):
            self._set_warn("无法预测对象名称的分类，该对象将会归于未分类")
        else:
            self._set_warn("")


    def _name_update(self, *_):
        self._state_update(state=self.v_name.get())


    def install(self):
        self.information = ttkbootstrap.Frame(self.master)
        self.information.pack(side=TOP, fill=X)

        self.mistake = ttkbootstrap.Label(self.master)
        self.mistake.pack(side=TOP, fill=X, pady=10)

        self.warn = ttkbootstrap.Label(self.master)
        self.warn.pack(side=TOP, fill=X, pady=0)

        self.information.columnconfigure(1, weight=1)
        self.w_label_sha     = ttkbootstrap.Label(self.information, text="SHA: ")
        self.w_label_object  = ttkbootstrap.Label(self.information, text="作用对象：")
        self.w_label_name    = ttkbootstrap.Label(self.information, text="模组名称：")
        self.w_label_grading = ttkbootstrap.Label(self.information, text="年龄分级：")
        self.w_label_author  = ttkbootstrap.Label(self.information, text="模组作者：")
        self.w_label_explain = ttkbootstrap.Label(self.information, text="附加描述：")
        self.w_label_tags    = ttkbootstrap.Label(self.information, text="类型标签：")
        self.w_label_get1    = ttkbootstrap.Label(self.information, text="下载地址：")
        self.w_label_get2    = ttkbootstrap.Label(self.information, text="下载地址：")
        self.w_label_get3    = ttkbootstrap.Label(self.information, text="下载地址：")

        self.w_label_sha_result = ttkbootstrap.Label   (self.information, text=self.sha)
        self.w_entry_object     = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_object)
        self.w_entry_name       = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_name)
        self.w_combobox_grading = ttkbootstrap.Combobox(self.information, width=60, textvariable=self.v_grading, values=option_list_grading)
        self.w_combobox_author  = ttkbootstrap.Combobox(self.information, width=60, textvariable=self.v_author)
        self.w_entry_explain    = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_explain)
        self.w_entry_tags       = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_tags)
        # self.w_entry_get1_url   = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_get1_url)
        # self.w_entry_get2_url   = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_get2_url)
        # self.w_entry_get3_url   = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_get3_url)

        self.w_button_tags      = ttkbootstrap.Button(self.information, text="+", bootstyle=(OUTLINE, SUCCESS), command=self.set_tags)
        # self.w_entry_get1_mode  = ttkbootstrap.Entry   (self.information, textvariable=self.v_get1_mode)
        # self.w_entry_get2_mode  = ttkbootstrap.Entry   (self.information, textvariable=self.v_get2_mode)
        # self.w_entry_get3_mode  = ttkbootstrap.Entry   (self.information, textvariable=self.v_get3_mode)


        self.w_label_sha     .grid(row=0, column=0, sticky=E, padx=(0, 0), pady=(0, 0))
        self.w_label_object  .grid(row=1, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        self.w_label_name    .grid(row=2, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        self.w_label_grading .grid(row=3, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        self.w_label_author  .grid(row=4, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        self.w_label_explain .grid(row=5, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        self.w_label_tags    .grid(row=6, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        # self.w_label_get1    .grid(row=7, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        # self.w_label_get2    .grid(row=8, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        # self.w_label_get3    .grid(row=9, column=0, sticky=E, padx=(0, 0), pady=(5, 0))

        self.w_label_sha_result .grid(row=0, column=1, sticky=EW, padx=(5, 0), pady=(0, 0))
        self.w_entry_object     .grid(row=1, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.w_entry_name       .grid(row=2, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.w_combobox_grading .grid(row=3, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.w_combobox_author  .grid(row=4, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.w_entry_explain    .grid(row=5, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.w_entry_tags       .grid(row=6, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        # self.w_entry_get1_url   .grid(row=7, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        # self.w_entry_get2_url   .grid(row=8, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        # self.w_entry_get3_url   .grid(row=9, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))

        self.w_button_tags      .grid(row=6, column=2, sticky=W, padx=(5, 0), pady=(5, 0))
        # self.w_entry_get1_mode  .grid(row=7, column=2, sticky=W, padx=(5, 0), pady=(5, 0))
        # self.w_entry_get2_mode  .grid(row=8, column=2, sticky=W, padx=(5, 0), pady=(5, 0))
        # self.w_entry_get3_mode  .grid(row=9, column=2, sticky=W, padx=(5, 0), pady=(5, 0))


        _alt = window.annotation_toplevel.register
        _alt(self.w_label_sha_result, T.ANNOADD.SHA, 2)
        _alt(self.w_entry_object, T.ANNOADD.OBJECT, 2)
        _alt(self.w_entry_name, T.ANNOADD.NAME, 2)
        _alt(self.w_combobox_grading, T.ANNOADD.GRADING, 2)
        _alt(self.w_combobox_author, T.ANNOADD.AUTHOR, 2)
        _alt(self.w_entry_explain, T.ANNOADD.EXPLAIN, 2)
        _alt(self.w_entry_tags, T.ANNOADD.TAGS, 2)
        _alt(self.w_button_tags, T.ANNOADD.TAG_SELECT_TOOL, 2)


    def set_tags(self, *_):
        o_tags = module.tags_manage.get_tags()
        s_tags = self.v_tags.get()
        res = widgets.dialogs.select2ags("选择标签", o_tags, s_tags, parent=self.masterwindow)
        self.v_tags.set(" ".join(res))


    def initial(self):
        data = module.mods_index.get_item(self.sha)
        self.v_object  .set( data["object"] )
        self.v_name    .set( data["name"] )
        self.v_grading .set( data.get("grading", "") )
        self.v_author  .set( data.get("author", "") )
        self.v_explain .set( data.get("explain", "").replace("\n", "\\n") )
        self.v_tags    .set( " ".join(data.get("tags", [])) )
        self.old_object = self.v_object.get()
        self.w_combobox_author.configure(values=module.author_manage.get_authors_list())


    def action_sure(self):
        # 检查数据是否合法
        z_object  = self.v_object.get().strip()
        z_name    = self.v_name.get().strip()
        z_grading = self.v_grading.get()[0] if self.v_grading.get() else ""
        z_author  = self.v_author.get().strip()
        z_explain = self.v_explain.get().strip()
        z_tags    = [x for x in self.v_tags.get().split(" ") if x]

        if not z_object:
            self._set_mistake("未填写 作用对象")
            self._state_update(state="[错误] 数据不完整")
            return

        if not z_name:
            self._set_mistake("未填写 模组名称")
            self._state_update(state="[错误] 数据不完整")
            return

        if not z_grading:
            self._set_mistake("未填写 年龄分级")
            self._state_update(state="[错误] 数据不完整")
            return

        if z_grading not in ["G", "P", "R", "X"]:
            self._set_mistake("年龄分级 只能是 G P R X 其中之一")
            self._state_update(state="[错误] 数据不完整")
            return

        newdata = {
            "object":   z_object,
            "name":     z_name,
            "author":   z_author,
            "grading":  z_grading,
            "explain":  strutils.escape_character_recognition(z_explain),
            "tags":     z_tags
        }

        if self.old_object != z_object:
            module.mods_manage.unload(self.old_object)

        module.mods_index.item_data_update(self.sha, newdata)
        self.action_cancel()


    def action_cancel(self):
        self.close = True
        self._state_update()


    def action_remove(self):
        result = module.mods_manage.remove(self.sha)
        if result is not None:
            window.messagebox.showinfo(title=result[0], message=result[1])
            return

        try:
            os.remove(os.path.join(core.env.directory.resources.mods, self.sha))

        except Exception:
            ...

        core.construct.event.set_event(MODS_INDEX_UPDATE)
        self.action_cancel()


    def action_delete(self):
        result = module.mods_manage.remove(self.sha)
        if result is not None:
            window.messagebox.showinfo(title=result[0], message=result[1])
            return

        module.mods_index.item_data_del(self.sha)

        try:
            os.remove(os.path.join(core.env.directory.resources.mods, self.sha))

        except Exception:
            ...

        core.construct.event.set_event(MODS_INDEX_UPDATE)
        self.action_cancel()
