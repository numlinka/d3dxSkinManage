# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# 主线程进入主循环
ENTER_MAINPOOL = "enter-mainpool"

# 用户登录
USER_LOGGED_IN = "user-logged-in"

# 用户注销
USER_LOGGED_OUT = "user-logged-out"

# 有 mod 被加载
MOD_LOADED = "mod-loaded"

# 有 mod 被卸载
MOD_UNLOADED = "mod-unloaded"

# mods index 已经更新
MODS_INDEX_UPDATE = "mods-index-refreshed"

# mods 管理缓存已经刷新
MODS_MANAGE_CACHE_REFRESHED = "mods-manage-cache-refreshed"

# 列表选中
WINDOW_MODS_MANAGE_TS_CLASS = "window-mods-manage-treeview-select-classification"
WINDOW_MODS_MANAGE_TS_OBJECT = "window-mods-manage-treeview-select-object"
WINDOW_MODS_MANAGE_TS_CHOICE = "window-mods-manage-treeview-select-choice"

# 列表更新
WINDOW_MODS_MANAGE_TV_CLASS_UPDATE = "window-mods-manage-treeview-classification-update"
WINDOW_MODS_MANAGE_TV_OBJECT_UPDATE = "window-mods-manage-treeview-object-update"
WINDOW_MODS_MANAGE_TV_CHOICE_UPDATE = "window-mods-manage-treeview-choice-update"

# 缩略图加载完成
THUMBNAIL_LOADED = "thumbnail-loaded"

# Mod 下载任务变动
MOD_DOWNLOAD_TASK_ALTERATION = "mod-download-task-alteration"


__all__ = [
    "ENTER_MAINPOOL",
    "USER_LOGGED_IN",
    "USER_LOGGED_OUT",
    "MOD_LOADED",
    "MOD_UNLOADED",
    "MODS_INDEX_UPDATE",
    "MODS_MANAGE_CACHE_REFRESHED",
    "WINDOW_MODS_MANAGE_TS_CLASS",
    "WINDOW_MODS_MANAGE_TS_OBJECT",
    "WINDOW_MODS_MANAGE_TS_CHOICE",
    "WINDOW_MODS_MANAGE_TV_CLASS_UPDATE",
    "WINDOW_MODS_MANAGE_TV_OBJECT_UPDATE",
    "WINDOW_MODS_MANAGE_TV_CHOICE_UPDATE",
    "THUMBNAIL_LOADED",
    "MOD_DOWNLOAD_TASK_ALTERATION"
]
