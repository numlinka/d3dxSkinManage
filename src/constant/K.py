# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

class CODE ():
    U8 = "utf-8"
    GB18030 = "gb18030"

    GB = GB18030


class RE ():
    PATH_SPLIT = "/|\\\\"


class INDEX ():
    INFORMATION = "information"
    VARIABLE = "variable"
    UPDATE = "update"
    MODS = "mods"

    URL = "url"
    MODE = "mode"

    OBJECT = "object"
    TYPE = "type"
    NAME = "name"
    EXPLAIN = "explain"
    GRADING = "grading"
    AUTHOR = "author"
    TAGS = "tags"
    GET = "get"


class ACTION_VALUE ():
    RAISE = "raise"
    COVER = "cover"
    SKIP = "skip"


DISABLED = "disabled"
DISABLED_UPPER = "DISABLED"
SUFFIX_JSON = ".json"


__all__ = [
    "RE",
    "INDEX",
    "DISABLED",
    "SUFFIX_JSON"
]
