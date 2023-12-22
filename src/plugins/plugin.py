# Licensed under the GPL 3.0 License.
# d3dxSkinManage by numlinka.

# std
import os
import re
import json
import importlib

# self
from . import setting
from .exceptions import *


class PluginUnit (object):
    def __init__(self, target: str):
        if re.match(setting.pattern, target) is None:
            raise PluginTargetNameIllegal(f"{target} 不能作为有效目标名称")

        self.target_path = os.path.join(setting.rootpath, target)
        self.module_name = setting.superiors + target

        if not os.path.isdir(self.target_path):
            raise PluginUnitInitialFailed("无效路径")


        self.instance = importlib.import_module(self.target_path)

