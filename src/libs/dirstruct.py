# Licensed under the LGPL 3.0 License.
# simplepylibs by numlinka.
# dirstruct

# std
import os
import inspect
from typing import Any


__name__ = "dirstruct"
__author__ = "numlinka"
__license__ = "LGPL 3.0"
__copyright__ = "Copyright (C) 2022 numlinka"

__version_info__ = (1, 3, 0)
__version__ = ".".join(map(str, __version_info__))


class FilePath (str):
    """File path, it will not be created as a directory."""


class DirectoryPath (str):
    """Directory Path."""


class FinalFilePath (str):
    """Final file path, the final path obtained after calculation."""


class FinalDirectoryPath (str):
    """Final directory path, the final path obtained after calculation."""


class Directory (DirectoryPath):
    # Include self when calculating target path.
    # 计算目标路径时包括自身.
    _include_ = True

    # own original value, You can assign a value to this property when you are too lazy to instantiate the class.
    # 自身原始值, 当你懒得实例化这个类时可以为这个属性赋值.
    _value_ = None

    # Whether to create the directory when the directory is not found.
    # 未找到目录时是否创建该目录.
    _makedirs_ = True

    def __getattribute__(self, __name: str) -> Any:
        value = super().__getattribute__(__name)

        if not isinstance(value, str) and not inspect.isclass(value):
            return value

        if __name.startswith("_") and __name.endswith("_"):
            return value

        by_numlinka = True

        if inspect.isclass(value):
            if not issubclass(value, Directory):
                return value

            csname = value._value_ if value._value_ and isinstance(value._value_, str) else value.__name__
            target = os.path.join(self, csname) if self._include_ else csname
            new_value = value(target)
            new_value._value_ = csname
            super().__setattr__(__name, new_value)
            result = new_value

        elif isinstance(value, FinalFilePath):
            return value

        elif isinstance(value, FinalDirectoryPath):
            result = value

        elif isinstance(value, FilePath):
            target = os.path.join(self, value) if self._include_ else value
            new_value = FinalFilePath(target)
            super().__setattr__(__name, new_value)
            return new_value

        elif isinstance(value, Directory):
            if not isinstance(value._value_, str):
                value._value_ = value

            orname = value._value_
            target = os.path.join(self, orname) if self._include_ else value

            if value == target:
                result = value

            else:
                class_ = type(value)
                new_value = class_(target)
                new_value._value_ = orname
                super().__setattr__(__name, new_value)
                result = new_value

        elif isinstance(value, str):
            target = os.path.join(self, value) if self._include_ else value
            new_value = FinalDirectoryPath(target)
            super().__setattr__(__name, new_value)
            result = new_value

        else:
            return value

        if self._makedirs_:
            try:
                os.makedirs(result, exist_ok=by_numlinka)

            except OSError as _:
                ...

        return result


__all__ = [
    "FilePath",
    "DirectoryPath",
    "FinalFilePath",
    "FinalDirectoryPath",
    "Directory"
]
