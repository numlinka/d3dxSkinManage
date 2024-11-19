# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import os
import copy
import shutil
import fnmatch
import threading

# local
import core
from constant import *

# self
from .exceptions import *


class ModsManage (object):
    def __init__(self):
        # 分类参照
        self.__reference_classification = {}
        # dict :: 分类名称 : 对象名称[]
        # 储存完整的分类作为参照体

        # 已加载 Mods
        self.__table_loads = {}
        # dict :: 对象名称 : SHA
        # 记录已加载 Mod 的 SHA

        # 本地 SHA 列表
        self.__local_sha_lst = []
        # 记录已下载的 SHA 列表

        # 本地 对象 列表
        self.__local_object_lst = []
        # 仅记录已下载 SHA 的对象名称列表

        # 本地 对象: SHA 列表
        self.__local_object_sha_lst = {}
        # dict :: 对象名称 : SHA
        # 仅记录本地已有对象的 SHA 列表

        # 本地 分类: 对象 列表
        self.__classification = {}
        # dict :: 分类名称 : 对象名称[]
        # 仅记录本地已有的分类及其对象名称列表

        # 本地 分类 列表
        self.__classification_lst = []
        # 仅记录本地已有的分类列表

        # 操作锁
        self.__call_lock = threading._RLock()


    def clear(self):
        core.log.debug("清除缓存索引数据...", L.MODULE_MODS_MANAGE)
        with self.__call_lock:
            self.__reference_classification = {}
            self.__table_loads = {}
            self.__local_sha_lst = []
            self.__local_object_lst = []
            self.__local_object_sha_lst = {}
            self.__classification = {}
            self.__classification_lst = []


    def update_reference_classification(self):
        core.log.debug("更新分类参照...", L.MODULE_MODS_MANAGE)
        with self.__call_lock:
            for class_ in os.listdir(core.userenv.directory.classification):
                path = os.path.join(core.userenv.directory.classification, class_)
                if not os.path.isfile(path): continue

                try:
                    with open(path, "r", encoding="utf-8") as file_object:
                        file_content = file_object.readlines()

                except Exception as _:
                    core.window.messagebox.showwarning(title="分类参照文件读取错误", message=f"{path}\n\n该文件无法解读为有效的分类参照\n请删除该文件，或检查该文件的编码")
                    continue

                object_list = [x.strip() for x in file_content if x.strip()]

                self.__reference_classification[class_] = object_list


    def update_local_sha_list(self):
        core.log.debug("更新本地 SHA...", L.MODULE_MODS_MANAGE)
        with self.__call_lock:
            SHA_lst = core.module.mods_index.get_all_sha_list()
            for SHA in os.listdir(core.env.directory.resources.mods):
                path = os.path.join(core.env.directory.resources.mods, SHA)
                if not os.path.isfile(path): continue
                if SHA not in SHA_lst: continue
                self.__local_sha_lst.append(SHA)


    def update_local_object_list(self):
        core.log.debug("构建本地对象列表...", L.MODULE_MODS_MANAGE)
        with self.__call_lock:
            self.__local_object_lst = []
            for SHA in self.__local_sha_lst:
                item = core.module.mods_index.get_item(SHA)
                if item is None:
                    continue

                object_name = item["object"]
                if object_name in self.__local_object_lst:
                    continue

                self.__local_object_lst.append(object_name)


    def update_local_object_sha_list(self):
        core.log.debug("构建本地对象 SHA 列表...", L.MODULE_MODS_MANAGE)
        with self.__call_lock:
            _local_SHA_set = set(self.__local_sha_lst)
            for object_ in self.__local_object_lst:
                SHA_list = core.module.mods_index.get_object_sha_list(object_)
                intersection = set(SHA_list) & _local_SHA_set
                self.__local_object_sha_lst[object_] = list(intersection)


    def update_local_classification(self):
        core.log.debug("构建本地分类...", L.MODULE_MODS_MANAGE)
        with self.__call_lock:
            # _object_lst = set(self.__local_object_lst)
            _object_lst = self.__local_object_lst
            _object_lst_surplus = set(self.__local_object_lst)

            for class_, object_list in self.__reference_classification.items():
                # intersection = _object_lst & set(object_list)
                # if len(intersection) == 0: continue

                intersection = set()

                for reference_object_name in object_list:
                    for object_name in self.__local_object_lst:
                        if fnmatch.fnmatch(object_name, reference_object_name):
                            intersection |= {object_name}


                self.__classification[class_] = list(intersection)
                # _object_lst -= intersection
                _object_lst_surplus -= set(intersection)

            if len(_object_lst) != 0:
                if "未分类" not in self.__classification: self.__classification["未分类"] = []
                self.__classification["未分类"] += list(_object_lst_surplus)


            # ! 本地分类列表
            # self.__classification_lst = [x for x in self.__classification if x != '未分类']

            # ! 参照分类列表
            self.__classification_lst = [x for x in self.__reference_classification if x != '未分类']

            self.list_sort()

            # if '未分类' in self.__classification: self.__classification_lst += ['未分类']
            self.__classification_lst += ['未分类']


    def update_loaded_mods(self):
        core.log.debug("更新加载模组...", L.MODULE_MODS_MANAGE)
        with self.__call_lock:
            _accident = []
            _conflict = []
            all_sha_list = core.module.mods_index.get_all_sha_list()
            for SHA in os.listdir(core.userenv.directory.work_mods):
                # 排除禁用字段开头的名称
                if SHA.lower().startswith(K.DISABLED): continue

                # 排除 _ 字段开头的名称
                if SHA.startswith("_"): continue

                # 排除不是文件夹的名称
                path = os.path.join(core.userenv.directory.work_mods, SHA)
                if not os.path.isdir(path): continue

                # 检查 SHA 是否在 all_sha_list 中
                if SHA not in all_sha_list:
                    _accident.append(SHA)
                    continue # ! 检查到意外的 SHA

                # 检查是否有相同的 object 被加载
                object_ = core.module.mods_index.get_item(SHA)['object']
                if object_ in self.__table_loads:
                    _conflict.append(SHA)
                    continue
                else:
                    self.__table_loads[object_] = SHA

            # 移除意外的和冲突的 SHA
            if len(_accident) >= 1:
                core.log.warn(f"检查到意外的 SHA: {_accident}", L.MODULE_MODS_MANAGE)

            if len(_conflict) >= 1:
                core.log.warn(f"检查到冲突的 SHA: {_conflict}", L.MODULE_MODS_MANAGE)

            for SHA in _accident + _conflict:
                self.remove(SHA)


    def list_sort(self):
        with self.__call_lock:
            try:
                # 对分类列表进行排序
                # self.__classification_lst.sort(key=_list_sort_for_class)
                sort_for_class_list(self.__classification_lst)

                # 对每个分类的 object 列表进行排序
                # for _, lst in self.__classification.items(): lst.sort(key=_list_sort_for_object)
                for class_name, object_list in self.__classification.items():
                    sort_for_object_list(class_name, object_list)

                # 对每个对象的 item 列表排序
                # for _, lst in self.__local_object_sha_lst.items(): lst.sort(key=_list_sort_for_item)
                for object_name, item_lost in self.__local_object_sha_lst.items():
                    sort_for_item_list(object_name, item_lost)

            except Exception as e:
                core.log.error("缓存数据表排序失败: {e}", __name__)


    def get_class_list(self) -> list[str]:
        """获取分类列表副本"""
        return self.__classification_lst.copy()


    def get_reference_class_list(self) -> list[str]:
        """获取参照分类列表副本"""
        return list(self.__reference_classification.keys())


    def get_reference_object_list(self, class_: str) -> list[str]:
        """获取参照分类对象列表副本"""
        return self.__reference_classification.get(class_, []).copy()


    def get_object_list(self, class_: str) -> list[str]:
        """获取分类对象列表副本"""
        return self.__classification.get(class_, []).copy()


    def get_object_sha_list(self, object_: str) -> list[str]:
        """获取对象 SHA 列表副本"""
        return self.__local_object_sha_lst.get(object_, []).copy()


    def get_load_object_sha(self, object_: str) -> str | None:
        """获取已加载对象 SHA"""
        return self.__table_loads.get(object_, None)


    def get_table_loads(self) -> dict[str, str]:
        """获取已加载对象 SHA 缓存"""
        return copy.deepcopy(self.__table_loads)


    def is_load_object(self, object_: str):
        """是否为已加载对象"""
        if object_ in self.__table_loads: return True
        return False


    def object_name_class_prediction(self, object_name: str) -> list[str]:
        """对象名称分类预测"""
        with self.__call_lock:
            class_list = []
            for class_name, reference_list in self.__reference_classification.items():
                for reference in reference_list:
                    if fnmatch.fnmatch(object_name, reference):
                        class_list.append(class_name)
                        break

            return class_list


    def is_load_sha(self, sha: str):
        """是否为已加载 SHA"""
        with self.__call_lock:
            for key, value in self.__table_loads.items():
                if sha == value: return True
            else: return False


    def is_have_cache_load(self, sha: str):
        """是否为拥有缓存的 SHA"""
        path = os.path.join(core.userenv.directory.work_mods, f"{K.DISABLED}-{sha}")
        return os.path.isdir(path)


    def is_local_sha(self, SHA: str):
        """是否为本地 SHA"""
        if SHA in self.__local_sha_lst: return True
        return False


    def refresh(self):
        core.log.info("刷新 Mods 管理索引缓存...", L.MODULE_MODS_MANAGE)
        self.clear()

        with self.__call_lock:
            self.update_reference_classification()
            self.update_local_sha_list()
            self.update_local_object_list()
            self.update_local_object_sha_list()
            self.update_local_classification()
            self.update_loaded_mods()

        core.construct.event.set_event(E.MODS_MANAGE_CACHE_REFRESHED)


    def load(self, SHA: str) -> None:
        core.log.debug(f"加载 Mod {SHA}", L.MODULE_MODS_MANAGE)
        with self.__call_lock:
            object_ = core.module.mods_index.get_item(SHA)['object']

            # 卸载冲突对象的 SHA Mod
            self.unload(object_)

            # 如果 SHA 已经被加载则不做任何操作
            if SHA == self.__table_loads.get(object_, None):
                return

            try:
                # 如果 SHA 存在且拥有禁用标识则去除
                dsname = f"{K.DISABLED}-{SHA}"
                if dsname in os.listdir(core.userenv.directory.work_mods):
                    old_path = os.path.join(core.userenv.directory.work_mods, dsname)
                    new_path = os.path.join(core.userenv.directory.work_mods, SHA)
                    os.rename(old_path, new_path)

                # 如果 SHA 不存在则从资源解压
                else:
                    from_file = os.path.join(core.env.directory.resources.mods, SHA)
                    to_path = os.path.join(core.userenv.directory.work_mods, SHA)

                    core.external.x7z(from_file, to_path)

            except FileNotFoundError:
                core.window.messagebox.showerror(title=f"操作中断：文件缺失", message=f"{e}")
                raise OperationInterrupted

            except PermissionError as e:
                core.window.messagebox.showerror(title=f"操作中断：权限错误", message=f"{e}\n\n当前文件正在被其他程序访问\n请关闭该程序或资源管理器后重试")
                raise OperationInterrupted

            except Exception as e:
                core.window.messagebox.showerror(title=f"操作中断：未定义错误", message=f"{e.__class__}\n\n{e}")
                raise OperationInterrupted

            finally:
                ...

            # 更新缓存
            self.__table_loads[object_] = SHA
            core.record.LOAD_MOD_SHA = SHA

            core.construct.event.set_event(E.MOD_LOADED)
            return None


    def unload(self, object_: str) -> None:
        core.log.debug(f"卸载 Mod {object_}", L.MODULE_MODS_MANAGE)
        with self.__call_lock:
            SHA = self.__table_loads.get(object_, None)
            if SHA is None: return None

            try:
                if self.is_have_cache_load(SHA):
                    core.log.debug(f"清除 Mod {SHA} 缓存", L.MODULE_MODS_MANAGE)
                    self.remove(f"{K.DISABLED}-{SHA}")
                # 在文件夹前面加上禁用标识
                dsname = f"{K.DISABLED}-{SHA}"
                old_path = os.path.join(core.userenv.directory.work_mods, SHA)
                new_path = os.path.join(core.userenv.directory.work_mods, dsname)
                os.rename(old_path, new_path)
                # target = os.path.join(core.userenv.directory.work_mods, SHA)
                # shutil.rmtree(target)

            except FileNotFoundError:
                ...

            except PermissionError as e:
                core.window.messagebox.showerror(title=f"操作中断：权限错误", message=f"{e}\n\n当前文件正在被其他程序访问\n请关闭该程序或资源管理器后重试")
                raise OperationInterrupted

            except Exception as e:
                core.window.messagebox.showerror(title=f"操作中断：未定义错误", message=f"{e.__class__}\n\n{e}")
                raise OperationInterrupted

            finally:
                ...

            core.record.UNLOAD_MOD_SHA = SHA
            core.construct.event.set_event(E.MOD_UNLOADED)
            del self.__table_loads[object_]


    def remove(self, SHA: str) -> tuple[str, str] | None:
        with self.__call_lock:
            target = os.path.join(core.userenv.directory.work_mods, SHA)
            try:
                if not os.path.isdir(target): return None
                shutil.rmtree(target)
                return None

            except PermissionError as e:
                return ("操作中断：权限错误", f"{e}\n\n当前文件正在被其他程序访问\n请关闭该程序或资源管理器后重试")

            except Exception as e:
                return ("操作中断：未知错误", f"{e.__class__}\n{e}")


