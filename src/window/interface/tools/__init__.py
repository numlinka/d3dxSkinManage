# Licensed under the GPL 3.0 License.
# d3dxSkinManage by numlinka.

# std
import types

# site
import ttkbootstrap
from ttkbootstrap.constants import *

# local
import module
import window
import widgets
from constant import T

# self
from . import ocd_crop
from . import cache_cleanup
from . import old_migration
from . import development
from . import launch_script


class ColumnUnit (object):
    frame: ttkbootstrap.Frame
    pack: bool = False
    button_list: list[ttkbootstrap.Button]



class Tools (object):
    def __init__(self, master, *_):
        self.super_master = master
        self._table: dict[int, ColumnUnit] = {}
        self.install()
        self.initial()


    def install(self):
        self.master = widgets.ScrollFrame(self.super_master, scb_pad=5)
        self.master.pack(fill=BOTH, expand=True, padx=5, pady=5)


    def add_button(self, text: str, command: types.FunctionType, column: int = 0):
        """## 添加按钮

        text: 按钮文本
        command: 回调函数 按钮点击事件
        column: 预期列 如果列出现空缺则按顺序添加
        """
        if column < 0:
            raise ValueError("column must be greater than or equal to 0.")

        if column not in self._table:
            # add new column
            column_unit = ColumnUnit()
            column_unit.frame = ttkbootstrap.Frame(self.master)
            column_unit.button_list = []
            self._table[column] = column_unit

        # add button
        column_unit = self._table[column]
        button = ttkbootstrap.Button(column_unit.frame, text=text, command=command, bootstyle=OUTLINE, takefocus=False)
        first = len(column_unit.button_list) == 0
        column_unit.button_list.append(button)
        button.pack(side=TOP, fill=X, padx=0, pady=(0 if first else 5, 0))

        if column_unit.pack: return

        if len(self._table) == 1:
            column_unit.frame.pack(side=LEFT, fill=Y, padx=5, pady=5)
            column_unit.pack = True
            return

        if max([x for x in self._table]) == column:
            column_unit.frame.pack(side=LEFT, fill=Y, padx=(0, 5), pady=5)
            column_unit.pack = True
            return

        else:
            self.repack_all_column()


    def repack_all_column(self):
        column_lst = list(self._table.keys())
        column_lst.sort()

        for column in column_lst:
            column_unit = self._table[column]
            if column_unit.pack == True: column_unit.frame.pack_forget()

        first = True
        for column in column_lst:
            column_unit = self._table[column]
            column_unit.frame.pack(side=LEFT, fill=Y, padx=(5 if first else 0, 5), pady=5)
            column_unit.pack = True
            first = False


    def initial(self):
        self.add_button(T.TEXT_OCD_CROP, bin_open_ocd_crop, 1)
        self.add_button(T.TEXT_OLD_MIGRATION, bin_open_old_migration, 1)
        self.add_button(T.TEXT_DEVELOPMENT, bin_open_development_debug, 1)
        self.add_button(T.TEXT_CACHE_CLEANUP, bin_open_cache_cleanup, 2)
        self.add_button(T.TEXT_TAGS_EDIT, bin_open_tags_edit, 2)
        self.add_button(T.TEXT_LAUNCH_SCRIPT, bin_open_launch_script, 2)



class containe ():
    rejection_count = 1



def bin_open_ocd_crop(*_):
    ocd_crop.OCDCrop()

def bin_open_old_migration(*_):
    old_migration.OldMigration()

def bin_open_development_debug(*_):
    if containe.rejection_count <= 3:
        containe.rejection_count += 1
        window.messagebox.showerror(title="访问被拒绝", message="开发者调试工具：访问被拒绝")
        return
    development.Development()

def bin_open_cache_cleanup(*_):
    cache_cleanup.CacheCleanup()

def bin_open_tags_edit(*_):
    res = widgets.dialogs.textedit(title="可选标签编辑", content=module.tags_manage.get_tags_content(), parent=window.mainwindow)
    module.tags_manage.update_content(res, True)

def bin_open_launch_script(*_):
    launch_script.LaunchScript()
