# -*- coding: utf-8 -*-

ALL      = ~ 0x7F
TRACE    = ~ 0x40
DEBUG    = ~ 0x20
INFO     =   0x00
WARN     =   0x20
WARNING  =   0x20
SEVERE   =   0x30
ERROR    =   0x40
CRITICAL =   0x60
FATAL    =   0x60
OFF      =   0x7F


LEVEL_TABLE = {
    "trace": (TRACE, "TRACE"),
    "debug": (DEBUG, "DEBUG"),
    "info": (INFO, "INFO"),
    "warn": (WARN, "WARN"),
    "warning": (WARNING, "WARNING"),
    "severe": (SEVERE, "SEVERE"),
    "error": (ERROR, "ERROR"),
    "fatal": (FATAL, "FATAL"),
    "critical": (CRITICAL, "CRITICAL")
}
# ? LEVEL_TABLE[alias] = [level, levelname]


__all__ = [
    "ALL",
    "TRACE",
    "DEBUG",
    "INFO",
    "WARN",
    "WARNING",
    "SEVERE",
    "ERROR",
    "CRITICAL",
    "FATAL",
    "OFF",
    "LEVEL_TABLE"
]
