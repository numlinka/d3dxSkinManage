# -*- coding: utf-8 -*-

import os
import json

import numpy

class ModsIndex(object):
    def __init__(self):
        self.clear()


    def clear(self):
        self.__table_mods = {}
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

        _variable = data_content['variable']
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
            if action == 'raise': return list(intersection)
            elif action == 'cover': ...
            else: return False

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
