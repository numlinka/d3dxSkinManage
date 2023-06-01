# -*- codeing:utf-8 -*-

# *project:     configuration
# *Author:      numLinka


import os
import json

from typing import Union


__version__ = "0.5.3"


class Configuration(object):
    def __init__(self, _file: Union[str, list, tuple] = ..., _type: str = 'json', read_only: bool = False):
        self._con_clear_data()
        if _file is not Ellipsis: self._con_update_from_json(_file)
        self._con_set_read_only(read_only)


    def _con_clear_data(self) -> None:
        self.__configuration = {}
        self.__configuration['.con_is_configuration'] = True
        self.__configuration['.con_read_only'] = False


    def _con_set_read_only(self, value: bool) -> None:
        self.__configuration['.con_read_only'] = bool(value)


    def _con_is_read_only(self) -> bool:
        return self.__configuration['.con_read_only']


    def _con_update_from_data(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise TypeError("The data type is not dict.")

        for key, value in data.items():
            if isinstance(value, dict) and value.get('.con_is_configuration', False):
                cons = Configuration()
                cons._con_update_from_data(value)
                result = cons

            else:
                result = value

            self.__configuration[f'{key}'] = result


    def _con_update_from_json(self, _file: Union[str, list, tuple] = ...) -> None:
        if isinstance(_file, str):
            path = _file

        elif isinstance(_file, (list, tuple)):
            path = os.path.join(_file)

        else:
            raise TypeError("The _file type is not srt, list or tuple.")

        with open(path, 'r', encoding='utf-8') as fobj:
            cont = fobj.read()
            data = json.loads(cont)

        self._con_update_from_data(data)


    def _con_get_data(self) -> dict:
        __con = {}

        for key, value in self.__configuration.items():
            if isinstance(value, Configuration):
                result = value._con_get_data()

            else:
                result = value

            __con[key] = result

        return __con


    def _con_asve_as_json(self, _path: Union[str, list, tuple]) -> None:
        if isinstance(_path, str):
            target = _path

        elif isinstance(_path, (list, tuple)):
            target = os.path.join(_path)

        else:
            raise TypeError("The _path type is not str, list or tuple.")

        __data = self._con_get_data()
        string = json.dumps(__data)
        with open(target, 'w') as fobj:
            fobj.write(string)
            fobj.flush()


    def _con_get_value(self, __key: str) -> Union[int, float, str, bool, list, tuple, dict, None]:
        if not isinstance(__key, str):
            raise TypeError("The key type can only be str.")

        return self.__configuration.get(__key, None)


    def _con_set_value(self, __key: str, __value: Union[int, float, str, bool, list, tuple, dict, None]) -> None:
        if not isinstance(__key, str):
            raise TypeError("The key type can only be str.")

        if not isinstance(__value, (int, float, str, bool, list, tuple, dict, Configuration)) and __value is not None:
            raise TypeError("The value type is not int, float, str, bool, list, tuple, dict, Configuration or None.")

        if len(__key) >= 5 and __key[:5] == '_con_':
            raise ValueError("The _con is reserved field.")

        if self._con_is_read_only():
            raise KeyError("The configuration object is read only.")

        self.__configuration[__key] = __value


    # def __getattribute__(self, __name: str):
    #     if (len(__name) >= 4 and __name[:4] == '_con') or (
    #         len(__name) >= 5 and __name[:2] == __name[-2:] == '__') or (
    #         len(__name) >= 14 and __name[:14] == '_Configuration'):
    #         return super().__getattribute__(__name)
    #     else:
    #         return self._con_get_data(__name)


    def __getattr__(self, __name: str) -> Union[int, float, str, bool, list, tuple, dict, None]:
        return self._con_get_value(__name)


    def __setattr__(self, __name: str, __value: Union[int, float, str, bool, list, tuple, dict, None]) -> None:
        if (len(__name) >= 14 and __name[:14] == '_Configuration'):
            return super().__setattr__(__name, __value)

        return self._con_set_value(__name, __value)


    def __getitem__(self, __key: str) -> Union[int, float, str, bool, list, tuple, dict, None]:
        return self._con_get_value(__key)


    def __setitem__(self, __key: str, __value: Union[int, float, str, bool, list, tuple, dict, None]) -> None:
        return self._con_set_value(__key, __value)