# ! 已弃用
def _list_sort_for_item_name(key) -> str:
    try:
        return core.module.mods_index.get_item(key)["name"]

    except Exception:
        return key


# ! 已弃用
def _list_sort_for_item_grading(key) -> str:
    try:
        return core.module.mods_index.get_item(key)[K.INDEX.GRADING]

    except Exception:
        return key


CLASS_NAME_SORT_LIST = ["角色", "武器", "."]


# ! 已弃用
def _list_sort_for_class_name(key) -> int:
    for index, value in enumerate(CLASS_NAME_SORT_LIST):
        if value in key:
            return index

    else:
        return len(CLASS_NAME_SORT_LIST)


def _list_sort_for_item(key) -> tuple[str, str]:
    try:
        first = core.module.mods_index.get_item(key)[K.INDEX.GRADING]

    except Exception as _:
        first = key

    try:
        second = core.module.mods_index.get_item(key)[K.INDEX.NAME]

    except Exception as _:
        second = key

    return (first, second)


def _list_sort_for_object(key) -> str:
    return key


def _list_sort_for_class(key) -> tuple[int, str]:
    for index, value in enumerate(CLASS_NAME_SORT_LIST):
        if value in key:
            return (index, key)

    else:
        return (len(CLASS_NAME_SORT_LIST), key)


def sort_for_class_list(class_list: list[str]):
    class_list.sort(key=_list_sort_for_class)


def sort_for_object_list(class_name: str, object_list: list[str]):
    object_list.sort(key=_list_sort_for_object)


def sort_for_item_list(object_name: str, item_list: list[str]):
    item_list.sort(key=_list_sort_for_item)
