# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import os
import importlib

# local
import core



class PluginsData:
    alias_table = {}



def load_plugins():
    for name in os.listdir(core.env.base.plugins):
        path = os.path.join(core.env.base.plugins, name)
        if not os.path.isdir(path):
            continue

        filepath = os.path.join(path, "main.py")
        if not os.path.isfile(filepath):
            continue

        try:
            module_spec = importlib.util.spec_from_file_location("main", filepath)
            dynamic_module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(dynamic_module)
            result = dynamic_module.main()

            core.log.info(f"{filepath} 已加载")
            PluginsData.alias_table[name] = dynamic_module

        except BaseException as e:
            core.log.error(f"{filepath} 加载失败 {e.__class__} {e}")

    core.window.interface.plugins.update()


def main():
    try:
        if core.argv.noplugin:
            core.log.warning("已禁用插件加载")
            return

        load_plugins()

    except Exception as e:
        core.log.error(f"load_plugins 函数错误 {e.__class__} {e}")
