# 插件使用教程

d3dxSkinManage 在 1.5.19 版本之后允许加载插件，你可以通过插件来丰富程序的功能。

::: warning 警告
插件仅为实验性功能，我们不提供任何安全性、品质性和兼容性保证。
:::


## 如何加载插件

首先在 [插件资源](/resources/plugins) 页面下载你所需要的插件压缩包，然后将它解压到 `./plugins/` 目录下。你需要保证其表现为一个文件夹且里面有一个 `main.py` 文件，不要出现文件夹嵌套，文件夹名称不能出现非英文字符，否则会导致插件无法被识别，或不能正常加载。

```TEXT
d3dxSkinManage/
├── plugins/
│   ├── plugin-name-1/
│   │   ├── main.py
│   │   ├── description.txt
│   │   └── ...
│   │
│   ├── plugin-name-2/
│   │   ├── main.py
│   │   ├── description.txt
│   │   └── ...
│   │
│   └── ...
│
└── ...
```

::: danger 错误示例
以下为错误的解压示例，插件将不能正常加载。
:::

```TEXT
d3dxSkinManage/
├── plugins/
│   ├── plugin-name-1/      <-- 文件夹嵌套  // [!code error]
│   │   └── plugin-name-1/  <-- 文件夹嵌套  // [!code error]
│   │       ├── main.py
│   │       ├── description.txt
│   │       └── ...
│   │
│   ├── xxx 插件/  <-- 文件夹名带中文和空格  // [!code error]
│   │   ├── main.py
│   │   ├── description.txt
│   │   └── ...
│   │
│   ├── main.py          <-- 插件内容出现在根目录  // [!code error]
│   ├── description.txt  <-- 插件内容出现在根目录  // [!code error]
│   │
│   └── ...
│
└── ...
```


## 检查插件是否被加载

在 1.5.20 版本后在软件的 **插件** 页面会列举已加载的插件，若插件加载失败则不会出现在该页面，但这并不意味着插件的内容没有对程序产生影响。你可以在日志文件中搜索 `(plugins)` 相关的日志，并查看错误信息。


## 失效和更新

随着版本更新，程序的部分结构会发生改变，这需要插件跟进，因此你需要检查你的插件是否为最新版本。程序不会自动帮你完成更新，你需要手动检查插件是否为最新版本，并更新。


## 视频教程链接

[插件加载教程](https://www.bilibili.com/video/BV1iN4y1173s)　[插件加载失败原因](https://www.bilibili.com/video/BV19Z421E725/)

视频教程由 [@黎愔](/contribution) 录制和提供。
