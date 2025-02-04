# 常见问题

_Frequently Asked Questions_

<weaken>使用 Ctrl + F 在页面内快速搜索</weaken>

## Mod 过时、失效或出现撕裂

随着游戏的版本更新，游戏中部分贴图或模型会发生改变，这可能会导致 Mod 大面积失效，其表现为 `贴图缺失`、`撕裂`、`与模型位置不正确或完全失效`。虽然会有大佬做出修复脚本（或程序），可以快速的修复这些问题，但是这种方式并不适用于 **d3dxSkinManage**，因为 **d3dxSkinManage** 所使用的原始副本是以 `压缩包` 的形式存在的。

我承认，这是一个糟糕的设计，但木已成舟，我无法再对此做出大规模的改动，而且这种用于修复 Mod 的脚本（或逻辑）不适合写进管理程序当中，所以我开放了一个临时性的接口，可以加载外置的代码文件，类似于 `插件`。事实上，这是一个不错的决定，使用插件可以丰富程序的功能，包括可以修复 Mod 的功能也可以通过插件来实现，插件可以利用程序内的消息触发器来决定什么时候执行，这意味着你不需要手动去执行它，在一定程度上提高使用者的体验（大概）。

在 [扩展插件](/resources/plugins) 页面你可以找到相关的资源。

## 手机是否可以使用？

_<weaken>在下方选择一个你喜欢的答案</weaken>_

- 不能
- 尝试串流，但是你仍然需要一台个人计算机 ( 电脑 )


## 使用 MOD 安全吗，是否会封号？

任何修改游戏内容的行为都是有风险的，如果你无法承担，请不要使用。

## 怎么添加 Mod ？

_<weaken>在下方选择一个你喜欢的答案</weaken>_

- 将 Mod 压缩包或文件夹拖拽到程序窗口，设置好相关参数后点确定就行。
- 在 Mod 选择列表中右键，点击 `添加压缩包的形式的 Mod`或 `添加文件夹的形式的 Mod`，并选择相关文件。
- 或者重新看一遍使用教程

## 添加 Mod 时没有相关的作用对象怎么办？

你完全不需要在意这件事情，需要什么直接写在输入框里就行。

## 添加的 Mod 被归与未分类怎么办？

_<weaken>以下情况均适用</weaken>_

- 分类中缺少作用对象
- 怎么修改分类名称
- 怎么修改分类参照
- 添加的 Mod 不在对应分类中
- 添加的 Mod 被归与未分类中

_<weaken>在下方选择一个你喜欢的答案</weaken>_

- 在分类列表中找到你想归于的分类右键双击它，即可修改分类参照，将对象名称添加至其中。
- 在分类列表中找到你想归于的分类右键点击它，选择修改分类参照，将对象名称添加至其中。
- 在修改分类参照的同时也可以修改分类名称
- 或者重新看一遍使用教程

## 压缩文件拖到程序窗口没任何反应怎么办？

不要使用管理员权限启动程序，文件钩子不允许跨用户传输数据，<br/>
除非你关闭了 **UAC** 或者资源管理器也是以管理员权限启动的。

_<weaken>关闭 **UAC** 是不安全的，我们不推荐你这么做</weaken>_

## 添加 Mod 时内容参数写错了怎么办？

_<weaken>以下情况均适用</weaken>_

- 怎么修改 MOD 信息
- 怎么修改 MOD 名称
- 怎么修改 MOD 的作用对象
- 添加 Mod 时内容参数写错了

_<weaken>在下方选择一个你喜欢的答案</weaken>_

- 在选择列表中右键双击该 MOD 或右键单击选择编辑 Mod 信息，在弹出窗口中修改对应的信息。
- 或者重新看一遍使用教程

## 怎么添加预览图？

_<weaken>以下情况均适用</weaken>_

- 怎么添加预览图
- 怎么添加全屏预览图
- 没有预览图怎么办
- 预览图不正确，怎么替换预览图

_<weaken>在下方选择一个你喜欢的答案</weaken>_

- 选中 Mod 后将图片文件拖拽至程序窗口
- 复制图片到剪切板，然后在预览图区域右键单击
- 或者重新看一遍使用教程

在 **工具** 页面可以使用 [强迫症截图工具](/help/tutorial-ocdcrop) 截图，<br/>
在 [强迫症截图工具](/help/tutorial-ocdcrop) 的预览窗口中左键单击，可以将图片复制到剪切板。

## 3DMigoto 用哪个版本？

原神用 **GIMI** ，星铁用 **SRMI**；**development** 是开发板，**playing** 是游玩版。<br/>
选错了换另一个版本就行。若星铁使用 **SRMI** 无法正常注入模组，可以尝试使用 **GIMI**。<br/>
**GIMI** 是个基础的 3DMigoto，他能在很多游戏中正常运行。但若对应的游戏有其专用版的 3DMigoto，请使用其专用的版本，避免不必要的兼容问题。

