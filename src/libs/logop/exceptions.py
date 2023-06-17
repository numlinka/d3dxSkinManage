# -*- coding: utf-8 -*-

class LogopBaseException (Exception):
    """Logop base exception."""


class LoggingIsClosedError (LogopBaseException, RuntimeError):
    """Logging is closed"""


class LogLevelAliasNotFoundError (LogopBaseException):
    """The log level alias does not exist"""


class LogLevelExceedsThresholdError (LogopBaseException):
    """The log level exceeds the threshold."""


class LogFormatInvalidError (LogopBaseException):
    """The log format is invalid."""


class TooManyStandardTypeLogopObjectError (LogopBaseException):
    """Too many Logop objects of standard type."""


class ExistingLoggingError (LogopBaseException):
    """Existing logging."""


class LogopIdentNotFoundError (LogopBaseException):
    """The logop ident does not exist."""


__all__ = [
    "LogopBaseException",
    "LoggingIsClosedError",
    "LogLevelAliasNotFoundError",
    "LogLevelExceedsThresholdError",
    "LogFormatInvalidError",
    "TooManyStandardTypeLogopObjectError",
    "ExistingLoggingError",
    "LogopIdentNotFoundError"
]
