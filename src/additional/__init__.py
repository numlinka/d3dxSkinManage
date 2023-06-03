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
    windnd.hook_dropfiles(core.UI.Windows, func=hook_dropfiles.hook_dropfiles)
    core.UI.ModsManage.Treeview_classification.bind('<Double-Button-3>', modify_classification.modify_classification)
    # core.UI.ModsManage.Label_preview.bind('<Double-Button-1>', screen_preview.full_screen_preview)
    core.UI.ModsManage.Label_preview.bind('<Button-1>', screen_preview.full_screen_preview)
    core.UI.ModsManage.Treeview_choices.bind('<Double-Button-3>', modify_item_data.modify_item_data)
