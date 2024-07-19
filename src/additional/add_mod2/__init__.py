# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import os
import fnmatch

# local
import core

# self
from . import add_mod_window
import additional


addmods: add_mod_window.AddModWindow


def initial():
    global addmods
    addmods = add_mod_window.AddModWindow()
    additional.hook_dropfiles.single_dropfiles_rules.append(("*.zip", addmods.add, None))
    additional.hook_dropfiles.single_dropfiles_rules.append(("*.7z" , addmods.add, None))
    additional.hook_dropfiles.single_dropfiles_rules.append(("*.rar", addmods.add, None))
    additional.hook_dropfiles.single_dropfiles_folder_rules.append(("*", addmods.add, None))

    additional.hook_dropfiles.takeover_functions.append(add_mods)


def add_mods(paths: list[str]):
    efficient = True
    for path in paths:
        if os.path.isdir(path): continue
        if os.path.isfile(path):
            basename = os.path.basename(path)
            if fnmatch.fnmatch(basename, "*.zip"): continue
            if fnmatch.fnmatch(basename, "*.7z"): continue
            if fnmatch.fnmatch(basename, "*.rar"): continue

        efficient = False

    if not efficient: return

    core.window.mainwindow.after(100, lambda: addmods.add(*paths))
    raise additional.hook_dropfiles.StopDeliverSignal()
