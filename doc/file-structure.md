```
\
├── home                        // 存放用户的文件夹
│   ├── GenshinImpact               // 用户文件夹，每一个用户的配置数据是独立的
│   │   ├── classification              // 分类依据
│   │   │   └── ...                         // 分类依据文件
│   │   │
│   │   ├── modsIndex                   // mods 索引
│   │   │   └── ...                         // mods 索引文件
│   │   │
│   │   ├── work                        // 工作目录， 3DMiGoto 会解压到这个文件夹
│   │   │   ├── Mods                        // 加载的 Mods 会解压到这个文件夹
│   │   │   ├── d3d11.dll                   // 最重要的文件
│   │   │   ├── scheme.json                 // 工作方式，决定程序会如何处理和启动 3DMiGoto
│   │   │   └── ...                         // 3DMiGoto 的其他文件
│   │   │
│   │   ├── configuration               // 用户配置文件，无特殊需要不要尝试去改动这个文件
│   │   ├── description.txt             // 用户描述文件，最简单的文本文件
│   │   └── picture.jpg                 // 用户头像
│   │
│   ├── StarRail                    // 用户文件夹
│   └── ...
│
├── local                       // 程序资源
│   ├── 7zip                        // 7zip，很靠谱的解压缩软件
│   │   ├── 7z.dll
│   │   └── 7z.exe
│   │
│   └── iconbitmap.ico              // 程序图标
│
├── resources                   // 用户资源
│   ├── 3dmigoto                    // 3DMiGoto 版本文件夹，存放不同版本的压缩包
│   │   └── ...
│   │
│   ├── 7zip                    // 这应该是个失误
│   │   ├── 7z.dll
│   │   └── 7z.exe
│   │
│   ├── cache                   // 缓存文件夹
│   │   └── ...
│   │
│   ├── mods                    // Mods 文件夹
│   │   └── ...
│   │
│   ├── preview                 // 预览图文件夹
│   │   └── ...
│   │
│   └── thumbnail               // 头像图文件夹
│       ├── _redirection.ini        // 重定向配置文件
│       └── ...
│
├── d3dxSkinManage.exe          // 主程序
└── update.exe                  // 更新程序
```