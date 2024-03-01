import os
import time
import hashlib
import tkinter
import datetime
import threading

import ttkbootstrap
from ttkbootstrap.constants import *

import core
import widgets

from . import keys
from constant import K
from additional.add_mod import FILE_WRAN_SIZE, FILE_WRAN_SIZE_MARK


option_list_grading = ["G - 大众级", "P - 指导级", "R - 成人级", "X - 限制级"]


class AddModUnitInputCache (object):
    object_ = ""
    grading = "G"
    author = ""
    explain = ""
    tags = ""



class AddModUnit (object):
    def __init__(self, taskid: str, master: tkinter.Misc, callback, path: str, filename: str = None, masterwindow: ttkbootstrap.Window = None):
        """## Mod 添加单元

        taskid: (str) 任务ID, 它应该是唯一的, 不变的, 在调用回调函数时会作为参数传递给回调函数
        master: (tkinter.Misc) 父组件, 可以是 Window, Frame 或其它容器组件
        callback: (function) 回调函数, 它会在任务单元的状态发生变化时被调用
        path: (str) 文件夹路径, 它应该是一个存在的文件或文件夹路径
        filename: (str) 文件名, 当你需要使用另为一个别名而非文件名作为默认名称时使用
        """
        self.taskid = taskid
        self.master = master
        self.original_path = path
        self.original_filename = filename
        self.callback = callback
        self.masterwindow = masterwindow

        self.name = taskid
        self.state = "等待指示..."
        self.s_ready = False    # 状态标识  表示已就绪  等待 导入确认
        self.s_mistake = False  # 状态标识  表示有错误  等待 close
        self.s_wait = False     # 状态标识  表示待确认  等待 self.e_wait 置位后继续操作
        self.s_cancel = False   # 状态标识  表示已取消  等待清理缓存
        self.e_wait = threading.Event()

        self.sha     = ""
        self.v_object  = ttkbootstrap.StringVar()
        self.v_name    = ttkbootstrap.StringVar()
        self.v_grading = ttkbootstrap.StringVar()
        self.v_author  = ttkbootstrap.StringVar()
        self.v_explain = ttkbootstrap.StringVar()
        self.v_tags    = ttkbootstrap.StringVar()

        self.v_name.set(self.name)
        self.v_name.trace_add("write", self._name_update)
        self.install()


    def _state_update(self, *, name: str = ..., state: str = ...):
        if isinstance(name, str): self.name = name
        if isinstance(state, str): self.state = state
        self.callback(self.taskid)


    def _set_mistake(self, text: str = ""):
        self.mistake.configure(text=text, bootstyle=DANGER)


    def _set_sha(self, sha: str):
        self.w_label_sha_result.configure(text=sha)


    def _name_update(self, *_):
        self._state_update(name=self.v_name.get())


    def install(self):
        self.information = ttkbootstrap.Frame(self.master)
        self.information.pack(side=TOP, fill=X)

        self.mistake = ttkbootstrap.Label(self.master)
        self.mistake.pack(side=TOP, fill=X, pady=10)

        self.information.columnconfigure(1, weight=1)
        self.w_label_sha     = ttkbootstrap.Label(self.information, text="SHA: ")
        self.w_label_object  = ttkbootstrap.Label(self.information, text="作用对象：")
        self.w_label_name    = ttkbootstrap.Label(self.information, text="模组名称：")
        self.w_label_grading = ttkbootstrap.Label(self.information, text="年龄分级：")
        self.w_label_author  = ttkbootstrap.Label(self.information, text="模组作者：")
        self.w_label_explain = ttkbootstrap.Label(self.information, text="附加描述：")
        self.w_label_tags    = ttkbootstrap.Label(self.information, text="类型标签：")

        self.w_label_sha_result = ttkbootstrap.Label   (self.information, text="等待扫描...")
        self.w_combobox_object  = ttkbootstrap.Combobox(self.information, width=60, textvariable=self.v_object)
        self.w_entry_name       = ttkbootstrap.Entry   (self.information, width=60, textvariable=self.v_name)
        self.w_combobox_grading = ttkbootstrap.Combobox(self.information, width=60, textvariable=self.v_grading)
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


    def set_tags(self, *_):
        o_tags = core.module.tags_manage.get_tags()
        s_tags = self.v_tags.get()
        res = widgets.dialogs.select2ags("选择标签", o_tags, s_tags, parent=self.masterwindow)
        self.v_tags.set(" ".join(res))


    def initial(self):
        threading.Thread(None, self.calculate, "AddModUnit.calculate", daemon=True).start()
        ...


    def calculate(self, *_):
        # 计算开始
        self._set_sha("调整可选项...")
        self._state_update(state=f"调整可选项...")
        class_name = core.window.interface.mods_manage.sbin_get_select_classification()
        if class_name is not None:
            object_list = core.module.mods_manage.get_reference_object_list(class_name)
            self.w_combobox_object.configure(values=object_list)

        self.w_combobox_grading.configure(values=option_list_grading)
        self.w_combobox_author.configure(values=core.module.author_manage.get_authors_list())


        object_ = core.window.interface.mods_manage.sbin_get_select_objects()
        if object_: self.v_object.set(object_)
        else: self.v_object.set(AddModUnitInputCache.object_)

        self.v_grading.set(AddModUnitInputCache.grading)
        self.v_author.set(AddModUnitInputCache.author)
        self.v_explain.set(AddModUnitInputCache.explain)
        self.v_tags.set(AddModUnitInputCache.tags)


        self._set_sha("正在扫描...")
        self._state_update(state=f"正在扫描...")

        # 检查文件名
        if os.path.isfile(self.original_path):
            self.filepath = self.original_path
            self.basename = os.path.basename(self.original_path)
            self.suffix = self.basename[self.basename.rfind(".") + 1:]
            self.prefix = self.basename[:self.basename.rfind(".")] if not isinstance(self.original_filename, str) else self.original_filename

        elif os.path.isdir(self.original_path):
            self.basename = os.path.basename(self.original_path)
            self.suffix = "7z"
            self.prefix = self.basename

        else:
            self._state_update(state="[错误] 未找到文件")
            self._set_mistake("无法找到有效文件或文件夹 请取消该任务")
            self.s_mistake = True
            return

        self.v_name.set(self.prefix)

        # 检查文件大小
        try:
            if os.path.isfile(self.original_path):
                original_size = os.path.getsize(self.original_path)

            elif os.path.isdir(self.original_path):
                original_size = get_folder_size(self.original_path)

            else:
                self._state_update(state="[错误] 发生了一个不应该出现的错误")
                self._set_mistake("无法扫描目标文件或文件夹 请取消该任务")
                self.s_mistake = True
                return

            if original_size > FILE_WRAN_SIZE:
                self._set_mistake(f"文件大小达到 {original_size/1024/1024:.2f} {FILE_WRAN_SIZE_MARK} 这超出常规 Mod 大小\n请点击确定以继续导入或取消该操作")
                self._state_update(state="[警告] 操作需要确认")
                self.s_wait = True
                self.e_wait.wait()
                self._set_mistake()

        except Exception as e:
            self._state_update(state=f"[错误] {e.__class__}")
            self._set_mistake(f"无法扫描目标文件或文件夹 请取消该任务")
            self.s_mistake = True
            return

        # 检查是否需要压缩
        try:
            if os.path.isdir(self.original_path):
                self._set_sha("正在压缩...")
                self._state_update(state=f"正在压缩...")


                tempfilename = hex(int(time.time() * 10 ** 8)) + ".7z"
                tempfilepath = os.path.join(core.env.directory.resources.cache, tempfilename)
                core.external.a7z(os.path.join(self.original_path, "*"), tempfilepath)
                self.filepath = tempfilepath

        except Exception as e:
            self._state_update(state=f"[错误] {e.__class__}")
            self._set_mistake(f"无法压缩目标文件夹 请取消该任务")
            self.s_mistake = True
            return


        if self.s_cancel:
            self.clear_cache()
            return

        self._set_sha("正在计算...")
        self._state_update(state=f"正在计算...")

        # 计算 SHA 值
        try:
            with open(self.filepath, "rb") as fileobject:
                self.content = fileobject.read()
                sha1 = hashlib.sha1()
                sha1.update(self.content)
                self.sha = sha1.hexdigest().upper()
                self._set_sha(self.sha)

        except Exception as e:
            self._state_update(state=f"[错误] {e.__class__}")
            self._set_mistake(f"无法计算 SHA 值 请取消该任务")
            self.s_mistake = True
            return

        self._state_update(state=f"最后检查...")

        # 检查 SHA 值是否已存在
        try:
            data = core.module.mods_index.get_item(self.sha)

            # 已存在的项目
            if core.module.mods_manage.is_local_sha(self.sha):
                self._set_mistake(f"该 SHA 值已经存在\n{data[K.INDEX.OBJECT]} - {data[K.INDEX.NAME]}\n请取消该任务")
                self._state_update(state="[错误] 已存在的项目")
                self.s_mistake = True
                return

            # 只有数据没有文件
            if data is not None:
                self.v_object  .set( data.get(K.INDEX.OBJECT) )
                self.v_name    .set( data.get(K.INDEX.NAME) )
                self.v_grading .set( data.get(K.INDEX.GRADING) )
                self.v_author  .set( data.get(K.INDEX.AUTHOR, "") )
                self.v_explain .set( data.get(K.INDEX.EXPLAIN, "") )
                self.v_tags    .set( " ".join(data.get(K.INDEX.TAGS, [])) )

        except Exception as e:
            self._state_update(state=f"[错误] {e.__class__}")
            self._set_mistake(f"无法读取数据 请取消该任务")
            self.s_mistake = True
            return

        # 富化数据
        for grading_text in option_list_grading:
            if self.v_grading.get() != grading_text[:1]: continue
            self.v_grading.set(grading_text)


        self.s_ready = True
        self._state_update(state=f"[就绪]")
        self._set_mistake()


    def action_sure(self):
        if self.s_mistake:
            self._state_update(state=keys.close)
            return

        if self.s_wait:
            self.s_wait = False
            self.e_wait.set()
            return

        if not self.s_ready:
            self._state_update(state="[错误] 未就绪")
            self._set_mistake("请等待计算完成")
            return

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

        # 计算 index 数据
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m")
        index_filepath = os.path.join(core.userenv.directory.mods_index, f"index_{date}.json")

        datacontent = {
            "object":   z_object,
            "type":     self.suffix,
            "name":     z_name,
            "author":   z_author,
            "grading":  z_grading,
            "explain":  z_explain,
            "tags":     z_tags
        }

        # 尝试将文件写入到 res
        try:
            with open(os.path.join(core.env.directory.resources.mods, self.sha), "wb") as fileobject:
                fileobject.write(self.content)

        except Exception as e:
            self._set_mistake(f"无法写入文件 {e.__class__}\n{e}\n请重试或取消该任务")
            self._state_update(state=f"[错误] 无法写入文件")
            return

        result = core.module.mods_index.item_data_update(self.sha, datacontent)
        if result is False:
            core.module.mods_index.item_data_new(index_filepath, self.sha, datacontent)
        self._state_update(state=keys.close)
        self.clear_cache()

        # 保存输入记忆
        AddModUnitInputCache.object_ = z_object
        AddModUnitInputCache.grading = z_grading
        AddModUnitInputCache.author = z_author
        AddModUnitInputCache.explain = z_explain
        AddModUnitInputCache.tags = " ".join(z_tags)


    def action_cancel(self):
        self.s_cancel = True
        self._state_update(state=keys.close)
        self.clear_cache()


    def clear_cache(self):
        try:
            if self.filepath == self.original_path: return
            os.remove(self.filepath)

        except Exception as _:
            ...


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size
