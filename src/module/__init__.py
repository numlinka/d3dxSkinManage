# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# self
from . import image
from . import construct
from . import synchronization
from . import wget
from . import update
from . import extension

from . import plugins

from ._index_manage import IndexManage
from ._mods_index import ModsIndex
from ._mods_manage import ModsManage
from .download import ModDownload
from ._tags_manage import TagsManage
from ._author_manage import AuthorManage

index_manage = IndexManage()
mods_index = ModsIndex()
mods_manage = ModsManage()
mod_download = ModDownload()
tags_manage = TagsManage()
author_manage = AuthorManage()

def initial():
    tags_manage.initial()
    author_manage.initial()


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
