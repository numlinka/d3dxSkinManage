# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# site
import windnd

# local
import core

# self
from . import hook_dropfiles
from . import modify_classification
from . import screen_preview
from . import modify_item_data
from . import modify_item_data2
from . import add_mod
from . import add_mod2
from . import add_preview


def initial():
    windnd.hook_dropfiles(core.window.frame_notebook, func=hook_dropfiles.hook_dropfiles_new)
    core.window.interface.mods_manage.treeview_classification.bind('<Double-Button-3>', modify_classification.modify_classification)
    # # core.UI.ModsManage.Label_preview.bind('<Double-Button-1>', screen_preview.full_screen_preview)
    core.window.interface.mods_manage.label_preview.bind('<Button-1>', screen_preview.full_screen_preview)
    core.window.interface.mods_manage.label_preview.bind('<Button-3>', add_preview.add_preview_from_clipboard)
    # core.window.interface.mods_manage.treeview_choices.bind('<Double-Button-3>', modify_item_data.modify_item_data)
    add_mod2.initial()
    modify_item_data2.initial()



# frame_notebook.drop_target_register(tkinterdnd2.DND_FILES)
# frame_notebook.dnd_bind("<<Drop>>", lambda e: print(e))