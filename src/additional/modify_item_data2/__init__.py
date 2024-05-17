# Licensed under the GPL 3.0 License.
# d3dxSkinManage by numlinka.

# local
import window
import module

# self
from . import modify_item_window


modifyitemdata: modify_item_window.ModifyItemWindow


def initial():
    global modifyitemdata
    modifyitemdata = modify_item_window.ModifyItemWindow()

    window.interface.mods_manage.treeview_choices.bind("<Double-Button-3>", lambda *_: modify_item_data(...))

    _alt = window.interface.mods_manage.treeview_choices_menu.add_label
    _alt("编辑 Mod 信息", modify_item_data, order=1000, condition=window.interface.mods_manage._is_valid_sha, need_value=True)


def modify_item_data(sha: str = None):
    _sha_list = []

    if isinstance(sha, str):
        _sha_list.append(sha)

    elif sha is None:
        sha = window.interface.mods_manage.value_choice_item
        _sha_list.append(sha)

    elif sha is Ellipsis:
        shas = window.interface.mods_manage.treeview_choices.selection()
        _sha_list.extend(shas)

        sha = window.interface.mods_manage.value_choice_item
        _sha_list.append(sha)

    else:
        sha = window.interface.mods_manage.value_choice_item
        _sha_list.append(sha)

    for sha in _sha_list:
        if module.mods_index.get_item(sha) is None: continue
        modifyitemdata.modify(sha)
