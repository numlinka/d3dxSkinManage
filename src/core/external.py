# -*- coding: utf-8 -*-

import threading
import subprocess

from . import env


def is_main_thread(*args, **kwds) -> bool:
    return threading.current_thread() is threading.main_thread()


def x7z(from_file: str, to_path: str):
    PIPE = subprocess.PIPE
    DEVNULL = subprocess.DEVNULL
    command = (env.file.local.t7z, 'x', '-y', f'-o{to_path}', from_file)
    task = subprocess.Popen(command, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, cwd=env.base.cwd)
    task.wait()


def a7z(from_file: str, to_path: str):
    PIPE = subprocess.PIPE
    DEVNULL = subprocess.DEVNULL
    command = (env.file.local.t7z, 'a', '-t7z', to_path, from_file)
    task = subprocess.Popen(command, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, cwd=env.base.cwd)
    task.wait()
