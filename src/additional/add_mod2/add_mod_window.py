# std
import threading

# install
import ttkbootstrap
from ttkbootstrap.constants import *

# project
import core

# self
from .add_mod_unit import AddModUnit
from .batch_edit import BatchEditUnit
from . import keys


class AddModWindow (object):
    def __init__(self):
        self._lock = threading.RLock()
        self.auto_increment_serial = 0
        self.window = ttkbootstrap.Toplevel("添加 Mods - 处理队列")
        core.window.methods.fake_withdraw(self.window)
        self.window.withdraw()
        self.window.protocol("WM_DELETE_WINDOW", self.window.withdraw)
        # self.window.transient(core.window.mainwindow)
        self.window.focus_set()
        self.install()

        self._task = {}

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

        self.wbn_sure   = ttkbootstrap.Button(self.wfe_option, text="确定", width=10, bootstyle=(OUTLINE, SUCCESS), command=self.bin_sure)
        self.wbn_cancel = ttkbootstrap.Button(self.wfe_option, text="取消", width=10, bootstyle=(OUTLINE, WARNING), command=self.bin_cancel)
        self.wbn_select = ttkbootstrap.Button(self.wfe_option, text="全选", width=10, bootstyle=(OUTLINE, INFO   ), command=self.bin_select)
        self.wbn_sure.pack(side=RIGHT)
        self.wbn_cancel.pack(side=RIGHT, padx=(0, 5))
        self.wbn_select.pack(side=LEFT, padx=(0, 5))


        self.wfe_batch_edit = ttkbootstrap.Frame(self.wfe_unit)
        self.batch_edit_unit = BatchEditUnit(self.wfe_batch_edit, self.window)


    def select_update(self, *_):
        if not main_threading_examine(self.select_update): return

        self.wfe_nowunit.pack_forget()
        result = self.wtv_tasklist.selection()

        if not result: return

        elif len(result) == 1:
            taskid = result[0]
            self.wfe_nowunit = self._task[taskid][keys.frame]

        else:
            units = [self._task[taskid][keys.unit] for taskid in result]
            self.wfe_nowunit = self.wfe_batch_edit
            self.batch_edit_unit.initial(units)

        self.wfe_nowunit.pack(side=TOP, fill=BOTH, expand=True)


    def _serial_increment(self) -> str:
        with self._lock:
            self.auto_increment_serial += 1
            result = f"TASK-{self.auto_increment_serial}"

        return result


    def _callback_state_update(self, taskid: str):
        if not main_threading_examine(self._callback_state_update, taskid): return

        with self._lock:
            if taskid not in self._task: return
            unit = self._task[taskid][keys.unit]
            unit: AddModUnit
            name = unit.name
            state = unit.state

            if state != keys.close:
                self.wtv_tasklist.item(taskid, text=f"{name}\n{state}")
                return

            del self._task[taskid]
            self.wtv_tasklist.delete(taskid)
            result = self.wtv_tasklist.get_children()
            if len(result) != 0: return
            self.window.withdraw()


    def bin_sure(self, *_):
        if not main_threading_examine(self.bin_sure): return

        with self._lock:
            result = self.wtv_tasklist.selection()
            for taskid in result:
                unit = self._task[taskid][keys.unit]
                unit: AddModUnit
                unit.action_sure()


    def bin_cancel(self, *_):
        if not main_threading_examine(self.bin_cancel): return

        with self._lock:
            result = self.wtv_tasklist.selection()
            for taskid in result:
                unit = self._task[taskid][keys.unit]
                unit: AddModUnit
                unit.action_cancel()


    def bin_select(self, *_):
        if not main_threading_examine(self.bin_select): return

        with self._lock:
            all_items = self.wtv_tasklist.get_children()
            self.wtv_tasklist.selection_set(all_items)


    # ! 已弃用
    def add_old(self, path: str):
        with self._lock:
            taskid = self._serial_increment()
            unit_frame = ttkbootstrap.Frame(self.wfe_unit)
            unit = AddModUnit(taskid, unit_frame, self._callback_state_update, path)
            self._task[taskid] = {keys.unit: unit, keys.frame: unit_frame}
            self.wtv_tasklist.insert("", END, taskid, text=taskid)
            self._callback_state_update(taskid)
            self.wtv_tasklist.selection_set(taskid)
            unit.initial()
            self.window.deiconify()


    def add(self, *paths: str):
        if not main_threading_examine(self.add, *paths): return

        with self._lock:
            self.window.deiconify()
            taskid_lst = []
            for path in paths:
                taskid = self._serial_increment()
                taskid_lst.append(taskid)
                unit_frame = ttkbootstrap.Frame(self.wfe_unit)
                unit = AddModUnit(taskid, unit_frame, self._callback_state_update, path, masterwindow=self.window)
                self._task[taskid] = {keys.unit: unit, keys.frame: unit_frame}
                self.wtv_tasklist.insert("", END, taskid, text=taskid)
                self._callback_state_update(taskid)
                self.wtv_tasklist.selection_set(taskid)

            for taskid in taskid_lst:
                unit = self._task[taskid][keys.unit]
                unit: AddModUnit
                self._callback_state_update(taskid)
                unit.initial()

            self.wtv_tasklist.selection_set(taskid)

            if self._is_first_deiconify:
                self.window.update()
                core.window.methods.center_window_for_window(self.window, core.window.mainwindow)
                self._is_first_deiconify = False


def main_threading_examine(func, *args) -> bool:
    """## 主线程检查

    检查当前线程是否为主线程
    如果 是   则直接返回True
    如果 不是 则调用主线程执行函数并返回False

    该函数用户将各类回调函数或触发函数包装成主线程执行
    避免多线程状态下争夺 tcl 锁资源导致的错误

    如果该函数应用广泛
    我可以考虑制作为装饰器
    """
    if threading.current_thread() is threading.main_thread():
        return True

    core.window.mainwindow.after(0, func, *args)
    return False
