# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import sys
import argparse
import threading
import traceback

# libs
import libs.logop

# local
import module
from constant import *

# self
from . import env
from . import userenv
from . import basic_event
from . import external
from . import amend
from . import action


log = libs.logop.logging.Logging(stdout=False, asynchronous=True)
log.set_format("[$(.date) $(.time).$(.moment)] [$(.levelname)] [$(.thread)] $(.message) ($(.mark))")
log.add_op(libs.logop.logoutput.LogopStandardPlus())
log.add_op(libs.logop.logoutput.LogopFile())

log.info("initial...", L.CORE)

construct = module.construct.Structural(20, [getattr(E, x) for x in E.__all__])
sync = module.synchronization.SynchronizationTask()

__parser = argparse.ArgumentParser(description='Description of your program')
__parser.add_argument("--autologin", default="", type=str, help="Automatically log in to the specified user environment.")
__parser.add_argument("--noupdatecheck", default="", type=str, help="Turn off update checking.")

argv: argparse.Namespace


import window
import additional


class record (object):
    LOAD_MOD_SHA: str = ""
    UNLOAD_MOD_SHA: str = ""


# 最终退出信号
# 你不需要手动置位
# 除非你有特殊需求
_final_exit_signal = threading.Event()



def _save_env_config():
    env.configuration._con_asve_as_json(env.file.local.configuration)


def _save_user_config():
    userenv.configuration._con_asve_as_json(userenv.file.configuration)


def _set_final_exit_signal():
    _final_exit_signal.set()


def initial():
    action.askexit.add_task(_save_env_config, 15_000, "保存环境配置文件", False)
    action.askexit.add_task(_save_user_config, 15_100, "保存用户配置文件", False)
    action.askexit.add_task(log.close, 20_000, "关闭日志记录器", False)
    action.askexit.add_task(_set_final_exit_signal, 25_000, "设置最终退出信号", False)



def run():
    global argv
    try:
        initial()
        amend.env_config_amend()

    except Exception as e:
        log.error("配置文件数据修正错误", L.CORE)

    try:
        log.set_level(env.configuration.log_level)
        argv = __parser.parse_args() # 果然, 它不适合呆在这里

    except Exception as e:
        env.configuration.log_level = libs.logop.level.INFO

    log.warning(f"当前设备编号为：{env.uuid}", L.CORE)
    sync.start()
    window.initial()
    module.initial()
    basic_event.initial()
    additional.initial()

    log.info("进入主循环", L.WINDOW)
    construct.event.set_event(E.ENTER_MAINPOOL)

    try:
        window.mainwindow.mainloop()

    except Exception as e:
        exc = traceback.format_exc()
        log.error(f"{e.__class__}: {e}\n{exc}", L.WINDOW)

    finally:
        _final_exit_signal.wait()
        sys.exit()


def login(name):
    log.info(f"登录用户名 \"{name}\"", L.CORE_LOGIN)
    userenv.login(name)
    window._login(name)

    construct.event.set_event(E.USER_LOGGED_IN)


def logout():
    log.info(f"注销登录", L.CORE_LOGOUT)
    ...

    construct.event.set_event(E.USER_LOGGED_OUT)


__all__ = [
    "env"
    "structure"
]
