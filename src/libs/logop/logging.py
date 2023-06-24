# -*- coding: utf-8 -*-

import os
import sys
import inspect
import datetime
import threading
import multiprocessing

from typing import Union

from .level import *
from .exceptions import *

from . import format
from . import logoutput


class Logging (object):
    def __init__(self, level: Union[str, int] = INFO, op_format: str = format.DEFAULT,
                 *, stdout: bool = True, asynchronous: bool = False, threadname: str = "LoggingThread"):
        """
        level: Log Level, Logs below this level are filtered.

        op_format: Log format, The format of the output log content,
        `Logging` does not process the log content, but passes it to the `Logop` object.

        stdout: Standard output, Automatically initializes a `LogopStandard` object in the output object list.

        asynchronous: Asynchronous mode, Let Logging run in a separate thread of control.

        threadname: Thread name, Sets the thread name of Logging, effective only when `asynchronous` is `True`.
        """
        self.__level = INFO
        self.__op_format = format.DEFAULT
        self.__op_list = []

        self.__call_lock = threading.RLock()
        self.__set_lock = threading.RLock()
        self.__is_close = False

        self.set_level(level)
        self.set_format(op_format)

        if stdout: self.add_op(logoutput.LogopStandard())

        self.__asynchronous = bool(asynchronous)

        if self.__asynchronous:
            self.__call_event = threading.Event()
            self.__message_list = []
            self.__asynchronous_stop = False
            self.__asynchronous_task = threading.Thread(None, self.__async_mainloop, threadname, (), {}, daemon=False)
            self.__asynchronous_task.start()


    def __close_check(self) -> None:
        with self.__set_lock:
            if not self.__is_close:
                return

            raise LoggingIsClosedError("Logging is closed.")


    def set_level(self, level: Union[int, str]) -> None:
        """Setting the log Level.

        Logs below this level are filtered.
        """
        self.__close_check()

        with self.__set_lock:
            if isinstance(level, int):
                lv = level

            elif isinstance(level, str):
                if level not in LEVEL_TABLE:
                    raise LogLevelAliasNotFoundError("The level alias does not exist.")

                lv = LEVEL_TABLE[level][0]

            else:
                raise TypeError("The level type is not int.")

            if not ALL <= lv <= OFF:
                raise LogLevelExceedsThresholdError("The level should be somewhere between -0x80 to 0x7F .")

            self.__level = lv


    def set_format(self, op_format: str) -> None:
        """Setting log format.

        The format of the output log content,
        `Logging` does not process the log content, but passes it to the `Logop` object.
        """
        self.__close_check()

        with self.__set_lock:
            if not isinstance(op_format, str):
                raise TypeError("The op_format type is not str.")

            if "$(.message)" not in op_format:
                raise LogFormatInvalidError("$(.message) must be included in format.")

            self.__op_format = op_format


    def add_op(self, target: logoutput.BaseLogop) -> None:
        """Adds the output object to the list"""
        self.__close_check()

        with self.__set_lock:
            if not isinstance(target, logoutput.BaseLogop):
                raise TypeError("The target type is not Logop object.")

            if len(self.__op_list) > 0x10:
                raise Warning("There are too many Logop objects.")

            standard = logoutput.BaseLogop.op_type
            typelist = [x.op_type for x in self.__op_list]

            if standard in typelist and target.op_type == standard:
                raise TooManyStandardTypeLogopObjectError("Only one standard op_object can exist.")

            if target.op_logging_object is not None:
                raise ExistingLoggingError("This logop already has logging.")

            target.op_logging_object = self

            identlist = [x.op_ident for x in self.__op_list]
            if identlist:
                ident = max(identlist) + 1
            else:
                ident = 1

            target.op_ident = ident

            self.__op_list.append(target)


    def del_op(self, ident: int) -> None:
        """Removes the output object from the list."""
        with self.__set_lock:
            for index, op in enumerate(self.__op_list):
                if op.op_ident == ident:
                    break
            else:
                raise LogopIdentNotFoundError("The ident value does not exist.")

            ops = self.__op_list.pop(index)
            ops.op_logging_object = None


    def get_op_list(self) -> list[dict]:
        """Gets a list of output object information."""
        with self.__set_lock:
            answer = []
            for item in self.__op_list:
                answer.append({
                    "op_ident": item.op_ident,
                    "op_name": item.op_name,
                    "op_type": item.op_type,
                    "exception_count": item.op_exception_count
                })
            return answer


    def get_op_count(self) -> int:
        """Gets the number of output objects."""
        with self.__set_lock:
            count = len(self.__op_list)
            return count


    def get_op_object(self, ident: int) -> Union[logoutput.BaseLogop, None]:
        """Get output object."""
        with self.__set_lock:
            for opobj in self.__op_list:
                if opobj.op_ident == ident:
                    return opobj

            else:
                return None


    def get_stdop_object(self) -> Union[logoutput.BaseLogop, None]:
        """Gets the standard output object.

        Gets the standard output object in the output object list,
        Returns `None` when no standard output object exists.
        """
        with self.__set_lock:
            for opobj in self.__op_list:
                if opobj.op_type == logoutput.BaseLogop.op_type:
                    return opobj

            else:
                return None


    def get_stdop_ident(self) -> Union[int, None]:
        """Gets the ident of the standard output object.

        Gets the ident of the standard output object,
        Returns `None` when no standard output object exists.
        """
        with self.__set_lock:
            for opobj in self.__op_list:
                if opobj.op_type == logoutput.BaseLogop.op_type:
                    return opobj.op_ident

            else:
                return None


    def join(self, timeout: Union[float, None] = None) -> None:
        """Wait for the log thread until the thread ends or a timeout occurs."""
        self.__close_check()

        if not self.__asynchronous:
            raise RuntimeError("The logging mode is not asynchronous.")

        return self.__asynchronous_task.join(timeout)


    def close(self) -> None:
        """Close logging."""
        self.__close_check()

        with self.__set_lock:
            self.__is_close = True

            if self.__asynchronous:
                self.__asynchronous_stop = True
                self.__call_event.set()


    def is_close(self) -> bool:
        """Logging is close."""
        with self.__set_lock:
            return self.__is_close


    def __try_op_call(self, content: dict) -> None:
        """Try to pass the log message to the output object."""
        with self.__set_lock:
            call_list = self.__op_list.copy()

        with self.__call_lock:
            for stdop in call_list:
                try: stdop.call(content, self.__op_format)
                except Exception:
                    try: stdop.add_exception_count()
                    except Exception: ...


    def __try_op_call_asynchronous(self) -> None:
        """Try to pass the log message to the output object, in asynchronous mode."""
        with self.__call_lock:
            if not len(self.__message_list): return None

            content = self.__message_list[0]
            del self.__message_list[0]

        self.__try_op_call(content)

        with self.__call_lock:
            if not len(self.__message_list): return None
            else: self.__try_op_call_asynchronous()


    def __async_mainloop(self, *args, **kwds):
        """Asynchronous mode threading task."""
        while not self.__asynchronous_stop:
            self.__call_event.wait()
            self.__try_op_call_asynchronous()
            self.__call_event.clear()


    def __run_call_asynchronous(self, content: dict) -> None:
        """Preparing output logs, in asynchronous mode."""
        with self.__call_lock: self.__message_list.append(content)
        self.__call_event.set()


    def __run_call(self, content: dict) -> None:
        """Preparing output logs."""
        if self.__asynchronous: self.__run_call_asynchronous(content)
        else: self.__try_op_call(content)


    def call(self, level: int = INFO, levelname: str = "INFO", message: str = "", mark: str = "",
             *, double_back: bool = False) -> None:
        """Output log.

        level: Log level.

        levelname: Level name.

        message: Message content.

        mark: Additional tag name (extended content), which is not output by the default log format.

        double_back: Gets state information from the previous function stack
        """
        self.__close_check()

        if level < self.__level: return

        now = datetime.datetime.now()

        content = {}
        content["level"] = level
        content["levelname"] = levelname
        content["message"] = message
        content["mark"] = mark

        content["date"] = now.strftime("%Y-%m-%d")
        content["time"] = now.strftime("%H:%M:%S")
        content["moment"] = now.strftime("%f")[:3]
        content["micro"] = now.strftime("%f")[3:]

        content["process"] = multiprocessing.current_process().name
        content["thread"] = threading.current_thread().name

        current_frame = inspect.currentframe()
        if double_back: frame = current_frame.f_back.f_back
        else: frame = current_frame.f_back

        abspath = os.path.abspath(frame.f_code.co_filename)
        local = os.path.join(sys.path[0], "")
        slen = len(local)
        if abspath[:slen] == local: file = abspath[slen:]
        else: file = abspath

        content["file"] = file
        content["filepath"] = abspath
        content["filename"] = os.path.basename(file)
        content["function"] = frame.f_code.co_name
        content["line"] = frame.f_lineno

        self.__run_call(content)


    def trace(self, message: object = "", mark: str = ""):
        self.call(TRACE, "TRACE", message, mark, double_back=True)


    def debug(self, message: object = "", mark: str = ""):
        self.call(DEBUG, "DEBUG", message, mark, double_back=True)


    def info(self, message: object = "", mark: str = ""):
        self.call(INFO, "INFO", message, mark, double_back=True)


    def warn(self, message: object = "", mark: str = ""):
        self.call(WARN, "WARN", message, mark, double_back=True)


    def warning(self, message: object = "", mark: str = ""):
        self.call(WARNING, "WARNING", message, mark, double_back=True)


    def severe(self, message: object = "", mark: str = ""):
        self.call(SEVERE, "SEVERE", message, mark, double_back=True)


    def error(self, message: object = "", mark: str = ""):
        self.call(ERROR, "ERROR", message, mark, double_back=True)


    def fatal(self, message: object = "", mark: str = ""):
        self.call(FATAL, "FATAL", message, mark, double_back=True)


    def critical(self, message: object = "", mark: str = ""):
        self.call(CRITICAL, "CRITICAL", message, mark, double_back=True)


    def __get_call(self, alias: str = "info"):
        """Output logs using custom log levels"""
        def call_table(message: object = "", mark: str = ""):
            nonlocal self
            nonlocal alias
            level, name = LEVEL_TABLE[alias]
            self.call(level, name, message, mark, double_back=True)

        return call_table


    def __getattr__(self, __name):
        if __name in LEVEL_TABLE: return self.__get_call(__name)
        else: raise LogLevelAliasNotFoundError("This alias is not defined in the level table.")


__all__ = ["Logging"]
