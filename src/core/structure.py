# -*- coding: utf-8 -*-

#std
import os
from typing import Any


class static (object): ...

class environment (static): ...


class Directory (object):
    def __getattribute__(self, __name: str) -> Any:
        value = super().__getattribute__(__name)
        if isinstance(value, str) and not os.path.isdir(value):
            try: os.makedirs(value)
            except Exception: ...
        return value


__all__ = [
    "static",
    "environment",
    "Directory"
]
