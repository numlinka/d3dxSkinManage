# -*- coding: utf-8 -*-

# std
import os
from os.path import join as __

# n
import libs.econfiguration
from . import env
from .exceptions import *
from .structure import *
import core

# libs
from constant import *

user_name: str = ...
configuration: libs.econfiguration.Configuration = ...


class __directory (Directory):
    mods_index: str = ...
    classification: str = ...
    work: str = ...
    work_mods: str = ...


class file (static):
    configuration: str = ...


directory = __directory()


def login(__username: str):
    core.log.info("登录用户环境...", L.CORE_USERENV)
    global user_name
    global configuration

    if user_name is not Ellipsis:
        core.log.error("用户已登录", L.CORE_USERENV)
        raise UserLoggedIn("用户已登录")

    if not os.path.isdir(__(env.base.home, __username)):
        core.log.error(f"登录用户名 \"{__username}\" 不存在", L.CORE_USERENV)
        raise UserDoesNotExist(f"登录用户名 \"{__username}\" 不存在")

    user_name = __username
    directory.mods_index = __(env.base.home, __username, "modsIndex")
    directory.classification = __(env.base.home, __username, "classification")
    directory.work = __(env.base.home, __username, "work")
    directory.work_mods = __(directory.work, "Mods")

    file.configuration = __(env.base.home, __username, "configuration")

    try: configuration = libs.econfiguration.Configuration(file.configuration)
    except Exception: configuration = libs.econfiguration.Configuration()


def logout():
    core.log.info("注销用户环境...", L.CORE_USERENV)
    global user_name
    global configuration

    user_name = ...
    configuration = ...

    directory.mods_index = ...
    directory.classification = ...
    directory.work = ...
    directory.work_mods = ...

    file.configuration = ...
