# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
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
