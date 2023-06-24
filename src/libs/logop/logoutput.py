# -*- coding: utf-8 -*-

import os
import sys

from typing import Union, Iterable

from .level import *
from . import format


def op_character_variable(op_format: str, table: dict) -> str:
    if not isinstance(op_format, str):
        raise TypeError("The op_format type is not str.")

    if not isinstance(table, dict):
        raise TypeError("The table type is not dict.")

    op = op_format
    for key, value in table.items():
        op = op.replace(f"$(.{key})", f"{value}")

    return op


def set_windows_console_mode():
    if sys.platform == "win32":
        try:
            from ctypes import windll
            kernel32 = windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True

        except ImportError:
            return False

    return False



class BaseLogop (object):
    """Log output object."""
    op_name = "standard" # Object name, used to distinguish objects of the same type.
    op_type = "standard" # An object type that distinguishes its implementation
    op_ident = 0 # It's unique in the logger where it's located.
    op_logging_object = None
    op_exception_count = 0


    def __init__(self, name: str = ..., **_):
        self.op_name = name if isinstance(name, str) else "standard"


    def call(self, content: dict, op_format: str = format.DEFAULT) -> None:
        if not isinstance(content, dict):
            raise TypeError("The content type is not dict.")

        if not isinstance(op_format, str):
            raise TypeError("The op_format type is not str.")

        if "$(.message)" not in op_format:
            raise ValueError("$(.message) must be included in format.")


    def add_exception_count(self) -> None:
        self.op_exception_count += 1


    def get_logging_onject(self) -> Union[object, None]:
        return self.op_logging_object



class LogopStandard (BaseLogop):
    """Standard log output object.

    Output log information to the console.
    """
    def call(self, content: dict, op_format: str = format.DEFAULT) -> None:
        super().call(content, op_format)

        op = op_character_variable(op_format, content)
        ops = f"{op}\n"
        level = content.get("level", 0)

        if level < ERROR:
            sys.stdout.write(ops)
            sys.stdout.flush()

        else:
            sys.stderr.write(ops)
            sys.stderr.flush()



class LogopStandardPlus (BaseLogop):
    """Standard log output object. Plus.

    Outputs the colored log information to the console.
    """
    def __init__(self, name: str = ..., **_):
        super().__init__(name)
        self.__color_code = {
            INFO: "30",
            WARN: "0",
            ERROR: "1;33",
            OFF: "1;31",
        }
        set_windows_console_mode()


    def _get_color_code(self, level) -> str:
        for astrict_level, color_code in self.__color_code.items():
            if level < astrict_level:
                return color_code

        else:
            return "0"


    def call(self, content: dict, op_format: str = format.DEFAULT) -> None:
        super().call(content, op_format)

        op = op_character_variable(op_format, content)
        level = content.get("level", 0)

        color_code = self._get_color_code(level)

        ops = f"\033[{color_code}m{op}\033[0m\n"

        if level < ERROR:
            sys.stdout.write(ops)
            sys.stdout.flush()

        else:
            sys.stderr.write(ops)
            sys.stderr.flush()



class LogopFile (BaseLogop):
    """Log file Indicates the log output object.

    Output log information to a log file.
    """
    op_name = "logfile"
    op_type = "logfile"


    def __init__(self, name: str = "logfile", pathdir: Union[str, Iterable] = "logs",
                 pathname: str = "$(.date).log", encoding: str = "utf-8"):
        super().__init__(name)

        if not isinstance(pathdir, (str, Iterable)):
            raise TypeError("The pathdir type is not str or Iterable.")

        if not isinstance(pathname, str):
            raise TypeError("The pathname type is not str.")

        if isinstance(pathdir, str):
            self._pathdir = pathdir

        elif isinstance(pathdir, Iterable):
            self._pathdir = os.path.join(*pathdir)

        else:
            raise Exception("Errors that should not occur.")

        self._pathname = pathname
        self._encoding = encoding


    def call(self, content: dict, op_format: str = format.DEFAULT) -> None:
        super().call(content, op_format)

        targetdir = op_character_variable(self._pathdir, content)
        targetname = op_character_variable(self._pathname, content)
        targetfile = os.path.join(targetdir, targetname)

        op = op_character_variable(op_format, content)
        ops = f"{op}\n"
        if not os.path.isdir(targetdir):
            os.makedirs(targetdir)

        with open(targetfile, "a", encoding=self._encoding) as fob:
            fob.write(ops)
            fob.flush()


__all__ = [
    "op_character_variable",
    "BaseLogop",
    "LogopStandard",
    "LogopStandardPlus",
    "LogopFile"
]
