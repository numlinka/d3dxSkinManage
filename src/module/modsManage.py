# -*- coding: utf-8 -*-

import os
import shutil

import core


class safety(object):
    @staticmethod
    def listdir(path):
        if not os.path.isdir(path): return []
        else: return os.listdir(path)


class ModsManage(object):
    def __init__(self):
        self.clear()


    def clear(self):
        self.__reference_classification = {} # 分类参照

        self.__table_loads = {} # 已加载 Mods - object_: SHA

        self.__local_SHA_lst = [] # 本地 SHA 列表
        self.__local_object_lst = [] # 本地 对象 列表
        self.__local_object_SHA_lst = {} # 本地 对象: SHA 列表

        self.__classification = {} # 本地 分类: 对象 列表
        self.__classification_lst = [] # 本地 分类 列表


    def refresh(self):
        core.Log.info(f"更新模组缓存数据表")
        self.clear()

        # 更新分类参照
        for class_ in safety.listdir(core.environment.user.classification):
            path = os.path.join(core.environment.user.classification, class_)
            if not os.path.isfile(path): continue

            with open(path, 'r', encoding='utf-8') as file_object:
                file_content = file_object.readlines()

            object_list = [x.strip() for x in file_content if x.strip()]

            self.__reference_classification[class_] = object_list


        # 更新本地 SHA
        SHA_lst = core.Module.ModsIndex.get_all_SHA_list()
        for SHA in safety.listdir(core.environment.resources.mods):
            path = os.path.join(core.environment.resources.mods, SHA)
            if not os.path.isfile(path): continue
            if SHA not in SHA_lst: continue
            self.__local_SHA_lst.append(SHA)


        # 构建本地对象列表
        self.__local_object_lst = list({core.Module.ModsIndex.get_item(x)['object'] for x in self.__local_SHA_lst})


        # 构建本地对象 SHA 列表
        _local_SHA_set = set(self.__local_SHA_lst)
        for object_ in self.__local_object_lst:
            SHA_list = core.Module.ModsIndex.get_object_SHA_list(object_)
            intersection = set(SHA_list) & _local_SHA_set
            self.__local_object_SHA_lst[object_] = list(intersection)


        # 构建本地分类
        _object_lst = set(self.__local_object_lst)

        for class_, object_list in self.__reference_classification.items():
            intersection = _object_lst & set(object_list)
            if len(intersection) == 0: continue

            self.__classification[class_] = list(intersection)
            _object_lst -= intersection

        if len(_object_lst) != 0:
            if '未分类' not in self.__classification: self.__classification['未分类'] = []
            self.__classification['未分类'] += list(_object_lst)


        # 更新加载模组
        _accident = []
        _conflict = []
        SHA_lst = core.Module.ModsIndex.get_all_SHA_list()
        for SHA in safety.listdir(core.environment.user.loadMods):
            path = os.path.join(core.environment.user.loadMods, SHA)
            if not os.path.isdir(path): continue
            if SHA not in SHA_lst: _accident.append(SHA); continue # ! 检查到意外的 SHA
            object_ = core.Module.ModsIndex.get_item(SHA)['object']
            if object_ in self.__table_loads: _conflict.append(SHA); continue # ! 检查到冲突的 SHA
            self.__table_loads[object_] = SHA

        # 移除意外的和冲突的 SHA
        if len(_accident) >= 1: core.Log.warn(f"检查到意外的 SHA: {_accident}")
        if len(_conflict) >= 1: core.Log.warn(f"检查到冲突的 SHA: {_conflict}")
        for SHA in _accident + _conflict:
            self.remove(SHA)


        # todo 对分类的每个列表进行排序
        for _, lst in self.__local_object_SHA_lst.items(): lst.sort(key=_name_sort)
        for _, lst in self.__classification.items(): lst.sort()

        self.__classification_lst = [x for x in self.__classification if x != '未分类']

        # todo 对分类列表进行排序
        self.__classification_lst.sort()

        if '未分类' in self.__classification: self.__classification_lst += ['未分类']


    def get_class_list(self) -> list[str]:
        return [x for x in self.__reference_classification] + ['未分类']
        # return self.__classification_lst.copy()


    def get_object_list(self, class_: str) -> list[str]:
        return self.__classification.get(class_, []).copy()


    def get_object_SHA_list(self, object_: str) -> list[str]:
        return self.__local_object_SHA_lst.get(object_, []).copy()


    def get_load_object_SHA(self, object_: str) -> str | None:
        return self.__table_loads.get(object_, None)


    def is_load_object(self, object_: str):
        if object_ in self.__table_loads: return True
        return False


    def is_local_SHA(self, SHA: str):
        if SHA in self.__local_SHA_lst: return True
        return False


    def load(self, SHA: str) -> None:
        object_ = core.Module.ModsIndex.get_item(SHA)['object']
        from_file = os.path.join(core.environment.resources.mods, SHA)
        to_path = os.path.join(core.environment.user.loadMods, SHA)

        try: self.unload(object_)
        except Exception: ...

        core.External.x7z(from_file, to_path)

        self.__table_loads[object_] = SHA

        return None


    def unload(self, object_: str) -> None:
        SHA = self.__table_loads.get(object_, None)
        if SHA is None: return None

        try:
            target = os.path.join(core.environment.user.loadMods, SHA)
            shutil.rmtree(target)

        except FileNotFoundError:
            ...

        except Exception:
            ...

        finally:
            del self.__table_loads[object_]


    def remove(self, SHA: str) -> None:
        target = os.path.join(core.environment.user.loadMods, SHA)
        shutil.rmtree(target)



def _name_sort(key) -> str:
    try:
        return core.Module.ModsIndex.get_item(key)['name']

    except Exception:
        return key
