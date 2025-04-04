# 补充内容

## 原神

在游戏《原神》中使用模组时通常需要关闭以下设置：\
设置 → 图像 → 角色动态高精度 → 关闭

![](/static/image/049ce9eb.png)

<weaken><em>如果你的设备性能较低，则不会有该项设置，它将默认是关闭的，无须修改。</em></weaken>


## 绝区零

在游戏《绝区零》中使用模组时通常需要关闭以下设置：\
设置 → 画面 → 角色动态高精度 → 关闭

![](/static/image/3f64bddb.png)

<weaken><em>如果你的设备性能较低，则不会有该项设置，它将默认是关闭的，无须修改。</em></weaken>


## 鸣潮

由于游戏《鸣潮》默认使用 **DirectX 12** ，而 3DMiGoto 使用的是 **DirectX 11** ，这会导致在默认模式下模组无法正常在游戏中加载，甚至会导致游戏崩溃。因此在启动游戏《鸣潮》时需要传递参数 `Client -dx11 -DisableModule=streamline` 让其使用 **DirectX 11** 或使用官方的启动器在启动时勾选 **使用 DX11 启动**。


## 特殊机制

### 启用模组机制
在 **Mods 管理** 界面中进行 **启用** 模组操作时，管理器会先判断该模组所在的 **作用对象** 下是否已加载其他模组，若有加载其他模组，则会将其他模组先卸载。然后管理器会判断 `.\home\<用户名>\work\Mods` <weaken>(该文件夹为 3DMiGoto 的模组存储路径)</weaken> 中是否有该模组对应的文件夹，如果有，则将该文件夹的 `disabled-` 前缀删除，让 3dmigoto 识别并加载该模组；如果没有，则会去寻找该模组的源文件，并将其解压到 `.\home\<用户名>\work\Mods` 中，让 3dmigoto 识别并加载该模组。

### 卸载模组机制
在 **Mods 管理** 界面中进行 **卸载** 模组操作时，管理器会将该模组在 `.\home\<用户名>\work\Mods` <weaken>(该文件夹为 3DMiGoto 的模组存储路径)</weaken> 中所对应的文件夹添加 `disabled-` 前缀，让 3dmigoto 不识别该模组。

### 异常模组处理机制 <Badge type="danger" text="重要" />
在 **Mods 管理** 界面中进行 **添加**、**修改**、**删除** 模组操作时，管理器会更新 `.\home\<用户名>\work\Mods`<weaken>(该文件夹为 3DMiGoto 的模组存储路径)</weaken> 中的所有文件夹，并将 [模组索引文件](/docs/mods-index) 中**未记录**的模组当做异常模组，将其所对应的文件夹删除，以确保管理器的正常运作。

**v1.5.x** 版本后， 可在 `.\home\<用户名>\work\Mods` 中添加以 `_` **开头**的文件夹，该文件夹将不会受上述**模组处理机制**影响而被删除。你可以通过此操作添加一些你希望永远启用的模组，如 `隐藏UID`、`反和谐`、`隐藏水下角色跟随波纹`的相关模组，但更建议所有的模组都以添加入管理器的方式进行管理，以免带来不必要的麻烦。

:::warning 注意
管理器不会处理 `.\home\<用户名>\work\Mods` 路径下的非文件夹文件，在自行添加文件时请确保文件的准确性以免 3DMiGoto 读取模组文件时发生错误导致无法正常运行。
:::

### 模组索引文件
**模组索引文件** 相关内容请参考文档——[模组索引文件](/docs/mods-index)。

### 日志文件
**日志文件** 位于 `.\logs` 文件夹中，记录着你在软件中进行的各种操作。当发生错误后，可在此处找到对应错误，也可将 **日志文件** 提交给开发者让他们帮你解决遇到的问题。
