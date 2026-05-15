# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import typing
import threading

# local
import core


class StopTaskExecution (Exception): ...


class TaskQueue (object):
    """
    Task Queue ( 任务队列 ) 最初并非为 d3dxSkinManage 项目设计的，而且当前的 TaskQueue 版本并未完善。
    """
    def __init__(self, name: str = ""):
        self._lock = threading.RLock()
        self.name = name
        self._isiid = 0
        self._table = {}
        self._queue = []


    def __sore_key(self, iid: str):
        with self._lock:
            return self._table[iid][0]


    def sort(self):
        with self._lock:
            self._queue = [x for x in self._table.keys()]
            self._queue.sort(key=self.__sore_key)


    def add_task(self, task: callable, order: int = 1000, iid: str = ..., need_params: bool = True) -> str:
        if not callable(task):
            raise TypeError("Task must be callable.")
        
        if not isinstance(order, int):
            raise TypeError("Order must be int.")

        if order < 0:
            raise ValueError("Order must be positive.")

        if not isinstance(iid, str) and iid is not Ellipsis:
            raise TypeError("Iid must be str.")


        with self._lock:
            if iid is Ellipsis:
                while True:
                    iid = f"Task-{self._isiid}"
                    self._isiid += 1

                    if iid not in self._table:
                        break

            self._table[iid] = (order, task, need_params)
            self.sort()


    def del_task(self, iid: str):
        with self._lock:
            if iid not in self._table:
                raise KeyError(f"Task with iid '{iid}' not found.")

            self._table.pop(iid)


    def get_iids(self) -> typing.Iterable:
        with self._lock:
            return self._table.keys()


    def execute(self, *args: typing.Iterable, **kwds: typing.Mapping):
        with self._lock:
            self.sort()
            for iid in self._queue:
                try:
                    order, task, need_params = self._table[iid]

                    try: core.log.debug(f"Execute task {iid} '{task.__name__}'")
                    except Exception: ...

                    if need_params: task(*args, **kwds)
                    else: task()

                except StopTaskExecution:
                    try: core.log.warning(f"StopTaskExecution raised in task {iid} '{task.__name__}'")
                    except Exception: ...
                    break

                except Exception as e:
                    try: core.log.warning(f"Exception in task {iid} '{task.__name__}': {e}")
                    except Exception: ...
                    continue

            else:
                ...

    exec = execute
    call = execute
    __call__ = execute



askexit = TaskQueue("askexit")


__all__ = ["TaskQueue", "StopTaskExecution"]
