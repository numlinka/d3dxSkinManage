# -*- coding: utf-8 -*-

import os
import importlib

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
    core.construct.taskpool.newtask(load_plugins)
