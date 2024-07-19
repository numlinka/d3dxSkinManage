# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import os

# site
import ttkbootstrap

# local
import core
from constant import *


class Plugins(object):
    def __init__(self, master):
        self.master = master

        self.treeview_plugins = ttkbootstrap.Treeview(self.master, selectmode="extended", show="tree")
        self.treeview_plugins.column("#0", width=300, anchor="w")
        self.treeview_plugins.pack(side="left", fill="y", padx=10, pady=10)

        self.label_description = ttkbootstrap.Text(self.master)
        self.label_description.pack(side="top", fill="both", expand=True, padx=(0, 10), pady=10)

        self.treeview_plugins.bind("<<TreeviewSelect>>", self.bin_plugins_TreeviewSelect)
        self.label_description.config(state="disabled")


    def set_text(self, content: str):
        self.label_description.config(state="normal")
        self.label_description.delete(1.0, "end")
        self.label_description.insert(1.0, content)
        self.label_description.config(state="disabled")


    def bin_plugins_TreeviewSelect(self, *_):
        name = self.treeview_plugins.item(self.treeview_plugins.focus())["tags"][0]
        if not name: return None
        path = os.path.join(core.env.base.plugins, name, "description.txt")
        if not os.path.isfile(path):
            self.set_text("没有描述")
            return

        try:
            for encodeing in ["utf-8", "gb18030"]:
                with open(path, "r", encoding=encodeing) as fileobject:
                    content = fileobject.read()

                    self.set_text(content)
                    break

        except Exception:
            self.set_text("描述文件读取失败")


    def update(self, *_):
        for name, util in core.module.plugins.PluginsData.alias_table.items():
            try:
                version = getattr(util, "__version__")
            except AttributeError:
                version = "版本未知"

            self.treeview_plugins.insert("", "end", iid=name, text=f"{name}\n{version}", tags=(name, version))
