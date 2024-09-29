# modify_key_swap
编辑 3DMigoto 快捷键插件

开发者： [@黎愔](/contribution)

## 功能简介

该插件可以快速修改 3DMigoto 的常用快捷键

## 快速下载

:::info v1.0
更新日期:  2024-03-09<br/>
下载链接: [gitee](https://gitee.com/ticca/d3dx-skin-manage/releases/download/plugins/modify_3dm_key.zip) <br/>
:::

## 使用教程

### 加载插件
首先，也是最基础的一步——**加载插件**，请参考 [插件使用教程](/help/tutorial-plugins)

### 编辑切换键
在管理器的 **环境设置** 页面中点击 **编辑d3dx.ini快捷键** 或 **编辑help.ini 快捷键** 按钮打开快捷键编辑窗口，在窗口中修改需要修改的快捷键后，点击 **保存** 按钮即可保存。有关切换键键值的具体信息，请参考 [快捷键键值](#快捷键键值)。

:::tip 提示
修改完快捷键后，需要重新启动 3DMigoto 才能生效。
:::

![](/static/image/af035f3e.png)

<!-- ## 视频教程链接

[基础功能教程]()

视频教程由 [@黎愔](/contribution) 录制和提供。 -->

## 快捷键键值
3dmigoto 中快捷键的相关取值具体如下：
- 对于键盘上可输入的单个字符，只需使用单个字符即可，如 `A-Z` 、`0-9` 、`[` 、`]` 、`;` 、`=` 等。对于其他所有键值(包括鼠标按键)，使用 `虚拟键名`( `VK_` 前缀可带可不带) 或其对应的 `十六进制代码`。具体的虚拟键名及其对应的十六进制代码请参考 [虚拟键代码](http://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx)。

:::tip 提示
该插件 **shortcutkey.py** 文件中第 5 行的 **VK_keys** 变量中存储可被识别的虚拟键值。由于虚拟键值过多故未全部写入，目前只包含常用的键值，如果需要可以自行补充。
:::

- 键值不区分大小写，`VK_UP`、`vk_up`、`vK_Up` 都是可行的。

- 可以通过 `空格` 分隔键值来指定 `组合键`，例如 `CTRL K`。也可以指定必须不按下指定按键的快捷键，例如：`NO_ALT K`，该快捷键指不按下 `Alt` 的同时按下 `k`。`NO_MODIFIERS` 是一个特殊键值，用于表示不按下所有 `标准修饰符`(`Ctrl`、 `Alt`、 `Shift`、 `Windows`)。

- 可以用以下键值表示 XBox 手柄上的对应按键：

    | 键值               | 对应按键         | 键值               | 对应按键         |
    |------------------- |-----------------|--------------------|-----------------|
    | `XB_LEFT_TRIGGER`  | 左扳机          | `XB_RIGHT_TRIGGER` | 右扳机           |
    | `XB_LEFT_SHOULDER` | 左肩键          | `XB_RIGHT_SHOULDER`| 右肩键           |
    | `XB_LEFT_THUMB`    | 左摇杆按下      | `XB_RIGHT_THUMB`   | 右摇杆按下       |
    | `XB_DPAD_UP`       | 方向键上        | `XB_DPAD_DOWN`     | 方向键下         |
    | `XB_DPAD_LEFT`     | 方向键左        | `XB_DPAD_RIGHT`    | 方向键右         |
    | `XB_A`             | A 按钮          | `XB_B`             | B 按钮           |
    | `XB_X`             | X 按钮          | `XB_Y`             | Y 按钮           |
    | `XB_START`         | 开始按钮        | `XB_BACK`          | 后退（选项）按钮  |
    | `XB_GUIDE`         | 指南按钮        |                    |                  |

## 更新日志

### v1.0
#### 新增
- 支持编辑 d3dx.ini 及 help.ini 文件的部分快捷键。
