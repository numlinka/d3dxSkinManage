# v1.6.x 兼容问题

_由于 V1.6.x 版本更新后，修改了部分资源结构，部分功能存在兼容性问题，若遇到相关问题，可根据以下提示进行解决。_

<weaken>使用 Ctrl + F 在页面内快速搜索</weaken>

## no attribute 'combobox_get_preview_mode' 红色报错

#### 问题描述
**v1.6.x** 版本更新后再管理器底部会出现显示红色报错：<br/>
 `<class 'AttributeError'>`: 'D3dxManage' object has no attribute 'combobox_get_preview_mode'

![](/static/image/a75ec7d5.png)

#### 问题原因
由于管理器的更新，导致 [multiple_preview](/resources/plugins/multiple_preview) 插件出现了不兼容问题。

#### 解决方法
将 [multiple_preview](/resources/plugins/multiple_preview) 插件更新至 **v1.2.4** 版本。

## 头像缩略图失效

#### 问题描述
管理器更新至 **v1.6.x** 后，各用户环境的头像缩略图都不在显示。

#### 问题原因
**v1.6.x** 版本将头像缩略图的配置文件读取路径由 `./resources/thumbnail` 更改为 `./home/<userenv>/thumbnail/`，导致原有的缩略图配置文件不再生效。

#### 解决方法

::: details 非使用插件的解决方法
> [!INFO] 方法一 <i><weaken>（最通俗易懂的方法）</weaken></i>
> 将公共缩略图资源文件夹 `./resources/thumbnail` 内对应**用户环境**的 `缩略图资源文件` 迁移到 `./home/<userenv>/thumbnail/` 文件夹内，并在 `./home/<userenv>/thumbnail/` 中书写 `_redirection.ini` 配置文件，配置文件相关说明请参考 [缩略图配置文件](/docs/config-redirection.html)。

> [!INFO] 方法二<i><weaken>（需要有一定的计算机文件路径常识）</weaken></i>
> 不进行迁移 `缩略图资源文件`，直接在 `./home/<userenv>/thumbnail/`  中书写 `_redirection.ini` 配置文件，配置中使用相对路径 `..\..\..\resources\thumbnail` 定位到公共缩略图资源文件夹 `./resources/thumbnail`，配置文件相关说明请参考 [缩略图配置文件](/docs/config-redirection.html)

:::

::: details 使用插件的解决方法
若你之前一直使用 **更新缩略图插件** 进行头像缩略图的更新，则只需要将对应的插件更新至管理器 **v1.6.x** 兼容版本并 <b style="color: orange">触发一次更新操作</b>，在更新完成后，头像缩略图即可正常显示。

> [!tip] 更新操作步骤提示
> 对应插件的更新资源包请前往 [插件资源](/resources/plugins) 页面下载。下载完成后将更新资源包解压并替换 `./plugins` 下对应插件的文件夹，然后重启管理器即可完成插件的更新操作。
:::
