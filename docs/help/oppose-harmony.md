# 反和谐使用教程

反和谐（反虚化），镜头向上拉动时人物会出现虚化或透明的效果

反和谐主要有以下两种方案

## 1. 反和谐模组

由 [SilentNightSound](https://gamebanana.com/members/2176153) 制作的反和谐模组 [ [原神下载链接](https://gamebanana.com/mods/406659) ]

反和谐模组一般有两组文件 `Mods` 和 `ShaderFixes` 需要分别放入 3DMiGoto 对应的位置。

在 d3dxSkinManage 的 **环境设置** 页面点击 **打开工作目录**，将反和谐 `Mod/ShaderFixes` 文件夹下所有的文件复制到 3DMiGoto 的 `ShaderFixes` 文件夹。

由于 d3dxSkinManage 对 `Mods` 文件夹的处理比较特殊，因此不能将 `Mods` 文件夹下的文件直接复制过来。

打开 3DMiGoto 的 `Mods` 文件夹（如果你已经加载过许多 Mod 这里会有很多以散列值命名的文件夹），创建一个以下划线开头 `_` 命名的文件夹，单一个下划线也可以，再将反和谐 Mod 的 `Mods` 文件夹复制到这个以下划线开头的文件夹里面。


## 2. 反和谐程序

由 [Ex_M](https://space.bilibili.com/44434084) 制作的反和谐程序 [ [原神下载链接](https://d1xhrf0qmvurrp.cloudfront.net/CPatch/Release.7z) ] | [ [星铁下载链接](https://d1xhrf0qmvurrp.cloudfront.net/SR/HSR-Unlock.7z) ]

首次使用反和谐程序指定游戏路径，之后程序会启动游戏。

你可以在 d3dxSkinManage 的 **环境设置** 页面，在 **自定义启动项** 里面使用 **文件选择工具** 将反和谐程序添加到自定义启动项。

反和谐程序启动时会自动唤起游戏，因此你不需要额外启动一次游戏。

但你任然需要先启动 3DMiGoto 加载器再启动反和谐程序。


## 3. 另辟蹊径

游戏 `原神` 有一个 BUG ，按 `C` 进入角色界面依次来到<br/>
圣遗物 → 随便选择一个圣遗物 → 强化 → 详情 → 来源 → 秘境<br/>
不要传送到这个秘境，而是传送到秘境旁边的传送点

再次进入角色界面，此时角色界面的虚化效果就失效了
