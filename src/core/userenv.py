# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import os
from os.path import join as __

# libs
import libs.econfiguration
import libs.dirstruct

# local
import core
from constant import *

# self
from . import env
from .exceptions import *
from .structure import *


user_name: str = ...
class configuration(libs.econfiguration.Configuration):
    GamePath: str


# class __directory (Directory):
#     mods_index: str = ...
#     classification: str = ...
#     work: str = ...
#     work_mods: str = ...
#     thumbnail: str = ...


# class file (static):
#     configuration: str = ...
#     redirection: str = ...


# directory = __directory()


class __UserenvWorkingDirectory (libs.dirstruct.Directory):
    mods_index = "modsIndex"
    classification = "classification"
    work = "work"
    work_mods = __(work, "Mods")
    thumbnail = "thumbnail"
    configuration = libs.dirstruct.FilePath("configuration")
    redirection = libs.dirstruct.FilePath(__(thumbnail, "_redirection.ini"))


directory: __UserenvWorkingDirectory
file: __UserenvWorkingDirectory
uwd: __UserenvWorkingDirectory


def login(__username: str):
    core.log.info("登录用户环境...", L.CORE_USERENV)
    global user_name
    global directory
    global file
    global uwd
    global configuration

    if user_name is not Ellipsis:
        core.log.error("用户已登录", L.CORE_USERENV)
        raise UserLoggedIn("用户已登录")

    if not os.path.isdir(__(env.base.home, __username)):
        core.log.error(f"登录用户名 \"{__username}\" 不存在", L.CORE_USERENV)
        raise UserDoesNotExist(f"登录用户名 \"{__username}\" 不存在")

    user_name = __username

    directory = __UserenvWorkingDirectory(__(env.base.home, __username))
    file = directory
    uwd = directory

    # directory.mods_index = __(env.base.home, __username, "modsIndex")
    # directory.classification = __(env.base.home, __username, "classification")
    # directory.work = __(env.base.home, __username, "work")
    # directory.work_mods = __(directory.work, "Mods")
    # directory.thumbnail = __(env.base.home, __username, "thumbnail")

    # file.configuration = __(env.base.home, __username, "configuration")
    # file.redirection = __(directory.thumbnail, "_redirection.ini")

    try: configuration = libs.econfiguration.Configuration(uwd.configuration)
    except Exception: configuration = libs.econfiguration.Configuration()
    core.construct.taskpool.newtask(core.window.treeview_thumbnail.add_image_from_redirection_config_file, (uwd.redirection, ))


def logout():
    core.log.info("注销用户环境...", L.CORE_USERENV)
    global user_name
    global configuration

    user_name = ...
    configuration = ...

    # directory.mods_index = ...
    # directory.classification = ...
    # directory.work = ...
    # directory.work_mods = ...

    # file.configuration = ...
