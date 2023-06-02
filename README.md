# d3dxSkinManage

## 简介

3DMigoto Mods 管理工具

[页面](https://d3dxskinmanage.numlinka.com/) | [聊天室](https://vocechat.numlinka.com/)

## 运行

### 运行环境

```
Python 3.10+
Windows 10+
```

### 依赖库

```
numpy
pillow
requests
pywin32
ttkbootstrap
windnd
webbrowser
```

### 运行

`python ./src/d3dxSkinManage.py`


## 工作方式

将 Mod 压缩包以其 SHA1 值命名储存在 ./resources/mods 中，并使用索引文件记录 Mod 文件的相关信息。

在加载 Mod 时将压缩包释放到对应 3DMigoto 的 Mods 文件夹。

[文件结构](doc/file-structure.md)
