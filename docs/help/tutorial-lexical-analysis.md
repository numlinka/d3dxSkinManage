# 词汇解析
在使用 d3dxSkinManage 及阅读文档的过程中，你会遇到一些管理器中所涉及的词汇，这些在入门时无法理解的词汇，会在下方进行解释。

##

### 3DMigoto
**3DMigoto** 是修改模组的一种程序，该程序是可以单独执行的，但随着你所使用的模组变多，你需要对模组文件的操作会很繁琐，来避免导入作用于同一对象的模组多次导入而产生炸模型的问题，**模组管理工具** 也因此被开发出来辅助整理模组。也就是说 **模组管理工具** 只是一种手段，如果没有了解一定的 **3DMigoto** 运行原理，在使用 **模组管理工具** 也会遇到许多的阻碍。所以建议先粗略学会 `如何使用 3DMigoto` 后再尝试使用 d3dxSkinManage 管理器进行便捷化管理模组。

### SHA
你只需要知道它是本程序中识别模组的**唯一标识**即可，你可以通过它寻找到对应模组，虽然一般不使用这个值进行搜索。

### 模组 / mod
**模组** <weaken>(mod)</weaken> 是用于修改游戏内如角色、怪物、场景、UI等的显示形式的文件，也是本管理工具唯一操作的 `实体`。你获取它时，它通常是一个压缩包文件；而当你在 3DMigoto 中使用它时，你需要将对应的压缩包解压出来 。在本管理工具中，**选择栏** 中的每一个值都对应着一个**模组**，其他如 **SHA**、**分类**、**作用对象** 等只是为了更好的寻找或操作模组所产生的 `虚体`，其他除 **SHA** 以外的 `虚体` 都可以通过 **自定义** 的方式辅助你实现更方便的操作。

### 作用对象 / 对象
**作用对象** 是指 Mod 所修改的游戏内如角色、怪物、场景、UI等的显示形式，当使用 **3DMigoto** 程序导入作用于同一对象的多个**模组**时，会导致该作用对象炸模型。所以在所以本工具时，请将作于与相同对象的模组存储于同一个对象名称中，本工具会通过算法使同一对象下的模组只能同时导入一个，你可以通过使用本工具的相关操作实现切换模组。

### 分类
**分类** 是指对**作用对象**的分类，将具有类似性质的对象存储于同一个分类，可以更方便寻找到对应的**作用对象**下存储的模组，实现更高效的切换模组。

### 模组源文件 / 模组原始文件 {#模组源文件}
当你将 **模组** 文件导入到 d3dxSkinManage 中后，这个文件会以压缩包的形式存储在 `.\resources\mods` 文件夹中，并以 **SHA** 命名，这个文件就是 **模组源文件**。

### 模组缓存文件
当你启用模组后，管理器会将 **模组源文件** 解压到 `.\home\<用户名>\work\Mods` 文件夹中，而 `.\home\<用户名>\work\Mods` 下的文件夹下的这些文件就是 **模组缓存文件**。