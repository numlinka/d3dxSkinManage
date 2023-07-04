# -*- coding: utf-8 -*-

# std
import time
import threading
# import subprocess
import traceback
from typing import Any, Iterable, Mapping

# libs
import core
from constant import L


control_each_task_sleep_time_seconds = 0.2


class SynchronizationTask (object):
    def __init__(self):
        self.running = False
        self.__controlLock = threading.RLock()
        self.__enableEvent = threading.Event()
        self.controlThread = threading.Thread(None, self.run, "Synchronization", (), daemon=True)

        self.__taskTable = []


    def run(self):
        while True:
            self.__enableEvent.wait()
            with self.__controlLock:
                if not self.__taskTable:
                    self.__enableEvent.clear()
                    core.window.status.set_mark('S')
                    core.window.status.set_status('-')
                    continue

                else:
                    task = self.__taskTable.pop(0)
                    length = len(self.__taskTable)
                    core.window.status.set_mark(length)

            try:
                name, function_, args, kwds = task
                core.window.status.set_status(name)
                core.log.debug(f"执行同步任务 {name} {function_}", L.MODULE_SYNC)
                function_(*args, **kwds)
                time.sleep(control_each_task_sleep_time_seconds)

            except Exception as e:
                core.window.status.set_mark('X')
                exc = traceback.format_exc()
                core.log.error(f"同步任务抛出异常 {e.__class__}: {e}\n{exc}", L.MODULE_SYNC)
                core.window.status.set_status(f'{e.__class__}: {e}', 1)
                self.clear()


    def addtask(self, name: str, functuon_: object, args: Iterable = (), kwds: Mapping = {}) -> None:
        if not isinstance(name, str): return
        if not isinstance(args, Iterable): return
        if not isinstance(kwds, Mapping): return

        content = (name, functuon_, args, kwds)

        with self.__controlLock:
            core.log.debug(f"添加同步任务 {name} {functuon_}", L.MODULE_SYNC)
            self.__taskTable.append(content)
        self.__enableEvent.set()


    def clear(self):
        with self.__controlLock:
            self.__taskTable = []
        self.__enableEvent.clear()


    def start(self):
        with self.__controlLock:
            if self.controlThread.is_alive(): return None
            self.controlThread.start()
            core.log.info("同步任务线程启动", L.MODULE_SYNC)
            self.running = True
