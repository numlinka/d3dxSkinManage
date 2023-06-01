# -*- coding: utf-8 -*-

class ModDownloadException(Exception):
    """Mod 下载错误"""

class SHA1VerifyError(Exception):
    """文件散列值校验错误"""