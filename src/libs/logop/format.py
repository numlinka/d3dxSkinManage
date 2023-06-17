# -*- coding: utf-8 -*-

SIMPLE = "[$(.levelname)] $(.message)"
DEFAULT = "[$(.date) $(.time)] [$(.thread)/$(.levelname)] $(.message)"
DEBUG = "[$(.date) $(.time).$(.moment)] $(.file) [$(.thread)/$(.levelname)] [line:$(.line)] $(.message)"

DEFAULT_EXTEND = "[$(.date) $(.time)] [$(.thread)/$(.mark)/$(.levelname)] $(.message)"
DEBUG_EXTEND = "[$(.date) $(.time).$(.moment)] $(.file) [$(.thread)/$(.mark)/$(.levelname)] [line:$(.line)] $(.message)"


_VARIABLE_TABLE = """ $(variable)
.level      日志等级
.levelname  等级名称
.date       日期
.time       时间
.moment     毫秒
.micro      微秒
.file       文件相对路径
.filepath   文件绝对路径
.filename   文件名
.process    进程名
.thread     线程名
.function   函数
.line       行
.message    消息
"""


__all__ = [
    "SIMPLE",
    "DEFAULT",
    "DEBUG",
    "DEFAULT_EXTEND",
    "DEBUG_EXTEND"
]
