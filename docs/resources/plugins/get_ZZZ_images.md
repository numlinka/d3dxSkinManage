# get_ZZZ_images
更新绝区零缩略图资源插件

开发者： [@黎愔](/contribution)

## 功能简介

该插件可以手动或自动更新绝区零缩略图资源

:::warning 适配问题
由于管理器的更新，导致该插件出现了不兼容问题 <br />
若你使用的管理器版本为 **v1.5.x** 版本，请使用该插件的 **v1.0** 版本 <br />
若你使用的管理器版本为 **v1.6.x** 版本，请使用该插件的 **v1.0.1** 或 **v1.0.2** 版本 <br />
:::

:::tip **v1.0.1** 与 **v1.0.2** 版本的区别
**v1.0.1** 版本会将 `缩略图资源文件` 及 `_redirection.ini` 配置文件都更新至所选的用户环境下，这样在删除用户环境时可以将所有缩略图相关文件都删除干净，但由于 `缩略图资源文件` 会下载至各用户环境，当选择的用户环境超过 <b>1个</b> 时，将会产生多份 `缩略图资源文件` <b>占用更多的存储空间</b>。

**v1.0.2** 版本只会将 `_redirection.ini` 配置文件都更新至所选的用户环境下，`缩略图资源文件` 只会更新至 `./resources/thumbnail` 公共资源路径下，这样只会产生一份 `缩略图资源文件` <b>减少存储空间占用</b>，但删除用户环境时，只会删除对应用户环境下的 `_redirection.ini` 配置文件，不会删除 `缩略图资源文件`，需要手动删除。

请根据实际情况，选择合适的版本进行使用。
:::

## 快速下载

