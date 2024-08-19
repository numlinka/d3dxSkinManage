# 目录结构

## 背景

目录结构是一个重要的部分，它决定了程序如何运行和如何存储数据。


## 目录结构

```TEXT
d3dxSkinManage/
├── home/                   // 存放用户的文件夹
│   ├── GenshinImpact/          // 用户文件夹，每一个用户的配置数据是独立的
│   │   ├── classification/         // 分类依据
│   │   │   └── ...                     // 分类依据文件
│   │   │
│   │   ├── modsIndex/              // 模组索引
│   │   │   └── ...                     // 模组索引文件
│   │   │
│   │   ├── work/                   // 工作目录，3DMiGoto 会释放到这个文件夹
│   │   │   ├── Mods/                   // 加载的模组会释放到这个文件夹
│   │   │   ├── d3d11.dll               // 最重要的文件
│   │   │   ├── scheme.json             // 工作方式，决定程序会如何处理和启动加载器
│   │   │   └── ...                     // 3DMiGoto 的其他文件
│   │   │
│   │   ├── thumbnail               // 头像缩略图文件夹
│   │   │   ├── _redirection.ini        // 缩略图配置文件
│   │   │   └── ...                     // 头像缩略图文件
│   │   │
│   │   ├── configuration           // 用户配置文件
│   │   ├── description.txt         // 用户描述文件，最简单的文本文件
│   │   └── picture.jpg             // 用户头像
│   │
│   ├── StarRail/               // 用户文件夹
│   └── .../
│
├── local/                  // 程序资源
│   ├── 7zip/                   // 7zip，很靠谱的解压缩软件
│   │   ├── 7z.dll
│   │   └── 7z.exe
│   │
│   └── iconbitmap.ico          // 程序图标
│
├── resources/              // 用户共享资源
│   ├── 3dmigoto/               // 3DMiGoto 版本文件夹，存放不同版本的压缩包
│   ├── cache/                  // 缓存文件夹
│   ├── mods/                   // 模组文件夹
│   ├── preview/                // 预览图文件夹
│   └── preview_screen/         // 全屏预览图文件夹
│
├── d3dxSkinManage.exe      // 主程序
└── update.exe              // 更新程序

```
