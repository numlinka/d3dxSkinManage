# -*- coding:utf-8 -*-

import threading

from typing import Any, Union
from collections.abc import Iterable, Mapping

from . import exceptions
from . import structure



class Event(object):
    def __init__(self, master: structure.Structure, event_list: list[str] = ...):
        if not isinstance(master, structure.Structure):
            raise TypeError("The master type is not Structure.")

        if event_list is Ellipsis:
            event_list = []

        if not isinstance(event_list, list):
            raise TypeError("The eventList type is not list.")

        for item in event_list:
            if not isinstance(item, str):
                raise TypeError("The item type in the list is not str.")

        self.master = master

        self.__set_lock = threading._RLock()
        self.__table_event = []
        self.__table_event_lock = threading._RLock()

        self.__signal = {}
        self.__wait = {}
        self.__call_lock = threading._RLock()

        self.add_event(*event_list)


    def wait(self, event: str, timeout: Union[int, float, None] = None) -> bool:
        """ ## 等待事件
        这会阻塞调用线程，直到事件被触发或发生超时

        ```
        参数:
            event: 事件
            timeout: 超时时间 秒

        返回: bool
            事件被触发时停止阻塞并返回 True
            发生超时时返回 False
        ```
        """
        if not isinstance(event, str):
            raise TypeError("The event type is not str.")

        try:
            self.__table_event_lock.acquire()
            self.__call_lock.acquire()

            if event not in self.__table_event:
                raise exceptions.EventNotExistError("The event does not exist.")

            if event not in self.__wait: self.__wait[event] = []

            unit = threading.Event()
            self.__wait[event].append(unit)

        except Exception as e:
            raise e

        finally:
            self.__table_event_lock.release()
            self.__call_lock.release()

        return unit.wait(timeout)


    def register(self, event: str, task: Any, args: Iterable = ..., kwds: Mapping = ...) -> int:
        """ ## 注册触发任务
        在接收到对应的事件信号时执行该任务

        ```
        参数:
            event: 事件
            task: 任务
            args: 传递给 task 的参数
            kwds: 传递给 task 的参数

        返回: int
            iid, 任务的 iid 值
            可以使用 self.unregister(iid) 注销触发任务
        ```
        """
        if not isinstance(event, str):
            raise TypeError("The event type is not str.")
        
        if args is Ellipsis: args = ()
        if kwds is Ellipsis: kwds = {}

        try:
            self.__table_event_lock.acquire()
            self.__call_lock.acquire()

            if event not in self.__table_event:
                raise exceptions.EventNotExistError("The event does not exist.")

            if event not in self.__signal: self.__signal[event] = {}

            iid = self.master.count
            self.__signal[event][iid] = (
                task,
                args if isinstance(args, Iterable) else (args,), 
                kwds if isinstance(kwds, Mapping) else {}
            )

        finally:
            self.__table_event_lock.release()
            self.__call_lock.release()

        return iid


    def unregister(self, iid: int) -> None:
        """ ## 注销触发任务

        ```
        参数:
            iid: 任务的 iid 值, 由 self.register 的返回值提供
        ```
        """
        if not isinstance(iid, int):
            raise TypeError("The iid type is not int.")

        with self.__call_lock:
            for event in self.__signal:
                self.__signal[event].pop(iid, None)

        return None


    def add_event(self, *name: str) -> None:
        """ ## 添加事件

        ```
        参数:
            name: 事件名称
        ```
        """
        for item in name:
            if not isinstance(item, str):
                raise TypeError("The name type is not str.")

        with self.__table_event_lock:
            for item in name:
                if item in self.__table_event:
                    raise exceptions.EventAlreadyExistsError("The event name already exists.")

                self.__table_event.append(item)

        return None


    def set_event(self, name: str) -> None:
        """ 触发事件

        ```
        参数:
            name: 事件名称
        ```
        """
        if not isinstance(name, str):
            raise TypeError("The name type is not str.")
        
        try:
            self.__call_lock.acquire()
            self.__set_lock.acquire()
            self.__table_event_lock.acquire()

            if name not in self.__table_event:
                raise exceptions.EventNotExistError("The event does not exist.")

            if name in self.__wait:
                # for _ in range(len(self.__wait[name])):
                #     unit = self.__wait[name].pop(0)
                #     unit.set()
                event_lst = self.__wait[name]
                self.__wait[name] = []
                for unit in event_lst:
                    unit.set()

            if name in self.__signal:
                for _, value in self.__signal[name].items():
                    task, args, kwds = value
                    self.master.eventtaskpool.newtask(task, args, kwds)

        finally:
            self.__call_lock.release()
            self.__set_lock.release()
            self.__table_event_lock.release()


__all__ = ["Event"]
