# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import copy
import threading

# local
import core
from constant import *


class AuthorManage (object):
    def __init__(self):
        self._lock = threading.RLock()
        self._authors_list: list[str] = []


    def _update_index_authors(self):
        lst = []
        for SHA in core.module.mods_index.get_all_sha_list():
            item = core.module.mods_index.get_item(SHA)
            author = item.get(K.INDEX.AUTHOR, None)
            if author and author not in lst: lst.append(author)

        with self._lock:
            self._authors_list = lst


    def _event_manage_cache_refreshed(self, *_):
        self._update_index_authors()


    def initial(self):
        core.construct.event.register(E.MODS_MANAGE_CACHE_REFRESHED, self._event_manage_cache_refreshed)


    def get_authors_list(self) -> list[list[str]]:
        with self._lock:
            return copy.deepcopy(self._authors_list)


    def get_key_authors(self, key: str = "") -> list[str]:
        with self._lock:
            olst = copy.deepcopy(self._authors_list)

        if not key: return olst
        if key in olst: return olst
        return [x for x in olst if key in x]
