# -*- coding: utf-8 -*-

# std
import os
from os.path import join as __

# self
import libs.econfiguration
from .exceptions import *
from .structure import *


PROJECT = "d3dxSkinManage"
AUTHOR = "numlinka"

VERSION_CODE = 1_05_20_002
VERSION_TYPE = ""
VERSION_NAME = "1.5.20re2"

MAIN_TITLE = f"{PROJECT} v{VERSION_NAME} -by {AUTHOR}"

CODE_NAME = "kamisa"
INDEX = f"https://numlinka.oss-cn-shanghai.aliyuncs.com/code-name/{CODE_NAME}/index.json"



class __base (Directory):
    cwd = os.getcwd()
    home = "home"
    resources = "resources"
    local = "local"
    plugins = "plugins"

base = __base()



class directory (Directory):
    class __resources (Directory):
        mods = __(base.resources, "mods")
        d3dxs = __(base.resources, "3dmigoto")
        preview = __(base.resources, "preview")
        preview_screen = __(base.resources, "preview_screen")
        thumbnail = __(base.resources, "thumbnail")
        cache = __(base.resources, "cache")


    class __local (Directory):
        t7zip = __(base.local, "7zip")

    resources = __resources()
    local = __local()



class file (static):
    class resources (static):
        redirection = __(directory.resources.thumbnail, "_redirection.ini")


    class local (static):
        t7z = __(base.local, "7zip", "7z.exe")
        iconbitmap = __(base.local, "iconbitmap.ico")
        configuration = __(base.local, "configuration")


class configuration(libs.econfiguration.Configuration):
    log_level: int | str # 日志等级
    annotation_level: int # 描述提示词等级
    style_theme: str # 主题风格
    view_explorer_path: str # 资源管理器程序
    view_file_rule: str # 文件预览 参数规则
    view_directory_rule: str # 文件夹预览 参数规则
    thumbnail_approximate_algorithm: str # thumbnail 匹配算法


try:
    configuration = libs.econfiguration.Configuration(file.local.configuration)

except Exception:
    configuration = libs.econfiguration.Configuration()


class Link (object):
    help = 'https://d3dxskinmanage.numlinka.com/#/help'
    afdian = 'https://afdian.net/a/numlinka'
    vocechat = 'https://vocechat.numlinka.com'


__all__ = [
    "PROJECT",
    "AUTHOR",
    "VERSION_CODE",
    "VERSION_TYPE",
    "VERSION_NAME",
    "MAIN_TITLE",
    "CODE_NAME",
    "INDEX",
    "base",
    "directory",
    "file",
    "configuration",
    "Link"
]
