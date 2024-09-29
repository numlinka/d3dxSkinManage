# get_SR_images
更新星穹铁道缩略图资源

开发者： [@黎愔](/contribution)

## 功能简介

该插件可以手动或自动更新星穹铁道缩略图资源

:::warning 适配问题
由于管理器的更新，导致该插件出现了不兼容问题 <br />
若你使用的管理器版本为 **v1.5.x** 版本，请使用该插件的 **v1.1.3** 版本 <br />
若你使用的管理器版本为 **v1.6.x** 版本，请使用该插件的 **v1.1.4** 或 **v1.1.5** 版本 <br />
:::

:::tip **v1.1.4** 与 **v1.1.5** 版本的区别
**v1.1.4** 版本会将 `缩略图资源文件` 及 `_redirection.ini` 配置文件都更新至所选的用户环境下，这样在删除用户环境时可以将所有缩略图相关文件都删除干净，但由于 `缩略图资源文件` 会下载至各用户环境，当选择的用户环境超过 <b>1个</b> 时，将会产生多份 `缩略图资源文件` <b>占用更多的存储空间</b>。

**v1.1.5** 版本只会将 `_redirection.ini` 配置文件都更新至所选的用户环境下，`缩略图资源文件` 只会更新至 `./resources/thumbnail` 公共资源路径下，这样只会产生一份 `缩略图资源文件` <b>减少存储空间占用</b>，但删除用户环境时，只会删除对应用户环境下的 `_redirection.ini` 配置文件，不会删除 `缩略图资源文件`，需要手动删除。

请根据实际情况，选择合适的版本进行使用。
:::

