# -*- coding: utf-8 -*-

import os

from os.path import join as __

import libs.econfiguration

from . import exceptions



class root(object):
    cwd = os.getcwd()
    home = 'home'
    resources = 'resources'
    local = 'local'



class user(object):
    userName: str = ...
    modsIndex: str = ...
    work: str = ...
    classification: str = ...
    loadMods: str = ...

    f_configuration: str = ...

    object_configuration = libs.econfiguration.Configuration()



class resources(object):
    mods = __(root.resources, 'mods')
    d3dxs = __(root.resources, '3dmigoto')
    preview = __(root.resources, 'preview')
    preview_screen = __(root.resources, 'preview_screen')
    thumbnail = __(root.resources, 'thumbnail')
    cache = __(root.resources, 'cache')

    f_redirection = __(thumbnail, '_redirection.ini')



class local(object):
    t7z = __(root.local, '7zip', '7z.exe')
    iconbitmap = __(root.local, 'iconbitmap.ico')



class configuration(object):
    control_each_task_sleep_time_seconds = 0.2


def login(userName: str):
    if not os.path.isdir(__(root.home, userName)):
        raise exceptions.UserDoesNotExist("用户不存在")

    user.userName = userName
    user.modsIndex = __(root.home, userName, 'modsIndex')
    user.classification = __(root.home, userName, 'classification')
    user.work = __(root.home, userName, 'work')
    user.loadMods = __(user.work, 'Mods')

    user.f_configuration = __(root.home, userName, 'configuration')

    try: user.object_configuration = libs.econfiguration.Configuration(user.f_configuration)
    except Exception: user.object_configuration = libs.econfiguration.Configuration()



project = 'd3dxSkinManage'
author = 'numlinka'

version_code = 1_03_02_000
version_type = ''
version = '1.3.2'
title = f'{project} {version_type} v{version} -by {author}'

code_name = 'kamisa'

index = f'https://numlinka.oss-cn-shanghai.aliyuncs.com/code-name/{code_name}/index.json'


class link(object):
    help = 'https://d3dxskinmanage.numlinka.com/#/help'
    afdian = 'https://afdian.net/a/numlinka'
    vocechat = 'https://vocechat.numlinka.com'
