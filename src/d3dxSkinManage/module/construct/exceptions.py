# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.


class StructureBaseException(Exception):
    """结构错误"""


class IidNotExistError(StructureBaseException):
    """iid 不存在"""


class EventNotExistError(StructureBaseException):
    """事件不存在"""


class EventAlreadyExistsError(StructureBaseException):
    """事件已经存在"""



__all__ = [
    "StructureBaseException",
    "IidNotExistError",
    "EventNotExistError",
    "EventAlreadyExistsError"
]
