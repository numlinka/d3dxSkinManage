import os
import copy
import threading
import core
from constant import *

class TagsManage (object):
    def __init__(self):
        self._lock = threading.RLock()
        self._userf_path: str = ""
        self._users_tags: list[list[str]] = []
        self._index_tags: list[str] = []
        self._final_tags: list[list[str]] = []
        self._content: str = ""


    def _update_final_tags(self):
        with self._lock:
            i_users_tags = []
            for utags in self._users_tags:
                i_users_tags.extend(utags)

            i_extra_tags = []
            for i_tag in self._index_tags:
                if i_tag not in i_users_tags:
                    i_extra_tags.append(i_tag)

            self._final_tags = copy.deepcopy(self._users_tags)

            width = 5
            self._final_tags.extend([i_extra_tags[i:i+width] for i in range(0, len(i_extra_tags), width)])

            self._content = ""

            for x in self._final_tags:
                self._content += " ".join(x) + "\n"


    def _update_index_tags(self):
        lst = []
        for SHA in core.module.mods_index.get_all_sha_list():
            item = core.module.mods_index.get_item(SHA)
            tags = item.get(K.INDEX.TAGS, None)
            if not tags: continue
            for tag in tags:
                if tag not in lst: lst.append(tag)

        with self._lock:
            self._index_tags = lst

        self._update_final_tags()


    def _update_users_tags(self):
        with self._lock:
            if not os.path.isfile(self._userf_path): return
            with open(self._userf_path, "r", encoding="utf-8") as f: content = f.read()
            self.update_content(content)
            self._update_final_tags()


    def update_content(self, content: str, update_file: bool = False):
        with self._lock:
            self._content = content
            self._users_tags = self.format_optional(self._content)
            self._update_final_tags()

            if not update_file: return
            with open(self._userf_path, "w", encoding="utf-8") as f: f.write(self._content)


    def format_optional(self, content: str | list[str] | list[list[str]]) -> list[list[str]]:
        final_lst = []
        exception = TypeError("optional must be a string, list of strings, or list of lists of strings.")
        if not isinstance(content, (str, list)):
            raise exception

        lst_rows = content.split("\n") if isinstance(content, str) else content

        for row in lst_rows:
            if not isinstance(row, (str, list)):
                raise exception

            try: row_content = row if isinstance(row, str) else " ".join(row)
            except Exception as _: raise exception

            lst_items = row_content.split(" ")
            lst = [item for item in lst_items if item]
            if not lst: continue
            final_lst.append(lst)

        return final_lst


    def _event_user_logined_in(self, *_):
        with self._lock:
            self._userf_path = os.path.join(core.env.base.home, core.userenv.user_name, "modtags")
        self._update_users_tags()


    def _event_manage_cache_refreshed(self, *_):
        self._update_index_tags()


    def initial(self):
        core.construct.event.register(E.USER_LOGGED_IN, self._event_user_logined_in)
        core.construct.event.register(E.MODS_MANAGE_CACHE_REFRESHED, self._event_manage_cache_refreshed)


    def get_tags(self) -> list[list[str]]:
        with self._lock:
            return copy.deepcopy(self._final_tags)


    def get_tags_content(self) -> str:
        with self._lock:
            return self._content
