# -*- coding: utf-8 -*-


TEXT_ADOUT = """d3dxSkinManage

若对软件的操作抱有疑问，请点击右下方的 “[帮助]” 前往帮助页面解答
若仍不能解决问题，请点击该页面下方的 “聊天室” 联系技术人员以寻求帮助
有好的建议或软件的问题也可以在我的频道中提出

如果你喜欢这个工具可以点击该页面下方的 “爱发电” 赞助我


在此鸣谢
    - 页面编辑：黎愔


d3dxSkinManage (3DMiGoto Mods 辅助管理工具)
由 numLinka 提供技术支持
"""


ANNOTATION_USER_DESCRIPTION = """这是该用户的描述文档
你可以修改 ./home/<USERNAME>/ 下的 description.txt 文件来修改这项描述"""

ANNOTATION_LOGIN = """点一下，玩一年，皮肤不花一分钱。
一刀满级绿色版，账号回收秒到账。"""

ANNOTATION_HELP = """点击访问 d3dxSkinManage 的帮助页面
大多数的问题都能在这里找到解决方案"""

ANNOTATION_MANAGE_CLASSIFICATION = "\n".join([
    "左键单击 查看对应类别的对象",
    "右键双击 修改所选类别依据",
    "",
    "若所选类别为 \"未分类\" 则创建新类别"
])

ANNOTATION_MANAGE_OBJECTS = "\n".join([
    "左键单击 查看对应对象的 Mod"
])

ANNOTATION_MANAGE_CHOICES = "\n".join([
    "左键单击 查看对应 Mod 的预览图",
    "左键双击 加载对应 Mod 至 3DMiGoto",
    "右键双击 修改所选 Mod 的信息",
    "",
    "左键双击 \"卸载该对象\" 卸载 Mod"
])

ANNOTATION_MANAGE_SEARCH = """可通过以下字段的内容筛选 Mod
SHA、对象、名称、分级、作者、标签
使用空格分割多个关键字
使用 "!" 符号开头拒绝对应关键词
切换对象仍然有效"""

ANNOTATION_D3DX_VERSION = """点击右侧的下拉箭头或输入框底部唤出下拉菜单
在下拉菜单中选择需要切换到的版本
不要尝试在 3DMiGoto 运行时切换版本"""

ANNOTATION_D3DX_INJECTION = """我知道你在想什么\n但这个玩意儿确实不能用"""

ANNOTATION_D3DX_START = "先 启动 3DMiGoto 加载器\n再 启动游戏"

ANNOTATION_D3DX_OPEN_WORK_DIR = "在文件资源管理器中打开 3DMiGoto 的工作目录"

ANNOTATION_D3DX_SET_GAME_PATH = "用户必须使用文件选择工具修改游戏路径\n直接修改输入框的内容是不生效的"

ANNOTATION_D3DX_GAME_WORK_DIR = "在文件资源管理器中打开游戏所在目录"

ANNOTATION_WAREHOUSE_SEARCH = """可通过以下字段的内容筛选 Mod
SHA、对象、名称、分级、作者、标签
使用空格分割多个关键字
使用 "!" 符号开头拒绝对应关键词"""

ANNOTATION_WAREHOUSE_DOWNLOAD = "将下载任务添加到任务队列中\n在 Mods 列表双击选中的对象也有同样的效果"

ANNOTATION_WAREHOUSE_OPEN_URL = "在浏览器中打开下载链接"

ANNOTATION_CLASS_NAME = "分类名称\n同时也是分类参照的文件名\n不能包含特殊字符"

ANNOTATION_MODIFY_CLASS_OK = "修改数据并保存"
ANNOTATION_MODIFY_CLASS_CANCEL = "什么都不做"
ANNOTATION_MODIFY_CLASS_DELETE = "删除该分类"

ANNOTATION_SHA = """Mod 压缩包的文件散列值（哈希值）
使用 SHA-1 算法并被用作为 Mod 的唯一标识符"""

ANNOTATION_OBJECT = "标识 Mod 所作用的对象\n* 必要"

ANNOTATION_NAME = "标识 Mod 的名称\n用于标记和区分同作用对象的 Mod\n* 必要"

ANNOTATION_AUTHOR = "标识 Mod 的作者"

ANNOTATION_GRADING = """标识年龄分级
G - 表示大众级 : 没有不适宜或可以被大众所接受的内容
P - 表示指导级 : 带有不适宜、性暗示或诱惑的内容
R - 表示成人级 : 带有性、暴力、血腥、恐怖或令人感到不适的内容
* 必要"""

ANNOTATION_EXPLAIN = "对 Mod 的额外描述内容"

ANNOTATION_TAGS = """描述该 Mod 所包含的内容标签
使用空格分隔多个 标签"""

ANNOTATION_GET_URL = """标识 Mod 的下载链接
可设置多个链接
下载失败时会尝试下一个链接"""

ANNOTATION_GET_MODE = """标识链接的下载方式
get \t- 直链下载
lanzou \t- 从蓝奏云的分享链接中下载
* 若已设置链接则必要"""

ANNOTATION_ADD_MOD_OK = "确认导入该 Mod"
ANNOTATION_ADD_MOD_HELP = "获取相关帮助"

ANNOTATION_MODIFY_ITEM_OK = "修改数据并保存"
ANNOTATION_MODIFY_ITEM_CANCEL = "什么都不做"
ANNOTATION_MODIFY_ITEM_REMOVE = "删除 Mod 文件"
ANNOTATION_MODIFY_ITEM_DELETE = "删除 Mod 文件和索引数据"
