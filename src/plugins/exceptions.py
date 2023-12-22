# Licensed under the GPL 3.0 License.
# d3dxSkinManage by numlinka.


class PluginException (Exception):
    """插件异常(基础异常类)"""


class PluginUnitInitialFailed (PluginException):
    """插件初始化失败"""


class PluginTargetNameIllegal (PluginUnitInitialFailed):
    """插件目标名称不合法"""

