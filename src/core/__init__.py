# -*- coding: utf-8 -*-

# * domain: core

import time
import threading
import subprocess

from typing import Iterable, Mapping

from . import environment
# from . import control

import module
import additional
import windows


class Module(object):
    IndexManage = module.indexManage.IndexManage()
    ModsIndex = module.modsIndex.ModsIndex()
    ModsManage = module.modsManage.ModsManage()
    ModsDownload = module.modsDownload.ModsDownload()


class UI(object):
    Windows = windows.Windows
    Messagebox = windows.Messagebox
    Status = windows.Status
    Login = windows.Login
    ModsManage = windows.ModsManage
    D3dxManage = windows.D3dxManage
    ModsWarehouse = windows.ModsWarehouse
    con = windows.con


class content(object):
    ThumbnailGroup = module.image.ImageTkThumbnailGroup(40, 40)



class Control(object):
    def __init__(self):
        self.running = False
        self.__controlLock = threading.RLock()
        self.__enableEvent = threading.Event()
        self.controlThread = threading.Thread(None, self.run, 'control', (), daemon=True)


        self.__taskTable = []


    def run(self):
        while True:
            self.__enableEvent.wait()
            with self.__controlLock:
                if not self.__taskTable:
                    self.__enableEvent.clear()
                    UI.Status.set_mark('S')
                    UI.Status.set_status('-')
                    continue

                else:
                    task = self.__taskTable.pop(0)
                    length = len(self.__taskTable)
                    UI.Status.set_mark(length)

            try:
                name, function_, args, kwds = task
                UI.Status.set_status(name)
                function_(*args, **kwds)
                time.sleep(environment.configuration.control_each_task_sleep_time_seconds)

            except Exception as e:
                UI.Status.set_mark('X')
                UI.Status.set_status(f'{e.__class__}: {e}', 1)
                self.clear()


    def addTask(self, name: str, functuon_: object, args: Iterable = (), kwds: Mapping = {}) -> None:
        if not isinstance(name, str): return
        if not isinstance(args, Iterable): return
        if not isinstance(kwds, Mapping): return

        content = (name, functuon_, args, kwds)

        with self.__controlLock:
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
            self.running = True


def login(userName):
    control.addTask('登录用户界面', UI.con.login, (userName, ))
    control.addTask('登录用户环境', environment.login, (userName, ))
    control.addTask('更新索引管理', Module.IndexManage.update)
    control.addTask('清除索引列表', Module.ModsIndex.clear)
    control.addTask('加载模组索引', Module.IndexManage.first_load)
    control.addTask('刷新模组管理', Module.ModsManage.refresh)
    control.addTask('刷新列表', UI.ModsManage.bin_refresh)
    control.addTask('更新 d3dx 信息', UI.D3dxManage.update)
    control.addTask('更新模组仓库列表', UI.ModsWarehouse.refresh)


control = Control()


def run():
    windows.initial()
    control.start()
    control.addTask('检查更新', module.update.check)
    control.addTask('加载缩略图', content.ThumbnailGroup.add_image_from_redirectionConfigFile, (environment.resources.f_redirection,))
    control.addTask('就绪', windows.ready)
    UI.Windows.mainloop()


class External(object):
    def IsMainThread(*args, **kwds) -> bool:
        return threading.current_thread() is threading.main_thread()


    @staticmethod
    def x7z(from_file: str, to_path: str):
        PIPE = subprocess.PIPE
        DEVNULL = subprocess.DEVNULL
        command = (environment.local.t7z, 'x', '-y', f'-o{to_path}', from_file)
        task = subprocess.Popen(command, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, cwd=environment.root.cwd)
        task.wait()


    def a7z(from_file: str, to_path: str):
        PIPE = subprocess.PIPE
        DEVNULL = subprocess.DEVNULL
        command = (environment.local.t7z, 'a', '-t7z', to_path, from_file)
        task = subprocess.Popen(command, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, cwd=environment.root.cwd)
        task.wait()


def Exit():
    try:
        environment.user.object_configuration._con_asve_as_json(environment.user.f_configuration)

    except Exception:
        ...

    UI.Windows.destroy()


UI.Windows.protocol('WM_DELETE_WINDOW', Exit)