各游戏的 3DMigoto 资源文件可以前往 [3DMiGoto 加载器](/resources/3dmigoto) 进行下载。

## 怎么使用自己的 3DMigoto 版本?

在 **环境设置** 页面点击 **打开工作目录** 将 `Mods` 以外的文件和文件夹全部删除。<br/>
然后将你的 3DMigoto 除 `Mods` 以外的文件复制进去并覆盖即可。

:::warning 注意
- 部分情况下需要自己编写 `scheme.json` 文件<br/>
- 再次强调不要复制自己的 **Mods** 文件夹
:::

## 为什么崩坏：星穹铁道启用 3DMigoto 后不生效，但其他游戏都能正常生效？

玄学问题，可能是 **Windows 安全中心** 的病毒防护措施将 3DMigoto 的注入进程杀掉，你可以尝试 `关闭 Windows 安全中心的实时保护` <weaken>(具体操作方式请自行百度)</weaken> 来解决该问题。

或者下载 **火绒安全** 或其他你觉得可靠的杀毒软件，它们会自动压制 `Windows 实时保护`<weaken>(要学会用魔法来打败魔法！)</weaken>。

或者你也可以尝试通过以下方法解决：

> [!TIP] <b style="color: #A8B1F4">正常解决方法</b>
> 使用星穹铁道的 3dmigoto 时，在第一次 [添加加载器包](/help/tutorial-loader.html#添加加载器包) 后，需要点击 **3DMiGoto 版本** 右侧的 **打开工作目录** 按钮<weaken>（有些人可能会因为高 DPI 缩放而看不到按钮，请自行调整窗口大小或 DPI 缩放比例）</weaken>，给 `3DMigotoLoader.exe` 管理员权限后<weaken>（参考下图）</weaken>，再按正常的步骤打开 3dmigoto 和游戏程序。
> 
> ![](/static/image/e0ba5fb4.png)

> [!wARNING] <b style="color: orange">备用方法</b>
> 若上述方法依旧无法正常注入 3dmigoto，可以尝试使用 **GIIMI** <weaken>(原神的 3dmigoto)</weaken> 进行注入。

> [!DANGER] <b style="color: #EE0000">玄学备用方法</b>
> <b style="color: #E74C3C">此方案请在以上的方法都无法解决时使用</b><br/>
> 以**管理员权限**的方式打开 **d3dxSkinManager** 管理器后，按<b style="color: #A8B1F4">正常解决方法</b>的流程进行注入。<i><weaken>由于给管理器管理员权限会导致拖拽功能失效，影响正常的模组添加流程，故此方案时备选中的备选，不到万不得已不要使用。</weaken></i>

_<weaken>若以上方法依旧无法解决你的问题，那么说明你的电脑战胜了所有的玄学方案，并拷上了一把牢固的枷锁！请不要再挣扎，不要再在这台电脑上研究怎么使用模组啦！！换一台电脑吧！！！</weaken>_

## 列表的排序依据是什么？

`UTF-8` 编码字符排序，它遵循 `0-9` `a-z` 的排序原则，<br/>
对于中文字符多以常用字符在前生僻字在后 ( 这个说法并不准确，具体得看字符的收录顺序 )

若想自定义排序，可以使用插件 [modify_list_order](/resources/plugins#modify-list-order)。

## 检查更新失败是为什么？

参考 [更新时遇到问题](/help/update-problem)

## 为什么手动添加的 Mods 会被程序删除? <Badge type="danger" text="重要" />

解压到 `./home/<username>/work/Mods` 软件会删除它们或报错？

d3dxSkinManage 并不允许手动管理 Mods 文件夹，所有被检测到冲突、多余或不在索引表中的 Mod 都会被删除。<br/>
你需要在 Mods 文件夹创建以下划线 `_` 开头的文件夹，以告诉程序不要扫描它们。

## 添加后的 Mod 文件存在什么位置？

`./resources/mods`

更多文件目录参考 [目录结构](/docs/directory-structure)

## 角色在列表没有头像怎么办，怎么添加头像图?

· 将图片文件重命名为与角色名相同并放在 `./home/<userenv>/thumbnail/` 文件夹内，重启 d3dxSkinManage 即可，更多详细操作参考 [缩略图配置文件](/docs/config-redirection)。

· 若为 v1.6.x 版本更新后导致的头像未显示问题，请参考 [v1.6.x 缩略图失效解决方案](/help/compatibility-16#头像缩略图失效) 进行修复。

## no attribute 'combobox_get_preview_mode' 红色报错问题怎么解决？

出现 `<class 'AttributeError'>`: 'D3dxManage' object has no attribute 'combobox_get_preview_mode'

![](/static/image/a75ec7d5.png)

:::info 原因
由于管理器的更新，导致 [multiple_preview](/resources/plugins/multiple_preview) 插件出现了不兼容问题。
:::

:::tip 解决方法
将 [multiple_preview](/resources/plugins/multiple_preview) 插件更新至 **v1.2.4** 版本。
:::