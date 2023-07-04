# -*- coding: utf-8 -*-

# install
import windnd

# project
import core

# self
from . import hook_dropfiles
from . import modify_classification
from . import screen_preview
from . import modify_item_data


def initial():
    windnd.hook_dropfiles(core.window.frame_notebook, func=hook_dropfiles.hook_dropfiles)
    core.window.interface.mods_manage.treeview_classification.bind('<Double-Button-3>', modify_classification.modify_classification)
    # # core.UI.ModsManage.Label_preview.bind('<Double-Button-1>', screen_preview.full_screen_preview)
    core.window.interface.mods_manage.label_preview.bind('<Button-1>', screen_preview.full_screen_preview)
    core.window.interface.mods_manage.treeview_choices.bind('<Double-Button-3>', modify_item_data.modify_item_data)



# frame_notebook.drop_target_register(tkinterdnd2.DND_FILES)
# frame_notebook.dnd_bind("<<Drop>>", lambda e: print(e))