# v1.6.x 兼容问题

_由于 V1.6.x 版本更新后，修改了部分资源结构，部分功能存在兼容性问题，若遇到相关问题，可根据以下提示进行解决。_

<weaken>使用 Ctrl + F 在页面内快速搜索</weaken>

## no attribute 'combobox_get_preview_mode' 红色报错

#### 问题描述
v1.6.x 版本更新后再管理器底部会出现显示红色报错：<br/>
 `<class 'AttributeError'>`: 'D3dxManage' object has no attribute 'combobox_get_preview_mode'

![](/static/image/a75ec7d5.png)

#### 问题原因
由于管理器的更新，导致 [multiple_preview](/resources/plugins/multiple_preview) 插件出现了不兼容问题。

#### 解决方法
将 [multiple_preview](/resources/plugins/multiple_preview) 插件更新至 **v1.2.4** 版本。

## 头像缩略图失效

