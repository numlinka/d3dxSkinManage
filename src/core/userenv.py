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
class configuration(libs.econfiguration.Configuration):
    GamePath: str


class __directory (Directory):
    mods_index: str = ...
    classification: str = ...
    work: str = ...
    work_mods: str = ...
    thumbnail: str = ...


class file (static):
    configuration: str = ...
    redirection: str = ...


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
    directory.thumbnail = __(env.base.home, __username, "thumbnail")

    file.configuration = __(env.base.home, __username, "configuration")
    file.redirection = __(directory.thumbnail, "_redirection.ini")

    try: configuration = libs.econfiguration.Configuration(file.configuration)
    except Exception: configuration = libs.econfiguration.Configuration()
    core.construct.taskpool.newtask(core.window.treeview_thumbnail.add_image_from_redirection_config_file, (file.redirection, ))


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
