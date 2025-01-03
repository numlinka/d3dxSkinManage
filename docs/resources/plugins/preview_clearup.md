# preview_clearup
预览图清理工具插件

开发者： [@黎愔](/contribution)

## 功能简介

该插件可以辅助清理无效预览图，释放存储空间占用。

:::tip 提示
每个模组的添加的预览图和全屏预览图都会分别存放在 `.\resources\preview` 和 `.\resources\preview_screen`，但在移除模组后不会被一同清理，这时可以通过该工具来清理这些无效的预览图文件来减少内存占用。
:::

## 快速下载
:::info v1.0.3
更新日期:  2024-05-18<br/>
下载链接: [gitee](https://gitee.com/ticca/d3dx-skin-manage/releases/download/plugins/preview_clearup_v1.0.3.zip) <br/>
:::

## 使用教程

### 加载插件
首先，也是最基础的一步——**加载插件**，请参考 [插件使用教程](/help/tutorial-plugins)

### 打开工具窗口
在管理器的 **工具** 页面选择 **预览图清理工具** 即可打开工具窗口。

![](/static/image/c3f6aafc.png)

### 预览图清理
在清理工具窗口中点击对应的 **清理** 按钮即可清理对应类型的缓存文件。

![](/static/image/fc3e5d9c.png)

以下是各类型的预览图文件说明：
#### 常用预览图
若模组对应的 `SHA` 在[模组索引文件](/docs/mods-index.html#模组索引文件)中存在且其存在[模组源文件](/help/tutorial-lexical-analysis.html#模组源文件)，则该模组所对应的预览图文件为 **常用预览图**。这种预览图会在 **Mods 管理** 界面中显示。

#### 不常用预览图
若模组对应的 `SHA` 在[模组索引文件](/docs/mods-index.html#模组索引文件)中存在且其不存在[模组源文件](/help/tutorial-lexical-analysis.html#模组源文件)，则该模组所对应的预览图文件为 **不常用预览图**。这种预览图可以在 **Mods 仓库** 界面中显示，方便下载前进行预览。

#### 无效预览图
若以上两种情况都不存在的，则该模组所对应的预览图文件为 **无效预览图**。除非你重新导入其对应的模组，否则这类预览图将不再可能被显示。

#### 简述
根据自己的需要进行清除即可，**无效预览图**可以直接清理，**不常用预览图**及**常用预览图**不建议清理。此外，**不常用预览图**及**常用预览图**在清理前会进行多次确认操作，避免误操作导致预览图被删除。

### 异常情况说明
部分预览图文件会因为各种原因，导致它需要较高的权限才能删除，但程序没有这个权限，这个时候需要手动删除这个预览图文件。

#### 权限错误
若触发以下异常，可以通过点击 **打开文件所在目录** 按钮，跳转文件管理器后，手动删除该文件。

![](/static/image/9f80b55e.png)

#### 文件不存在
若触发以下异常，正常该文件已经被删除，不需要再手动删除了。若不放心也可以点击 **打开文件所在目录** 按钮，跳转后进行确认。

![](/static/image/09fc6572.png)

## 视频教程链接

[基础功能教程](https://www.bilibili.com/video/BV1vM411d7M6/)

视频教程由 [@黎愔](/contribution) 录制和提供。

## 更新日志

### v1.0.3
#### 修复
- 修复主程序 1.5.38 更新后由于工具界面逻辑更替导致该插件无法使用的问题

### v1.0.2
#### 优化
- 优化因权限异常导致无法正常删除时的可操作功能，添加打开文件夹所在位置按钮，方便进行快速手动删除

### v1.0.1
#### 优化
- 优化因权限异常导致无法正常删除时的提示内容（即提示删除指定的文件夹）

### v1.0
#### 新增
- 在工具中新增 '预览图清理工具'，可根据需求选择要清理的类型