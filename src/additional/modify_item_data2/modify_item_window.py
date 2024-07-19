# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import threading

# site
import ttkbootstrap
from ttkbootstrap.constants import *

# local
import window
import module
from constant import T

# self
from . import modify_item_unit
from . import batch_edit



class structunit (object):
    frame: ttkbootstrap.Frame
    unit: modify_item_unit.ModifyItemUnit



class ModifyItemWindow (object):
    def __init__(self):
        self._lock = threading.RLock()
        self.window = ttkbootstrap.Toplevel("修改 item 信息")
        window.methods.fake_withdraw(self.window)
        self.bin_withdraw()
        self.window.protocol("WM_DELETE_WINDOW", self.bin_withdraw)
        self.window.transient(window.mainwindow)
        self.window.focus_set()
        self.install()

        self._task: dict[str: structunit] = {}
        self._is_first_deiconify = True


    def install(self):
        self.wtv_tasklist = ttkbootstrap.Treeview(self.window, selectmode=EXTENDED, show=TREE, height=10)
        self.wfe_content = ttkbootstrap.Frame(self.window)
        self.wtv_tasklist.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.wfe_content.pack(side=RIGHT, fill=BOTH, expand=True, padx=(0, 5), pady=5)

        self.wfe_option = ttkbootstrap.Frame(self.wfe_content)
        self.wfe_unit = ttkbootstrap.Frame(self.wfe_content)
        self.wfe_option.pack(side=BOTTOM, fill=X)
        self.wfe_unit.pack(side=TOP, fill=BOTH, expand=True, pady=(0, 5))

        self.wfe_nowunit = ttkbootstrap.Frame(self.wfe_content)
        self.wfe_nowunit.pack(side=TOP, fill=BOTH, expand=True)
        self.wtv_tasklist.bind("<<TreeviewSelect>>", self.select_update)

        self.wbn_sure   = ttkbootstrap.Button(self.wfe_option, text="确定", width=10, bootstyle=(OUTLINE, INFO   ), command=self.bin_sure)
        self.wbn_cancel = ttkbootstrap.Button(self.wfe_option, text="取消", width=10, bootstyle=(OUTLINE, SUCCESS), command=self.bin_cancel)
        self.wbn_remove = ttkbootstrap.Button(self.wfe_option, text="移除", width=10, bootstyle=(OUTLINE, WARNING), command=self.bin_remove)
        self.wbn_delete = ttkbootstrap.Button(self.wfe_option, text="销毁", width=10, bootstyle=(OUTLINE, DANGER ), command=self.bin_delete)
        self.wbn_select = ttkbootstrap.Button(self.wfe_option, text="全选", width=10, bootstyle=(OUTLINE, INFO   ), command=self.bin_select)
        self.wbn_sure.pack(side=RIGHT)
        self.wbn_cancel.pack(side=RIGHT, padx=(0, 5))
        self.wbn_remove.pack(side=RIGHT, padx=(0, 5))
        self.wbn_delete.pack(side=RIGHT, padx=(0, 5))
        self.wbn_select.pack(side=LEFT, padx=(0, 5))


        self.wfe_batch_edit = ttkbootstrap.Frame(self.wfe_unit)
        self.batch_edit_unit = batch_edit.BatchEditUnit(self.wfe_batch_edit, self.window)


        _alt = window.annotation_toplevel.register
        _alt(self.wbn_sure, T.ANNOADD.SURE_MODIFY, 2)
        _alt(self.wbn_cancel, T.ANNOADD.CANCEL, 2)
        _alt(self.wbn_remove, T.ANNOADD.REMOVE, 2)
        _alt(self.wbn_delete, T.ANNOADD.DELETE, 2)
        _alt(self.wbn_select, T.ANNOADD.ALL_SELECT, 2)


    def select_update(self, *_):
        self.wfe_nowunit.pack_forget()
        result = self.wtv_tasklist.selection()

        if not result: return

        elif len(result) == 1:
            sha = result[0]
            task_unit = self._task[sha]
            task_unit: structunit
            self.wfe_nowunit = task_unit.frame

        else:
            units = [self._task[sha].unit for sha in result]
            self.wfe_nowunit = self.wfe_batch_edit
            self.batch_edit_unit.initial(units)

        self.wfe_nowunit.pack(side=TOP, fill=BOTH, expand=True)


    def _callback_state_update(self, sha: str):
        with self._lock:
            if sha not in self._task: return

            unitstruct = self._task[sha]
            unitstruct: structunit

            if not unitstruct.unit.close:
                name = unitstruct.unit.name
                state = unitstruct.unit.state
                self.wtv_tasklist.item(sha, text=f"{name}\n{state}")
                return

            self.wtv_tasklist.delete(sha)
            del self._task[sha]

            result = self.wtv_tasklist.get_children()
            if len(result) != 0: return
            self.bin_withdraw()


    def bin_withdraw(self, *_):
        self.window.withdraw()
        self._is_first_deiconify = True


    def bin_sure(self, *_):
        with self._lock:
            result = self.wtv_tasklist.selection()
            for sha in result:
                unitstruct = self._task[sha]
                unitstruct: structunit
                unitstruct.unit.action_sure()


    def bin_cancel(self, *_):
        with self._lock:
            result = self.wtv_tasklist.selection()
            for sha in result:
                unitstruct = self._task[sha]
                unitstruct: structunit
                unitstruct.unit.action_cancel()


    def bin_remove(self, *_):
        with self._lock:
            result = self.wtv_tasklist.selection()
            for sha in result:
                unitstruct = self._task[sha]
                unitstruct: structunit
                unitstruct.unit.action_remove()


    def bin_delete(self, *_):
        with self._lock:
            result = self.wtv_tasklist.selection()
            for sha in result:
                unitstruct = self._task[sha]
                unitstruct: structunit
                unitstruct.unit.action_delete()


    def bin_select(self, *_):
        with self._lock:
            all_items = self.wtv_tasklist.get_children()
            self.wtv_tasklist.selection_set(all_items)


    def modify(self, sha: str):
        if module.mods_index.get_item(sha) is None: return

        with self._lock:
            if sha not in self._task:
                task_unit = structunit()
                task_unit.frame = ttkbootstrap.Frame(self.wfe_unit)
                task_unit.unit = modify_item_unit.ModifyItemUnit(sha, task_unit.frame, self._callback_state_update, self.window)
                self._task[sha] = task_unit
                self.wtv_tasklist.insert("", END, sha, text=sha)

                task_unit.unit.initial()

            self.wtv_tasklist.selection_set(sha)
            self.window.deiconify()

            if self._is_first_deiconify:
                self._is_first_deiconify = False
                self.window.update()
                window.methods.center_window_for_window(self.window, window.mainwindow)

