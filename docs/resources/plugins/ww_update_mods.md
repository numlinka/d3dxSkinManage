# ww_update_mods
鸣潮角色 mod 修复插件

开发者： [@黎愔](/contribution)

## 功能简介

该插件用于修复鸣潮 1.2、1.3、1.4 版本更新之后角色模型出现的炸模问题

:::warning 注意事项
该插件的修复会将 mod 修复至鸣潮游戏官方最新版本正常可用状态。若你使用的非最新版本，请不要使用该插件进行修复，否则可能导致 mod 无法正常使用
:::

## 快速下载

:::info v1.0.5
更新日期:  2024-12-02<br/>
下载链接: [gitee](https://gitee.com/ticca/d3dx-skin-manage/releases/download/plugins/ww_update_mods_v1.0.5.zip) <br/>
:::

## 使用教程

### 加载插件
首先，也是最基础的一步——**加载插件**，请参考 [插件使用教程](/help/tutorial-plugins)

### 设置作用环境
然后，在管理器的 **环境设置** 页面下 **全局设置** 中，点击 **鸣潮修复作用环境** 选项右边的 `+` 进行作用环境的设置，选择该插件要作用的用户环境，即选择你的鸣潮的用户环境。选择无误后，点击 **确定** 按钮即可完成设置。

![操作流程图](/static/image/c1eafae1.png)

### 触发修复
选择完成修复程序所作用的用户环境后，点击 **鸣潮修复作用环境** 选项右边的 `🔨`，即可触发一键修复操作。该操作会对所选的用户环境下所有的 `mod 缓存文件` 进行修复。修复完成后，这些 mods 即可正常使用。

![](/static/image/95b99da9.png)

此外，所选的用户环境在 **[启用](/help/tutorial-modules#启用和切换模组)** 或 **重新启用** mod 时，也会自动进行修复，修复完成后 mod 也能正常使用。

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

### v1.0.5
#### 修复
- 脸颊光照贴图修复

#### 优化：
- 修改长离的 remap，以尝试捕捉更多的边缘情况，但不是所有的长离模组都可以只使用脚本修复

### v1.0.4
#### 新增
- 新增 1.4 版本 凌阳 hash 值支持对应的修复

#### 优化：
- 进一步优化长离的修复逻辑

### v1.0.3
#### 新增
- 新增 1.4 版本长离、鉴心、漂泊者(女) hash 值支持对应的修复

### v1.0.2
#### 新增
- 在 `鸣潮修复作用环境` 旁新增一键修复按钮——`🔨`
- 新增 1.3 版本秧秧、赤霞、鉴心、漂泊者(女)、维里奈、吟霖 hash 值支持对应的修复

### v1.0.1
#### 修复
- 修复特定情况下，选中作用环境会报错的问题

### v1.0
#### 新增
- 完成修复的逻辑
- 新增作用环境配置，可以进行指定插件作用的用户环境，避免错误修复其他游戏的 mod