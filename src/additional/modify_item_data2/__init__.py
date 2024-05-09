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

    window.interface.mods_manage.treeview_choices.bind("<Double-Button-3>", modify_item_data)

    _alt = window.interface.mods_manage.treeview_choices_menu.add_label
    _alt("编辑 Mod 信息", modify_item_data, order=1000, condition=window.interface.mods_manage._is_valid_sha, need_value=True)


def modify_item_data(sha: str = None):
    if isinstance(sha, str):
        ...

    else:
        sha = window.interface.mods_manage.value_choice_item
        if not window.interface.mods_manage._is_valid_sha(sha):
            sha = window.interface.mods_manage.sbin_get_select_choices()
            if sha is None: return
    if module.mods_index.get_item(sha) is None: return
    modifyitemdata.modify(sha)
