# -*- coding: utf-8 -*-

# std
import traceback

# self
from . import env
from . import userenv
from . import basic_event
from . import external
from . import amend

# libs
import libs.logop
from constant import *

import module

log = libs.logop.logging.Logging(stdout=False, asynchronous=True)
log.set_format("[$(.date) $(.time).$(.moment)] [$(.levelname)] [$(.thread)] $(.message) ($(.mark))")
log.add_op(libs.logop.logoutput.LogopStandardPlus())
log.add_op(libs.logop.logoutput.LogopFile())

log.info("initial...", L.CORE)

construct = module.construct.Structural(20, [getattr(E, x) for x in E.__all__])
sync = module.synchronization.SynchronizationTask()


import window
import additional


class record (object):
    LOAD_MOD_SHA: str = ""
    UNLOAD_MOD_SHA: str = ""



class tasklist (object):
    exit = [
        (env.configuration._con_asve_as_json, (env.file.local.configuration, )),
        (log.close, ())
    ]



def run():
    try:
        amend.env_config_amend()

    except Exception as e:
        log.error("配置文件数据修正错误", L.CORE)

    try:
        log.set_level(env.configuration.log_level)

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

    _exit()


def login(name):
    log.info(f"登录用户名 \"{name}\"", L.CORE_LOGIN)
    userenv.login(name)
    window._login(name)

    construct.event.set_event(E.USER_LOGGED_IN)


def logout():
    log.info(f"注销登录", L.CORE_LOGOUT)
    ...

    construct.event.set_event(E.USER_LOGGED_OUT)




def _exit():
    log.info("程序请求退出", L.CORE_EXIT)

    try:
        # todo 程序推出时应该保存用户数据
        tasklist.exit.insert(0, (userenv.configuration._con_asve_as_json, (userenv.file.configuration, )))

    except Exception as e:
        ...

    log.info("正在回收资源...", L.CORE_EXIT)
    for task in tasklist.exit:
        try:
            task[0](*task[1])

        except Exception as e:
            ...


__all__ = [
    "env"
    "structure"
]