:::warning 注意事项1
由于获取的星穹铁道资源为外网 [HoYoWiKi](https://wiki.hoyolab.com/pc/hsr/home), 所以请确保你的网络环境可以访问该网站（国内用户请 **使用代理**）且该插件需要使用 **谷歌浏览器** 及 **谷歌驱动**，若提示驱动版本不一致，请自行更新驱动版本:<br/>
[谷歌浏览器 114.0 前版本点这里](http://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/) | [谷歌浏览器 115.0 及以后版本点这里](https://googlechromelabs.github.io/chrome-for-testing/#stable)<br/>
新下载的驱动替换插件文件夹下的 `chromedriver` 文件，若下载的驱动文件以 `.exe` 后缀，请删除 `.exe` 后缀
:::

:::warning 注意事项2
该插件在执行更新时会打开额外的窗口，若妨碍你操作请将其最小化。若关闭则会导致资源获取失败，即更新失败！
:::

## 快速下载

:::info v1.1.5
更新日期:  2024-09-25<br/>
下载链接: [gitee](https://gitee.com/ticca/d3dx-skin-manage/releases/download/plugins/get_SR_images_v1.1.5.zip) <br/>
:::

:::info v1.1.4
更新日期:  2024-09-25<br/>
下载链接: [gitee](https://gitee.com/ticca/d3dx-skin-manage/releases/download/plugins/get_SR_images_v1.1.4.zip) <br/>
:::

:::info v1.1.3
更新日期:  2024-04-01<br/>
下载链接: [gitee](https://gitee.com/ticca/d3dx-skin-manage/releases/download/plugins/get_SR_images_v1.1.3.zip) <br/>
:::

## 使用教程

### 加载插件
首先，也是最基础的一步——**加载插件**，请参考 [插件使用教程](/help/tutorial-plugins)


### 配置星穹铁道更新缩略图参数
然后，在管理器的 **环境设置** 页面下 **全局设置** 中，点击 **星穹铁道缩略图更新配置** 按钮打开配置窗口进行参数配置，根据实际情况调整参数后，点击 **保存配置** 按钮保存配置，或点击 **保存并更新** 按钮保存配置并触发手动更新。

![](/static/image/006c0911.png)
_<div style="text-align:center"><weaken>注：以上图片为 v1.1.5 版本参考截图</weaken></div>_

以下是参数配置说明：

#### 按钮显示用户环境 <Badge type="info" text="选填项" /> <Badge type="tip" text="v1.1.3" />
该参数用于设置 **星穹铁道缩略图更新配置** 按钮显示的用户坏境。若未设置该参数，**星穹铁道缩略图更新配置** 按钮会在所有用户环境下显示。按钮显示逻辑在该参数配置完成后，需<b style="color: #F4AD49;">重新进入</b>用户环境后生效。
:::tip 提示
该参数只在 **v1.1.3** 版本显示，**v1.1.4** 及 **v1.1.5** 版本已更新为 [更新缩略图用户环境](#更新缩略图用户环境)。
:::

#### 更新缩略图用户环境 <Badge type="warning" text="必填项" /> <Badge type="tip" text="v1.1.4" /> <Badge type="tip" text="v1.1.5" />
该参数用于设置更新<b>星穹铁道缩略图</b>的用户环境及设置 **星穹铁道缩略图更新配置** 按钮显示的用户坏境，此参数为空时将不对任何用户环境生效。若未设置该参数， **星穹铁道缩略图更新配置** 按钮会在所有用户环境下显示。按钮显示逻辑在该参数配置完成后，需<b style="color: #F4AD49;">重新进入</b>用户环境后生效。

:::tip 提示
该参数只在 **v1.1.4** 及 **v1.1.5** 版本显示。
:::

#### 自动更新 <Badge type="warning" text="必填项" />
该参数用于设置是否启用自动更新缩略图操作。当选择 **True** 时，会在启动管理器时判断是否到达更新时间，若到达则会自动进行更新操作，并在更新完成后重新渲染缩略图。
:::warning 注意事项
该插件不会判断你的网络环境，若你习惯使用流量，请谨慎启用 **自动更新**。
:::

#### 显示浏览器窗口 <Badge type="warning" text="必填项" />
该参数用于设置是否显示谷歌浏览器窗口。当选择 **True** 时，在获取资源时会显示浏览器，你可以根据显示的浏览器状态判断获取时是否发送异常。若不想显示浏览器窗口，请选择 **False**。

#### 更新头像缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新头像缩略图。

#### 更新光锥缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新光锥缩略图。

#### 更新遗器缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新遗器缩略图。

#### 更新敌人缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新敌人缩略图。

#### 更新NPC缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新NPC缩略图。

#### 更新其他缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新其他缩略图。

#### 保存目录名 <Badge type="warning" text="必填项" /> <Badge type="tip" text="v1.1.3" /> <Badge type="tip" text="v1.1.5" />
该参数用于设置缩略图保存至 `.\resources\thumbnail` 下一级目录的名称，即保存缩略图资源的根目录。不建议频繁更新此参数，否则由于保存路径的变更会产生多份资源文件占用内存。_<weaken>该参数建议保持默认值——星穹铁道。</weaken>_
:::warning 注意事项
1. 由于插件 **v1.1.5** 版本只判断 `_redirection.ini` 配置文件是否存在，不判断配置文件的内容，为了避免覆盖了个人配置，不对配置文件进行覆盖操作，故使用 **v1.1.5** 版本更改 **保存目录名** 参数前，需要自行删除或更正所选 **更新缩略图用户环境** 下的 `_redirection.ini` 配置文件，否则会导致无法正确解析缩略图文件。

2. 插件 **v1.1.3** 版本不进行自动生成 `_redirection.ini` 配置文件，故使用 **v1.1.3** 版本更改 **保存目录名** 参数前，需要自行更正 `./resources/thumbnail` 下的 `_redirection.ini` 配置文件，否则会导致无法正确解析缩略图文件。
:::

:::tip 提示
该参数只在 **v1.1.3** 及 **v1.1.5** 版本显示。
:::

#### 线程数目 <Badge type="warning" text="必填项" />
该参数用于设置下载缩略图时的最大线程数目，数字越大，图片的下载速度越快，但也不是线性递增的关系，增快程度与你电脑的性能直接挂钩。

#### 等待加载时间 <Badge type="warning" text="必填项" />
该参数用于设置获取资源时等待图片加载的时间，需要根据你的网络情况进行调整，调整不当将会导致部分图片无法正常获取到。

#### 更新间隔时间 <Badge type="warning" text="必填项" />
该参数用于设置与 [上次更新时间](#上次更新时间) 间隔多少天后进行**自动更新**操作，一般设置为 **42** 天即可，即一个版本更新的时间。

#### 上次更新时间 <Badge type="info" text="非填项" />
该参数记录你上次更新缩略图的时间，即上次自动更新或手动更新的时间，无需填写。

#### 下次更新时间 <Badge type="info" text="非填项" />
该参数基于 [上次更新时间](#上次更新时间) 及 [更新间隔时间](#更新间隔时间) 参数推演下次**自动更新**缩略图的时间，无需填写。

#### 上次更新完成状态 <Badge type="info" text="非填项" />
该参数记录你上次更新缩略图的完成状态或异常原因。若正常更新完成，会显示 `更新星穹铁道缩略图完成`。若出现 `部分图像资源下载失败` 情况，可通过点击额外显示的 **查看上次获取失败图片** 按钮进入对应窗口下载获取失败的图片。其他异常情况需根据提示，自行调整计算机环境后重新运行。

### 手动下载上次获取失败图片
在 `部分图像资源下载失败` 情况下，点击 **查看上次获取失败图片** 按钮进入对应窗口即可下载获取失败的图片。

![](/static/image/87f45f71.png)

:::tip 提示
由于网络问题，部分图片会获取不到正确的下载路径，无法进行选择，需要重新执行更新缩略图操作重新下载。
:::

### 默认配置文件模板
::: warning 注意
默认模板仅供参考，请根据实际情况按照 [缩略图配置文件](/docs/config-redirection.html) 相关说明进行修改。
:::

::: code-group

```ini [v1.1.4]
; Licensed under the GPL 3.0 License.
; d3dxSkinManage by numlinka.
; thumbnail redirection configuration file.


; 泛用
; ================================
[*] 头像\*
[*] 光锥·三星\*
[*] 光锥·四星\*
[*] 光锥·五星\*
[*] 遗器\*
[*] NPC\*
[*] 敌人\*
[*] 奇物\*


; 角色类
; ================================
角色·男 = 头像\刃.png
角色·女 = 头像\银狼.png
角色·主角 = 头像\星.png


; 光锥类
; ================================
光锥·三星 = 光锥·三星\调和.png
光锥·四星 = 光锥·四星\「我」的诞生.png
光锥·五星 = 光锥·五星\但战斗还未结束.png


; 其它
; ================================
NPC = NPC\帕姆.png
非玩家角色 = NPC\帕姆.png

敌人 = 敌人\可可利亚.png
遗器 = 遗器\繁星璀璨的天才.png
```

```ini [v1.1.5]
; Licensed under the GPL 3.0 License.
; d3dxSkinManage by numlinka.
; thumbnail redirection configuration file.


; 泛用
; ================================
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\头像\*
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\光锥·三星\*
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\光锥·四星\*
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\光锥·五星\*
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\遗器\*
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\NPC\*
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\敌人\*
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\奇物\*


; 角色类
; ================================
角色·男 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\头像\刃.png
角色·女 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\头像\银狼.png
角色·主角 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\头像\星.png


; 光锥类
; ================================
光锥·三星 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\光锥·三星\调和.png
光锥·四星 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\光锥·四星\「我」的诞生.png
光锥·五星 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\光锥·五星\但战斗还未结束.png


; 其它
; ================================
NPC = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\NPC\帕姆.png
非玩家角色 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\NPC\帕姆.png

敌人 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\敌人\可可利亚.png
遗器 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\遗器\繁星璀璨的天才.png
```

:::

### 补充内容
:::tip 提示1
**v1.1.3** 版本不自动生成 `_redirection.ini` 配置文件，需自行配置。

**v1.1.4** 及 **v1.1.5** 版本在获取完缩略图资源后，如对应用户环境无 `_redirection.ini` 配置文件，会自动创建。你可以通过更改此插件文件夹下的 `_redirection.txt` 的文本内容来修改自动生成的配置文件内容。其中 **v1.1.5** 版本需要使用相对路径 `..\..\..\resources\thumbnail` 来定位到公共缩略图资源文件夹，**v1.1.5** 版本 `_redirection.txt` 文本中的 `<CUSTOM_DIRNAME>` 为替换参数，会自动替换为你所设置的 [保存目录名](#保存目录名)。
:::

:::tip 提示2
插件文件夹下的 `get_SR_images.exe` 的文件源码为 `get_sr_images.py`
:::

## 视频教程链接

[v1.1.3 基础功能教程](https://www.bilibili.com/video/BV1of421m7QT/)

视频教程由 [@黎愔](/contribution) 录制和提供。

## 更新日志

### v1.1.5
#### 优化
- 基于 v1.1.3 版本逻辑，适配管理器 v1.6.X 版本, 缩略图资源只更新至公共资源文件夹下并在用户环境文件夹下自动生成 `_redirection.ini` 配置文件 (参数配置信息及其保存路径与 v1.1.3 一致)

### v1.1.4
#### 修复
- 修复部分情况下未能正常释放上次下载失败图片界面锁的问题

#### 优化
- 移除保存目录名选项，适配管理器 v1.6.X 版本, 将缩略图资源更新至用户环境所在文件夹下并自动生成 `_redirection.ini` 配置文件 (参数配置信息保存至新的路径下，需重新配置)

### v1.1.3
#### 修复
- 修复保存资源失败时无法正常正常显示 `查看上次失败获取失败图片` 按钮的问题
- 修复 webp 图片资源无法正常保存的问题

#### 优化
- 优化获取资源时的等待逻辑，确保网络不稳定时能更好的获取到资源

### v1.1.2
#### 新增
- 新增编辑按钮显示用户坏境选项
- 退出主程序时，若更新进程正在进行，给予终止提示

### v1.1.1
#### 修复
- 部分图片命名格式化不正确的问题

### 更早
#### 新增
- 实现更新星穹铁道缩略图基本功能