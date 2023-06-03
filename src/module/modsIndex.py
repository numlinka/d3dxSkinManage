# -*- coding: utf-8 -*-

import os
import json

import numpy

class ModsIndex(object):
    def __init__(self):
        self.clear()


    def clear(self):
        self.__table_mods = {}
        self.__table_from = {}
        self.__cache_object = {}


    def __fill_variable(self, _mods: dict, _variable: dict) -> dict[str: dict]:
        for SHA, roitem in _mods.items():
            if 'get' not in roitem: continue

            for index, item in enumerate(roitem['get']):
                url = item['url']
                for key, value in _variable.items():
                    url = url.replace(f'($.{key})', value)

                item['url'] = url

        return _mods


    def __load_json(self, file: str) -> dict[str: dict]:
        if not os.path.isfile(file): raise FileNotFoundError()

        with open(file, 'r', encoding='utf-8') as file_object:
            file_content = file_object.read()

        data_content = json.loads(file_content)

        _variable = data_content.get('variable', {})
        _mods = data_content['mods']

        return self.__fill_variable(_mods, _variable)


    def __load_npy(self, file: str) -> dict[str: dict]:
        if not os.path.isfile(file): raise FileNotFoundError()

        numpy_object = numpy.load(file, allow_pickle=True)
        data_content = numpy_object.item()

        _variable = data_content.get('variable', {})
        _mods = data_content['mods']

        return self.__fill_variable(_mods, _variable)


    def load(self, file: str, mode: str, action: str = 'raise') -> None:
        if not os.path.isfile(file): raise FileNotFoundError()
        if mode not in ['json', 'npy']: raise ValueError()

        if mode == 'json': _mods = self.__load_json(file)
        elif mode == 'npy': _mods = self.__load_npy(file)
        else: raise ValueError()

        old_SHA = [x for x in self.__table_mods]
        new_SHA = [x for x in _mods]

        intersection = set(old_SHA) & set(new_SHA)
        length = len(intersection)
        if length != 0:
            # 返回，寻求处理方式
            if action == 'raise':
                return list(intersection)

            # 覆盖
            elif action == 'cover':
                ...

            # 跳过
            elif action == 'skip':
                for SHA in intersection: del _mods[SHA]

            # 意外
            else:
                return False

        if file not in self.__table_from: self.__table_from[file] = []
        self.__table_from[file] += [x for x in _mods]

        self.__table_mods.update(_mods)
        self.cache_update()

        return None


    def cache_update(self) -> None:
        for SHA, data in self.__table_mods.items():
            name = data['object']
            if name not in self.__cache_object: self.__cache_object[name] = []
            if SHA not in self.__cache_object[name]: self.__cache_object[name].append(SHA)

        return None


    def get_item(self, SHA: str) -> dict | None:
        return self.__table_mods.get(SHA, None)


    def get_object_list(self) -> list[str]:
        return [x for x in self.__cache_object]


    def get_object_SHA_list(self, name: str) -> list[str]:
        return self.__cache_object.get(name, []).copy()


    def get_all_SHA_list(self) -> list[str]:
        return [x for x in self.__table_mods]


    def get_SHA_from(self, SHA: str) -> str | None:
        for from_ in self.__table_from:
            if SHA in self.__table_from[from_]:
                return from_

        else:
            return None


    def item_data_update(self, SHA: str, data: dict) -> bool:
        if SHA not in self.__table_mods: return False

        self.__table_mods[SHA].update(data)
        self.cache_update()

        filepath = self.get_SHA_from(SHA)
        with open(filepath, 'r', encoding='utf-8') as fileobject: filecontent = fileobject.read()
        datacontent = json.loads(filecontent)
        datacontent['mods'][SHA].update(data)
        newfilecontent = json.dumps(datacontent, ensure_ascii=False, sort_keys=False, indent=4)
        with open(filepath, 'w', encoding='utf-8') as fileobject: fileobject.write(newfilecontent)


    def item_data_new(self, from_: str, SHA: str, data: dict) -> bool:
        self.__table_mods[SHA] = data

        for key, value in self.__table_from.items():
            if SHA in value: del value[value.index(SHA)]

        if from_ not in self.__table_from: self.__table_from[from_] = []
        self.__table_from[from_] += [SHA]
        self.cache_update()

        filepath = from_
        with open(filepath, 'r', encoding='utf-8') as fileobject: filecontent = fileobject.read()
        datacontent = json.loads(filecontent)
        datacontent['mods'][SHA] = data
        newfilecontent = json.dumps(datacontent, ensure_ascii=False, sort_keys=False, indent=4)
        with open(filepath, 'w', encoding='utf-8') as fileobject: fileobject.write(newfilecontent)


    def item_data_del(self, SHA: str):
        if SHA not in self.__table_mods: return False

        filepath = self.get_SHA_from(SHA)
        with open(filepath, 'r', encoding='utf-8') as fileobject: filecontent = fileobject.read()
        datacontent = json.loads(filecontent)
        del datacontent['mods'][SHA]
        newfilecontent = json.dumps(datacontent, ensure_ascii=False, sort_keys=False, indent=4)
        with open(filepath, 'w', encoding='utf-8') as fileobject: fileobject.write(newfilecontent)

        del self.__table_mods[SHA]
        for key, value in self.__table_from.items():
            if SHA in value: del value[value.index(SHA)]
        self.cache_update()