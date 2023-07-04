# -*- coding:utf-8 -*-

import threading

from typing import Any, Union
from collections.abc import Iterable, Mapping

from . import exceptions
from . import structure



class TaskPool(object):
    def __init__(self, master: structure.Structure, task_pool_size: int = 20):
        if not isinstance(master, structure.Structure):
            raise TypeError("The master type is not Structure.")

        if not isinstance(task_pool_size, int):
            raise TypeError("The task_pool_size type is not int.")

        self.master = master

        self.__set_lock = threading._RLock()
        self.__table_answer = dict()
        self.__table_answer_lock = threading._RLock()
        self.__table_task = list()
        self.__table_task_lock = threading._RLock()
        self.__table_runing = dict()
        self.__table_runing_lock = threading._RLock()

        self.set_task_pool_size(task_pool_size)


    def newtask(self, task: Any, args: Iterable = (), kwds: Mapping = {}, answer: bool = True) -> int:
        """ ## 添加任务
        任务会在一个独立的控制线程中执行

        当任务池满时任务会在任务列表中等待，
        直到任务池有空闲再依次开始

        当任务抛出异常时，`answer` 参数不生效，
        异常结果仍然会被记录
        ```
        参数:
            task: 任务, 可调用对象
            args: 传递给 task 的位置参数
            kwds: 传递给 task 的键指参数
            answer: 是否记录返回值

        返回: int
            任务的 iid 值
            在 answer 为 True 时，任务结束后 task 的返回值会被保存
            使用 self.get_answer(iid) 获取返回值
        ```
        """
        iid = self.master.count
        data = {
            'iid': iid,
            'task': task,
            'answer': bool(answer),
            'args': args if isinstance(args, Iterable) else (args,),
            'kwds': kwds if isinstance(kwds, Mapping) else {},
        }

        with self.__table_task_lock:
            self.__table_task.append(data)

        self.__auto_activate()
        return iid


    def join(self, iid: int, timeout: Union[int, float, None] = None) -> Union[bool, None]:
        """ ## 等待直到任务终止
        这会阻塞调用线程，直到任务正常结束或异常终止
        ```
        参数:
            iid: 任务的 iid 值
            timeout: 超时时间 秒
        返回:
            当任务还未开始时返回 False
            当任务已经结束时返回 True
            当等待发生超时或结束时返回 None
            当任务不存在, 没有记录返回值或被清除时抛出 IidNotExistError 异常
        ```
        """
        if not isinstance(iid, int):
            raise TypeError("The iid type is not int.")

        with self.__table_task_lock:
            iidlst = [x['iid'] for x in self.__table_task]
            if iid in iidlst:
                return False

        with self.__table_answer_lock:
            # if (self.__table_answer){return True;}
            if iid in self.__table_answer: return True

        # ! 不得不说, 这种缩进确实很难看
        with self.__table_runing_lock:
            if iid in self.__table_runing:
                unit = self.__table_runing[iid] # 等待的过程中不应该占用锁

            else:
                raise exceptions.IidNotExistError("The iid does not exist.")

        unit.join(timeout)
        return None


    def get_answer(self, iid: int, delete: bool = False) -> Any:
        """ ## 获取返回值

        ```
        参数:
            iid: 任务的 iid 值, 由 self.newtask 的返回值提供
            delete: 是否删除这条记录
        ```
        """
        if not isinstance(iid, int):
            raise TypeError("The iid type is not int.")

        with self.__table_answer_lock:
            if iid not in self.__table_answer:
                raise exceptions.IidNotExistError("The iid does not exist.")

            result = self.__table_answer[iid]

            if delete:
                self.__table_answer.pop(iid)

        self.__auto_activate()
        return result


    def get_task_pool_size(self) -> int:
        """ ## 获取任务池大小
        """
        with self.__set_lock:
            num = self.__taskPoolSize

        self.__auto_activate()
        return num


    def set_task_pool_size(self, size: int) -> None:
        """ ## 设置任务池大小
        """
        if not isinstance(size, int):
            raise TypeError("The size type is not int.")

        if size <= 1 and False:
            raise ValueError("一个螺旋桨照飞~!")

        if size <= 0:
            raise ValueError("没有螺旋桨照飞~!")

        with self.__set_lock:
            self.__taskPoolSize = size

        self.__auto_activate()
        return None


    def __task_unit(self, iid: int, task: Any, args: Iterable = (), kwds: Mapping = {}, answer: bool = True) -> SystemExit:
        """ ## 任务单元
        """
        try:
            result = task(*args, **kwds)
        except BaseException as e: # 捕获 BaseException 它将包含 Exception 和 SystemExit
            result = e
            answer = True

        if answer:
            with self.__table_answer_lock:
                self.__table_answer[iid] = result

        with self.__table_runing_lock:
            try: self.__table_runing.pop(iid)
            except Exception: ... # 这里应该不会出现错误

        self.__auto_activate()
        raise SystemExit()


    def __auto_activate(self) -> None:
        """ ## 自动激活任务
        任务池没有一个专用的控制线程来检查是否有任务可以启动

        因此需要用户在操作其他控制方法的同时检查一次

        包括任务在添加或结束时
        """
        try:
            self.__table_task_lock.acquire()
            self.__table_answer_lock.acquire()
            self.__table_runing_lock.acquire()

            task_num = len(self.__table_task)
            runing_num = len(self.__table_runing)
            pool_size = self.__taskPoolSize

            if task_num <= 0: return
            if pool_size - runing_num <= 0: return

            task = self.__table_task.pop(0)

            iid = task['iid']
            self.__table_runing[iid] = threading.Thread(None, self.__task_unit, f'AsyncTask-{iid}', (), kwargs=task, daemon=True)
            self.__table_runing[iid].start()

        except Exception as e:
            raise e

        finally:
            self.__table_task_lock.release()
            self.__table_answer_lock.release()
            self.__table_runing_lock.release()

        self.__auto_activate()

    addtask = newtask


__all__ = ["TaskPool"]
