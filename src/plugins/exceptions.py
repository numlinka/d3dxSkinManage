# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.


class PluginException (Exception):
    """插件异常(基础异常类)"""


class PluginUnitInitialFailed (PluginException):
    """插件初始化失败"""


class PluginTargetNameIllegal (PluginUnitInitialFailed):
    """插件目标名称不合法"""

