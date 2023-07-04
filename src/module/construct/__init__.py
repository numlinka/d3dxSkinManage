# -*- coding:utf-8 -*-

import threading

from typing import Any

from . import taskpool
from . import event

from . import structure
from .taskpool import *
from .event import *



class Structural (structure.Structure):
    def __init__(self, task_pool_size: int = 20, event_list: list = []):
        """ ## 建立一个结构体

        ```
        参数:
            task_pool_size: 任务池大小
            event_list: 初始信号列表
        ```
        """
        self.count: int

        self.__count = 0
        self.__count_lock = threading._RLock()

        self.taskpool = taskpool.TaskPool(self, task_pool_size)
        self.eventtaskpool = taskpool.TaskPool(self, task_pool_size)
        self.event = event.Event(self, event_list)


    def get_count(self) -> int:
        """ ## 获取原子计数

        ```
        每访问一次数值 +1
        可以使用 self.count 直接访问
        ```
        """
        with self.__count_lock:
            num = self.__count
            self.__count += 1

        return num


    def __getattribute__(self, __name: str) -> Any:
        if __name == 'count': return self.get_count()
        else: return super().__getattribute__(__name)


__all__ = []
