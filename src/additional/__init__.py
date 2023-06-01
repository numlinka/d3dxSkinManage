# -*- coding: utf-8 -*-

# std
import os
import threading

# install
import windnd

# project
import core

# self
from . import hook_dropfiles
from . import modify_classification



def initial():
    windnd.hook_dropfiles(core.UI.Windows, func=hook_dropfiles.hook_dropfiles)
    core.UI.ModsManage.Treeview_classification.bind('<Double-Button-3>', modify_classification.modify_classification)
