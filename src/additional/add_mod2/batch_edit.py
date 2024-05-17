import os
import time
import hashlib
import tkinter
import datetime
import threading

import ttkbootstrap
from ttkbootstrap.constants import *

import core
import window
import widgets
from constant import T

from .add_mod_unit import AddModUnit


option_list_grading = ["G - 大众级", "P - 指导级", "R - 成人级", "X - 限制级"]



class BatchEditUnit (object):
    def __init__(self, master: tkinter.Misc, masterwindow: ttkbootstrap.Window = None):
        """## Mod 添加单元

        master: (tkinter.Misc) 父组件, 可以是 Window, Frame 或其它容器组件
        """
        self.master = master
        self.masterwindow = masterwindow

        self.e_wait = threading.Event()
        self.units = []
        self.pause_editing = True

        self.sha     = ""
        self.v_object  = ttkbootstrap.StringVar()
        self.v_name    = ttkbootstrap.StringVar()
        self.v_grading = ttkbootstrap.StringVar()
        self.v_author  = ttkbootstrap.StringVar()
        self.v_explain = ttkbootstrap.StringVar()
        self.v_tags    = ttkbootstrap.StringVar()

        self.v_object .trace_add("write", self._object_update)
        self.v_name   .trace_add("write", self._name_update)
        self.v_grading.trace_add("write", self._grading_update)
        self.v_author .trace_add("write", self._author_update)
        self.v_explain.trace_add("write", self._explain_update)
        self.v_tags   .trace_add("write", self._tags_update)

        self.v_name.set("不适用")
        self.install()


    def install(self):
        self.mistake_msg = "\n".join([
            "在进入批量编辑模式时",
            "输入框会调整为出现次数最多的元素",
            "你需要对其进行一次编辑否则它不会被应用"
        ])

        self.information = ttkbootstrap.Frame(self.master)
        self.information.pack(side=TOP, fill=X)

        self.mistake = ttkbootstrap.Label(self.master, text=self.mistake_msg)
        self.mistake.pack(side=TOP, fill=X, pady=10)

        self.information.columnconfigure(1, weight=1)
        self.w_label_sha     = ttkbootstrap.Label(self.information, text="SHA: ")
        self.w_label_object  = ttkbootstrap.Label(self.information, text="作用对象：")
        self.w_label_name    = ttkbootstrap.Label(self.information, text="模组名称：")
        self.w_label_grading = ttkbootstrap.Label(self.information, text="年龄分级：")
        self.w_label_author  = ttkbootstrap.Label(self.information, text="模组作者：")
        self.w_label_explain = ttkbootstrap.Label(self.information, text="附加描述：")
        self.w_label_tags    = ttkbootstrap.Label(self.information, text="类型标签：")

        self.w_label_sha_result = ttkbootstrap.Label   (self.information, text="批量编辑模式")
        self.w_combobox_object  = ttkbootstrap.Combobox(self.information, width=60, textvariable=self.v_object)
        self.w_entry_name       = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_name)
        self.w_combobox_grading = ttkbootstrap.Combobox(self.information, width=60, textvariable=self.v_grading, values=option_list_grading)
        self.w_combobox_author  = ttkbootstrap.Combobox(self.information, width=60, textvariable=self.v_author)
        self.w_entry_explain    = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_explain)
        self.w_entry_tags       = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_tags)

        self.w_button_tags = ttkbootstrap.Button(self.information, text="+", bootstyle=(OUTLINE, SUCCESS), command=self.set_tags)

        self.w_label_sha     .grid(row=0, column=0, sticky=E, padx=(0, 0), pady=(0, 0))
        self.w_label_object  .grid(row=1, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        self.w_label_name    .grid(row=2, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        self.w_label_grading .grid(row=3, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        self.w_label_author  .grid(row=4, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        self.w_label_explain .grid(row=5, column=0, sticky=E, padx=(0, 0), pady=(5, 0))
        self.w_label_tags    .grid(row=6, column=0, sticky=E, padx=(0, 0), pady=(5, 0))

        self.w_label_sha_result .grid(row=0, column=1, sticky=EW, padx=(5, 0), pady=(0, 0))
        self.w_combobox_object  .grid(row=1, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.w_entry_name       .grid(row=2, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.w_combobox_grading .grid(row=3, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.w_combobox_author  .grid(row=4, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.w_entry_explain    .grid(row=5, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))
        self.w_entry_tags       .grid(row=6, column=1, sticky=EW, padx=(5, 0), pady=(5, 0))

        self.w_button_tags.grid(row=6, column=2, sticky=W, padx=(5, 0), pady=(5, 0))


        _alt = window.annotation_toplevel.register
        _alt(self.w_label_sha_result, T.ANNOADD.SHA_BATCH, 2)
        _alt(self.w_combobox_object, T.ANNOADD.OBJECT, 2)
        _alt(self.w_entry_name, T.ANNOADD.NAME, 2)
        _alt(self.w_combobox_grading, T.ANNOADD.GRADING, 2)
        _alt(self.w_combobox_author, T.ANNOADD.AUTHOR, 2)
        _alt(self.w_entry_explain, T.ANNOADD.EXPLAIN, 2)
        _alt(self.w_entry_tags, T.ANNOADD.TAGS, 2)
        _alt(self.w_button_tags, T.ANNOADD.TAG_SELECT_TOOL, 2)


    def initial(self, units: list[AddModUnit]):
        self.pause_editing = True
        self.units = units
        attr_name_list = [
            "v_object",
            "v_name",
            "v_grading",
            "v_author",
            "v_explain",
            "v_tags",
            ]

        for attr_name in attr_name_list:
            str_lst = []
            for unit in self.units:
                unit: AddModUnit

                variable = getattr(unit, attr_name)
                variable: ttkbootstrap.StringVar

                str_lst.append(variable.get())

            most_common = find_most_common(str_lst)

            variable = getattr(self, attr_name)
            variable: ttkbootstrap.StringVar
            variable.set(most_common)

        self.pause_editing = False


    def  _object_update(self, *_):
        if self.pause_editing: return
        value = self.v_object.get()
        for unit in self.units:
            unit: AddModUnit
            unit.v_object.set(value)


    def  _name_update(self, *_):
        if self.pause_editing: return
        value = self.v_name.get()
        for unit in self.units:
            unit: AddModUnit
            unit.v_name.set(value)


    def  _grading_update(self, *_):
        if self.pause_editing: return
        value = self.v_grading.get()
        for unit in self.units:
            unit: AddModUnit
            unit.v_grading.set(value)


    def  _author_update(self, *_):
        if self.pause_editing: return
        value = self.v_author.get()
        for unit in self.units:
            unit: AddModUnit
            unit.v_author.set(value)


    def  _explain_update(self, *_):
        if self.pause_editing: return
        value = self.v_explain.get()
        for unit in self.units:
            unit: AddModUnit
            unit.v_explain.set(value)


    def  _tags_update(self, *_):
        if self.pause_editing: return
        value = self.v_tags.get()
        for unit in self.units:
            unit: AddModUnit
            unit.v_tags.set(value)


    def set_tags(self, *_):
        o_tags = core.module.tags_manage.get_tags()
        s_tags = self.v_tags.get()
        res = widgets.dialogs.select2ags("选择标签", o_tags, s_tags, parent=self.masterwindow)
        self.v_tags.set(" ".join(res))


def find_most_common(lst: list[str]):
    if not lst: return ""

    string_count = {}

    for string in lst:
        if string in string_count:
            string_count[string] += 1
        else:
            string_count[string] = 1

    string_list = [x for x in string_count if x]
    string_list.sort(key=lambda x: string_count[x], reverse=True)

    if not string_list: return ""

    most_common_strings = []

    string = string_list.pop(0)
    count = string_count[string]
    most_common_strings.append(string)

    for string in string_list:
        if string_count[string] == count:
            most_common_strings.append(string)
        else:
            break

    final_string = " | ".join(most_common_strings)

    return final_string
