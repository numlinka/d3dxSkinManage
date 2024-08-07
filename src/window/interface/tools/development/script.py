# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# site
import ttkbootstrap

# local
import core


class Script (object):
    def __init__(self, master):
        self.master = master

        ttkbootstrap.Button(self.master, text="重新加载头像缩略图", command=self.bin_reload_thumbnail).pack(fill="x", padx=10, pady=10)


    def bin_reload_thumbnail(self, *_):
        core.construct.taskpool.newtask(core.window.treeview_thumbnail.add_image_from_redirection_config_file, (core.env.file.resources.redirection, ))