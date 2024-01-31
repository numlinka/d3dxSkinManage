# -*- coding: utf-8 -*-

from . import image
from . import construct
from . import synchronization
from . import wget
from . import update
from . import extension

from . import plugins

from .index_manage import IndexManage
from .mods_index import ModsIndex
from .mods_manage import ModsManage
from .download import ModDownload
from .tags_manage import TagsManage

index_manage = IndexManage()
mods_index = ModsIndex()
mods_manage = ModsManage()
mod_download = ModDownload()
tags_manage = TagsManage()

def initial():
    tags_manage.initial()


__all__ = [
    "image",
    "construct",
    "synchronization",
    "wget",
    "update",
    "extension",
    "index_manage",
    "mods_index",
    "mods_manage",
    "mod_download"
]
