# 缓存清理工具

你是否因为模组缓存文件占用过多内存而烦恼，但是现在没有关系，这个工具可以帮助你清理不常用的模组的缓存文件，为你的存储空间释放无意义的压力。


## 打开工具窗口

在主程序的 **工具** 页面选择 **缓存清理工具** 即可打开工具窗口。

![](/static/image/203a840f.png)


## 使用方法

在清理工具窗口中点击对应的 **清理** 按钮即可清理对应类型的缓存文件。

![](/static/image/be9a2f31.png)

以下是各类型的缓存文件说明：
### 常用缓存
若模组对应的 `SHA` 在[模组索引文件](/docs/mods-index.html#模组索引文件)中存在且其存在[模组源文件](/help/tutorial-lexical-analysis.html#模组源文件)，则该模组所对应的[模组缓存文件](/help/tutorial-lexical-analysis.html#模组缓存文件)为 **常用缓存**。

### 不常用缓存
若模组对应的 `SHA` 在[模组索引文件](/docs/mods-index.html#模组索引文件)中存在且其不存在[模组源文件](/help/tutorial-lexical-analysis.html#模组源文件)，则该模组所对应的[模组缓存文件](/help/tutorial-lexical-analysis.html#模组缓存文件)为 **不常用缓存**。

### 无效缓存
若以上两种情况都不存在的，则该模组所对应的[模组缓存文件](/help/tutorial-lexical-analysis.html#模组缓存文件)为 **无效缓存**。

#### 简述
根据自己的需要进行清除即可，**无效缓存**及**不常用缓存**是可以直接清理的，**常用缓存**如果你没有更改过工作文件下的[模组缓存文件](/help/tutorial-lexical-analysis.html#模组缓存文件)的相关信息也是可以直接清理。

若更改过模组缓存文件，建议每次更改缓存的信息后，就使用 [导出模组缓存文件插件](/resources/plugins/export_wort_mod_file) 将模组缓存文件重新导入进管理器，这样子常用缓存也可以正常清除不用担心修改的信息丢失。

