# -*- codeing:utf-8 -*-


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