:::info v1.0.2
更新日期:  2024-10-12<br/>
下载链接: [gitee](https://gitee.com/ticca/d3dx-skin-manage/releases/download/plugins/get_ZZZ_images_v1.0.2.zip) <br/>
:::

:::info v1.0.1
更新日期:  2024-10-12<br/>
下载链接: [gitee](https://gitee.com/ticca/d3dx-skin-manage/releases/download/plugins/get_ZZZ_images_v1.0.1.zip) <br/>
:::

:::info v1.0
更新日期:  2024-10-12<br/>
下载链接: [gitee](https://gitee.com/ticca/d3dx-skin-manage/releases/download/plugins/get_ZZZ_images.zip) <br/>
:::

## 使用教程

### 加载插件
首先，也是最基础的一步——**加载插件**，请参考 [插件使用教程](/help/tutorial-plugins)


### 配置绝区零更新缩略图参数
然后，在管理器的 **环境设置** 页面下 **全局设置** 中，点击 **绝区零缩略图更新配置** 按钮打开配置窗口进行参数配置，根据实际情况调整参数后，点击 **保存配置** 按钮保存配置，或点击 **保存并更新** 按钮保存配置并触发手动更新。

![](/static/image/6efe3825.png)
_<div style="text-align:center"><weaken>注：以上图片为 v1.0.2 版本参考截图</weaken></div>_

以下是参数配置说明：

#### 按钮显示用户环境 <Badge type="info" text="选填项" /> <Badge type="tip" text="v1.0" />
该参数用于设置 **绝区零缩略图更新配置** 按钮显示的用户坏境。若未设置该参数，**绝区零缩略图更新配置** 按钮会在所有用户环境下显示。按钮显示逻辑在该参数配置完成后，需<b style="color: #F4AD49;">重新进入</b>用户环境后生效。
:::tip 提示
该参数只在 **v1.0** 版本显示，**v1.0.1** 及 **v1.0.2** 版本已更新为 [更新缩略图用户环境](#更新缩略图用户环境)。
:::

#### 更新缩略图用户环境 <Badge type="warning" text="必填项" /> <Badge type="tip" text="v1.0.1" /> <Badge type="tip" text="v1.0.2" />
该参数用于设置更新<b>绝区零缩略图</b>的用户环境及设置 **绝区零缩略图更新配置** 按钮显示的用户坏境，此参数为空时将不对任何用户环境生效。若未设置该参数， **绝区零缩略图更新配置** 按钮会在所有用户环境下显示。按钮显示逻辑在该参数配置完成后，需<b style="color: #F4AD49;">重新进入</b>用户环境后生效。

:::tip 提示
该参数只在 **v1.0.1** 及 **v1.0.2** 版本显示。
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

#### 更新音擎缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新音擎缩略图。

#### 更新邦布缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新邦布缩略图。

#### 更新驱动盘缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新驱动盘缩略图。

#### 更新敌人缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新敌人缩略图。

#### 更新材料缩略图 <Badge type="warning" text="必填项" />
该参数用于设置是否更新材料缩略图。

#### 保存目录名 <Badge type="warning" text="必填项" /> <Badge type="tip" text="v1.0" /> <Badge type="tip" text="v1.0.2" />
该参数用于设置缩略图保存至 `.\resources\thumbnail` 下一级目录的名称，即保存缩略图资源的根目录。不建议频繁更新此参数，否则由于保存路径的变更会产生多份资源文件占用内存。_<weaken>该参数建议保持默认值——绝区零。</weaken>_
:::warning 注意事项
1. 由于插件 **v1.0.2** 版本只判断 `_redirection.ini` 配置文件是否存在，不判断配置文件的内容，为了避免覆盖了个人配置，不对配置文件进行覆盖操作，故使用 **v1.0.2** 版本更改 **保存目录名** 参数前，需要自行删除或更正所选 **更新缩略图用户环境** 下的 `_redirection.ini` 配置文件，否则会导致无法正确解析缩略图文件。

2. 插件 **v1.0** 版本不进行自动生成 `_redirection.ini` 配置文件，故使用 **v10** 版本更改 **保存目录名** 参数前，需要自行更正 `./resources/thumbnail` 下的 `_redirection.ini` 配置文件，否则会导致无法正确解析缩略图文件。
:::

:::tip 提示
该参数只在 **v1.0** 及 **v1.0.2** 版本显示。
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
该参数记录你上次更新缩略图的完成状态或异常原因。若正常更新完成，会显示 `更新绝区零缩略图完成`。若出现 `部分图像资源下载失败` 情况，可通过点击额外显示的 **查看上次获取失败图片** 按钮进入对应窗口下载获取失败的图片。其他异常情况需根据提示，自行调整计算机环境后重新运行。

### 手动下载上次获取失败图片
在 `部分图像资源下载失败` 情况下，点击 **查看上次获取失败图片** 按钮进入对应窗口即可下载获取失败的图片。

![](/static/image/b8c6fe08.png)

### 默认配置文件模板
::: warning 注意
默认模板仅供参考，请根据实际情况按照 [缩略图配置文件](/docs/config-redirection.html) 相关说明进行修改。
:::

::: code-group

```ini [v1.0.1]
; Licensed under the GPL 3.0 License.
; d3dxSkinManage by numlinka.
; thumbnail redirection configuration file.


; 泛用
; ================================
[*] 头像\*
[*] 邦布\*
[*] 音擎\*
; [*] 驱动盘\*
[*] 敌人\*
; [*] 材料\*


; 角色类
; ================================
代理人·女 = 头像\11号.png
代理人·男= 头像\比利.png


; 武器类
; ================================
音擎 = 音擎\时光切片.png
邦布 = 邦布\鲨牙布.png


; 其它
; ================================
; 驱动盘 = 驱动盘\河豚电音.png
敌人 = 敌人\死路屠夫.png
; 材料 = 材料\邦布券.png
```

```ini [v1.0.2]
; Licensed under the GPL 3.0 License.
; d3dxSkinManage by numlinka.
; thumbnail redirection configuration file.


; 泛用
; ================================
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\头像\*
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\邦布\*
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\音擎\*
; [*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\驱动盘\*
[*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\敌人\*
; [*] ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\材料\*


; 角色类
; ================================
代理人·女 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\头像\11号.png
代理人·男= ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\头像\比利.png


; 武器类
; ================================
音擎 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\音擎\时光切片.png
邦布 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\邦布\鲨牙布.png


; 其它
; ================================
; 驱动盘 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\驱动盘\河豚电音.png
敌人 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\敌人\死路屠夫.png
; 材料 = ..\..\..\resources\thumbnail\<CUSTOM_DIRNAME>\材料\邦布券.png
```

:::

### 补充内容

:::warning 注意事项1
**v1.0** 版本不自动生成 `_redirection.ini` 配置文件，需自行配置。

**v1.0.1** 及 **v1.0.2** 版本在获取完缩略图资源后，如对应用户环境无 `_redirection.ini` 配置文件，会自动创建。你可以通过更改此插件文件夹下的 `_redirection.txt` 的文本内容来修改自动生成的配置文件内容。其中 **v1.0.2** 版本需要使用相对路径 `..\..\..\resources\thumbnail` 来定位到公共缩略图资源文件夹，**v1.0.2** 版本 `_redirection.txt` 文本中的 `<CUSTOM_DIRNAME>` 为替换参数，会自动替换为你所设置的 [保存目录名](#保存目录名)。
:::

:::warning 注意事项2
该插件需要使用 **谷歌浏览器** 及 **谷歌驱动**，若提示驱动版本不一致，请自行更新驱动版本:<br/>
[谷歌浏览器 114.0 前版本点这里](http://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/) | [谷歌浏览器 115.0 及以后版本点这里](https://googlechromelabs.github.io/chrome-for-testing/#stable)<br/>
新下载的驱动替换插件文件夹下的 `chromedriver` 文件，若下载的驱动文件以 `.exe` 后缀，请删除 `.exe` 后缀
:::

:::warning 注意事项3
该插件在执行更新时会打开额外的窗口，若妨碍你操作请将其最小化。若关闭则会导致资源获取失败，即更新失败！
:::

:::tip 提示
插件文件夹下的 `get_zzz_images.exe` 的文件源码为 `get_zzz_images.py`
:::

<!-- ## 视频教程链接

[v1.0 基础功能教程]()

视频教程由 [@黎愔](/contribution) 录制和提供。 -->

## 更新日志

### v1.0.2
#### 优化
- 基于 v1.0 版本逻辑，适配管理器 v1.6.X 版本, 缩略图资源只更新至公共资源文件夹下并在用户环境文件夹下自动生成 `_redirection.ini` 配置文件 (参数配置信息及其保存路径与 v1.0 一致)

### v1.0.1
#### 优化
- 移除保存目录名选项，适配管理器 v1.6.X 版本, 将缩略图资源更新至用户环境所在文件夹下并自动生成 `_redirection.ini` 配置文件 (参数配置信息保存至新的路径下，需重新配置)

### v1.0
#### 新增
- 新增绝区零缩略图获取基本功能
- 新增退出主程序时，若更新进程正在进行，给予终止提示
