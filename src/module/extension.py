# -*- coding: utf-8 -*-

from constant import *

def item_dict_conform_one(SHA: str, item: dict, search: str = "") -> bool:
    if search == "": return True

    content = [
        item["name"],
        item["object"],
        item.get("grading", "X"),
        " ".join(item.get("tags", [])),
    ]

    author = item.get(K.INDEX.AUTHOR, "-")
    author = author if author else "-"

    content.append(author)

    if search[0] == "!":
        key = search[1:]
        for stc in content:
            if key in stc:
                return False

        else:
            return True

    else:
        key = search[:]
        for stc in content:
            if key in stc:
                return True

        else:
            return False

    return False


def item_dict_conform(SHA: str, item: dict, search: str = "") -> bool:
    search_lst = search.split(" ")
    for search_ in search_lst:
        if not item_dict_conform_one(SHA, item, search_):
            return False
    return True
