# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# local
import core
from constant import *


def initial():
    core.log.info("初始化信号事件...", L.CORE)

    core.construct.event.register(E.ENTER_MAINPOOL, when_entering_mainpool)
    core.construct.event.register(E.USER_LOGGED_IN, user_logged_in)

    core.construct.event.register(E.MODS_INDEX_UPDATE, lambda *_: core.sync.addtask("刷新模组管理", core.module.mods_manage.refresh))
    core.construct.event.register(E.MODS_MANAGE_CACHE_REFRESHED, update_all_list)
    core.construct.event.register(E.THUMBNAIL_LOADED, update_all_list)

    core.construct.event.register(E.MOD_LOADED, update_objects_list)
    core.construct.event.register(E.MOD_UNLOADED, update_objects_list)

    core.construct.event.register(E.WINDOW_MODS_MANAGE_TS_CLASS, update_objects_list)
    core.construct.event.register(E.WINDOW_MODS_MANAGE_TS_OBJECT, update_choices_list)
    core.construct.event.register(E.WINDOW_MODS_MANAGE_TS_OBJECT, update_preview)
    core.construct.event.register(E.WINDOW_MODS_MANAGE_TS_CHOICE, update_preview)
    core.construct.event.register(E.MOD_DOWNLOAD_TASK_ALTERATION, update_warehouse_list)


def when_entering_mainpool():
    core.sync.addtask("检查更新", core.module.update.check)
    core.sync.addtask("inform", core.window.inform.check)
    core.sync.addtask("初始化登录用户列表", core.window.login.initial)
    core.sync.addtask("加载插件", core.module.plugins.main)
    core.sync.addtask("登录就绪", core.window.ready_login)
    core.sync.addtask("自动登录检查", core.window.auto_login_check)

    # core.construct.taskpool.newtask(core.window.treeview_thumbnail.add_image_from_redirection_config_file, (core.env.file.resources.redirection, ))


def user_logged_in():
    core.sync.addtask("加载所有 index 文件", core.module.index_manage.auto_load_all_index_file)
    core.sync.addtask("刷新模组管理", core.module.mods_manage.refresh)
    core.sync.addtask('更新 d3dx 信息', core.window.interface.d3dx_manage.update)
    core.sync.addtask('更新模组仓库列表', core.window.interface.mods_warehouse.refresh)


def update_all_list():
    update_choices_list()
    update_objects_list()
    update_classification_list()
    update_warehouse_list()


def update_classification_list():
    core.window.mainwindow.after(0, core.window.interface.mods_manage.update_classification_list)


def update_objects_list():
    core.window.mainwindow.after(0, core.window.interface.mods_manage.update_objects_list)


def update_choices_list():
    core.window.mainwindow.after(0, core.window.interface.mods_manage.update_choices_list)
    # core.construct.taskpool.newtask(core.window.interface.modsmanage.update_choices_list)

def update_preview():
    core.window.mainwindow.after(0, core.window.interface.mods_manage.sbin_update_preview)


def update_warehouse_list():
    core.window.mainwindow.after(0, core.window.interface.mods_warehouse.refresh)
