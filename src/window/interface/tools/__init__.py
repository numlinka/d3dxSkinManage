# -*- coding: utf-8 -*-


import ttkbootstrap

import core

from constant import *
from . import ocd_crop
from . import cache_cleanup
from . import old_migration
from . import development
from . import launch_script
import widgets

TEXT_OCD_CROP = """
强迫症截图工具

你是否因为在截取预览图时位置和大小参差不齐而烦恼
但是现在没有关系
这个工具可以帮助你截取位置和大小一致的图片
为你的强迫症之路舔砖 Java (加瓦)
"""

TEXT_CACHE_CLEANUP = """
缓存清理工具

在 1.5 版本之后会大量使用缓存提高操作速度
但这些缓存不会因为 Mod 的删除而删除
可以通过此工具扫描并清理这些无用的缓存文件
释放硬盘空间
"""

TEXT_OLD_MIGRATION = """
旧版 Mod 管理器数据迁移工具

迁移 3DMiModsManage 的数据到 d3dsSkinManage
解决老用户因为旧版数据太多迁移到新版麻烦的问题
有一些小小的 BUG
但总体上是成功的
"""

TEXT_DEVELOPMENT = """
开发者调试工具

警告！你需要对自己的行为负责，自行承担后果
该工具可以略过行为检查直接进行操作
操作不当会导致其他模块故障或损坏数据库
你已经被警告过了
"""

TEXT_TAGS_EDIT = """
可选标签编辑工具

你可以在此编辑 Mod 标签的可选内容和顺序
使用空格和换行来分隔多个标签
已出现过的标签会被追加到可选内容中
如果出现错误请自行修复
"""


LAUNCH_SCRIPT = """
生成启动脚本

让你不再需要通过程序来启动 3DMiGoto
注意，这里只提供最基础的启动方式
如果你需要实现更复杂的逻辑
请自行富化脚本内容
"""



class containe ():
    rejection_count = 1


class Tools (object):
    def __init__(self, master, *_):
        self.super_master = master
        self.install()


    def install(self):
        self.master = widgets.ScrollFrame(self.super_master)
        self.master.pack(fill="both", expand=True)

        self.frame_1 = ttkbootstrap.Frame(self.master)
        self.frame_2 = ttkbootstrap.Frame(self.master)
        self.frame_3 = ttkbootstrap.Frame(self.master)
        self.frame_1.pack(side="left", fill="y", padx=10, pady=10)
        self.frame_2.pack(side="left", fill="y", padx=(0, 10), pady=10)
        self.frame_3.pack(side="left", fill="y", padx=(0, 10), pady=10)

        self.button_ocd_crop = ttkbootstrap.Button(self.frame_1, text=TEXT_OCD_CROP, bootstyle="outline", command=self.bin_open_ocd_crop)
        self.button_ocd_crop.pack(side="top", fill="x")

        self.button_cache_cleanup = ttkbootstrap.Button(self.frame_2, text=TEXT_CACHE_CLEANUP, bootstyle="outline", command=self.bin_open_cache_cleanup)
        self.button_cache_cleanup.pack(side="top", fill="x")

        self.button_old_version_migration = ttkbootstrap.Button(self.frame_1, text=TEXT_OLD_MIGRATION, bootstyle="outline", command=self.bin_open_old_migration)
        self.button_old_version_migration.pack(side="top", fill="x", pady=(10, 0))

        self.button_development_debug = ttkbootstrap.Button(self.frame_1, text=TEXT_DEVELOPMENT, bootstyle="outline", command=self.bin_open_development_debug)
        self.button_development_debug.pack(side="top", fill="x", pady=(10, 0))

        self.button_tags_edit = ttkbootstrap.Button(self.frame_2, text=TEXT_TAGS_EDIT, bootstyle="outline", command=self.bin_open_tags_edit)
        self.button_tags_edit.pack(side="top", fill="x", pady=(10, 0))

        self.button_launch_script = ttkbootstrap.Button(self.frame_3, text=LAUNCH_SCRIPT, bootstyle="outline", command=self.bin_open_launch_script)
        self.button_launch_script.pack(side="top", fill="x")

        core.construct.event.register(E.USER_LOGGED_IN, self.master.bin_auto_resize)


    def initial(self):
        ...


    def bin_open_ocd_crop(self, *_):
        ocd_crop.OCDCrop()


    def bin_open_cache_cleanup(self, *_):
        cache_cleanup.CacheCleanup()


    def bin_open_old_migration(self, *_):
        old_migration.OldMigration()


    def bin_open_development_debug(self, *_):
        if containe.rejection_count <= 3:
            containe.rejection_count += 1
            core.window.messagebox.showerror(title="访问被拒绝", message="开发者调试工具：访问被拒绝")
            return

        development.Development()


    def bin_open_tags_edit(self, *_):
        res = widgets.dialogs.textedit(title="可选标签编辑", content=core.module.tags_manage.get_tags_content(), parent=core.window.mainwindow)
        core.module.tags_manage.update_content(res, True)


    def bin_open_launch_script(self, *_):
        launch_script.LaunchScript()
