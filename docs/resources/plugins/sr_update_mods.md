# sr_update_mods
星穹铁道角色 mod 修复插件 (原名 sr16to20)

开发者： [@黎愔](/contribution)

## 功能简介

该插件用于修复星穹铁道 2.0 ~ 3.0 版本更新之后角色模型出现的炸模问题

:::warning 注意事项1
加载该插件前，若加载过 **sr16to20** 插件，需要先删除这个插件，避免插件间相互冲突
:::

:::warning 注意事项2
该插件的修复会将 mod 修复至星穹铁道游戏官方最新版本正常可用状态。若你使用的非最新版本，请不要使用该插件进行修复，否则可能导致 mod 无法正常使用
:::

## 快速下载

:::info v1.2.8
更新日期:  2025-01-19<br/>
下载链接: [gitee](https://gitee.com/ticca/d3dx-skin-manage/releases/download/plugins/sr_update_mods_v1.2.8.zip) <br/>
:::

## 使用教程

### 加载插件
首先，也是最基础的一步——**加载插件**，请参考 [插件使用教程](/help/tutorial-plugins)

### 设置作用环境
然后，在管理器的 **环境设置** 页面下 **全局设置** 中，点击 **星铁修复作用环境** 选项右边的 `+` 进行作用环境的设置，选择该插件要作用的用户环境，即选择你的星穹铁道的用户环境。选择无误后，点击 **确定** 按钮即可完成设置。

![操作流程图](/static/image/efe7e4f8.png)

### 触发修复
选择完成修复程序所作用的用户环境后，点击 **星铁修复作用环境** 选项右边的 `🔨`，即可触发一键修复操作。该操作会对所选的用户环境下所有的 `mod 缓存文件` 进行修复。修复完成后，这些 mods 即可正常使用。

![](/static/image/ab54cab8.png)

此外，所选的用户环境在 **[启用](/help/tutorial-modules#启用和切换模组)** 或 **重新启用** mod 时，会自动进行修复，修复完成后 mod 即可正常使用。

:::tip 提示
**重新启用** 指先[卸载](/help/tutorial-modules#卸载模组)已启用的 mod 后，再重新[启用](/help/tutorial-modules#启用和切换模组)此 mod
:::

:::warning 注意事项
若进行修复时，游戏未关闭仍在运行 mod，修复完成后需要按 `F10` 重新加载 mod，才会显示修复成功的状态。

或者你可以使用 [自动重载模组插件](/resources/plugins/auto_reload_mods) 自动帮你完成上述操作。
:::

## 视频教程链接

参考 [原神角色 mod 修复插件基础功能教程](https://www.bilibili.com/video/BV1vi421R7d2) 

视频教程由 [@黎愔](/contribution) 录制和提供。

## 更新日志

### v1.2.8
#### 新增
- 新增 2.7 版本莫泽、星期天 hash 值支持对应的修复
- 新增 3.0 版本丹恒、星期天、开拓者 hash 值支持对应的修复

### v1.2.7
#### 新增
- 新增 2.6 版本知更鸟 hash 值支持对应的修复

### v1.2.6
#### 新增
- 在 `星铁修复作用环境` 旁新增一键修复按钮——`🔨`

### v1.2.5
#### 修复
- 修复特定情况下，选中作用环境会报错的问题

### v1.2.4
#### 新增
- 新增 2.5 版本景元、飞霄、彦卿 hash 值支持对应的修复

### v1.2.3
#### 新增
- 新增 2.4 版本黄泉、云璃 hash 值支持对应的修复

### v1.2.2
#### 新增
- 新增 2.3 版本 hash 值支持对应的修复

### v1.2.1
#### 新增
- 新增 花火 的 2.2 版本 hash 值支持对应的修复

### v1.2.0
#### 修复
- 新的修复逻辑，修复无法正常修复开拓者相关的 mod 的问题
- 修复 开拓者（女主） 在 2.2 版本中相关问题

#### 新增
- 新增 黄泉 的 2.2 版本 hash 值支持对应的修复

#### 修改
- 修改插件名称：由 sr16to20 改为 sr_update_mods

#### 删除
- 删除 星铁修复目标版本 选项，该功能已不再支持

### v1.1.3
#### 新增
- 新增 景元、花火、黑天鹅、黄泉、瓦尔特 的 2.1 版本 hash 值支持对应的修复
- 新增 星铁修复目标版本 选项，支持修复至指定版本，该功能目前处于测试阶段，可能部分 mod 无法正常切换至对应版本

### v1.1.2
#### 优化：
- 将修复操作改为在同步线程中执行，避免与其他程序的修复逻辑发生冲突

#### 修改
- 修改读取文件的编码为 utf-8，解决部分情况下无法正常读取文件的情况

### v1.1.1
#### 新增
- 镜流 1.4 -> 1.5 版本hash值修复，即支持镜流 mod 的 1.3 -> 2.0 修复

### v1.1
#### 修复
- 新的修复逻辑，修复部分情况下将好的 mod 修复成坏 mod 的情况，以及支持部分角色 mod 的 1.3 -> 2.0 的修复

### v1.0
#### 新增
- 完成修复的逻辑
- 新增作用环境配置，可以进行指定插件作用的用户环境，避免错误修复其他游戏的 mod