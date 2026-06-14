<div align="center">

<a href="https://d3dxskinmanage.numlinka.com">
  <img width="128px" src="favicon.ico" alt="d3dxSkinManage">
</a>

# d3dxSkinManage

_3DMigoto 皮肤 Mods 管理工具_

<div>
<a href="https://www.gnu.org/licenses/gpl-3.0.zh-cn.html" target="_blank">
  <img src="https://img.shields.io/badge/License-GPLv3-lightblue" alt="GPLv3"/>
</a>
<a href="https://github.com/numlinka/d3dxSkinManage/releases" target="_blank">
  <img src="https://img.shields.io/badge/releases-1.6.4-lightblue" alt="releases"/>
</a>
<a href="https://www.python.org/downloads/release/python-3120/" target="_blank">
  <img src="https://img.shields.io/badge/Python-3.12-lightblue" alt="Python3.12"/>
</a>
</div>

<a href="https://d3dxskinmanage.numlinka.com">
  文档
</a>
·
<a href="https://d3dxskinmanage.numlinka.com/resources/download">
  下载
</a>
·
<a href="https://d3dxskinmanage.numlinka.com/help/tutorial">
  快速上手
</a>
·
<a href="https://d3dxskinmanage.numlinka.com/resources">
  扩展资源
</a>

</div>

<p></p>

<div align="left">

## 概述

**d3dxSkinManage** 是一款专为 **3DMigoto** 设计的皮肤模组管理工具。它帮助你更规范地组织、备份和管理模组文件，支持多游戏、多用户环境，并提供插件系统以扩展功能。

> 你可以把马带到水边，但你不能让它读说明书。

---

## 核心特性

### 🕹️ 多用户环境
为不同的游戏设置独立的用户环境，隔离用户数据与个性化设置。支持自定义头像、描述信息等。

### 💾 压缩存储与索引管理
模组文件以 **SHA-1** 命名压缩存储，通过索引文件记录模组信息，程序自动计算分组而非依赖文件夹组织。有效减少磁盘空间占用。

### 🗂️ 智能分类与筛选
支持基于分类参照的动态分类、通配符匹配，以及按分类、对象、SHA、名称、年龄分级等多维度筛选。

### 🛠️ 加载器集成
内置 3DMigoto 加载器管理，支持 **GIMI**（原神）、**SRMI**（星穹铁道）、**HIMI**（崩坏3）、**WWMI**（鸣潮）、**ZZMI**（绝区零）等多种加载器的一键部署与注入。

### 🔌 插件系统
提供实验性的插件加载机制，你可通过插件扩展程序功能，社区已提供多种实用插件：
- **Mod 修复插件**：游戏版本更新后修复失效模组
- **批量处理工具**：批量删除、导出、导入模组
- **自动登录与重载**：自动化工作流
- **多预览图、排序编辑、快捷键编辑**等

### 🖼️ 头像缩略图
支持为分类和对象设置头像缩略图，通过文件名匹配或配置文件灵活管理，帮助快速识别。

---

## 支持的平台

| 系统要求 |
| :--- |
| **Windows 10** x64 及以上非精简版系统 |

---

## 快速开始

### 1️⃣ 下载与安装

从 [下载页面](https://d3dxskinmanage.numlinka.com/resources/download) 获取完整程序包，解压到合适位置即可使用。

> 路径中请勿包含中文等非 ASCII 字符，不要使用管理员权限运行。

### 2️⃣ 创建用户环境

启动程序后，在用户列表下方点击 **新建用户环境**，设置用户名、头像和描述。

### 3️⃣ 添加加载器

从 [加载器下载页](https://d3dxskinmanage.numlinka.com/resources/3dmigoto) 获取对应游戏的 3DMigoto 压缩包，放入 `./resources/3dmigoto` 目录，重启程序后在环境设置中选择对应版本。

### 4️⃣ 添加模组

将模组压缩包或文件夹拖拽到程序窗口，填写作用对象、模组名称、年龄分级等信息即可。

### 5️⃣ 启动游戏

在环境设置中配置游戏路径，点击 **启动加载器** 再点击 **启动游戏** 即可。

---

## 支持的模组资源

| 游戏 | 加载器 | 模组站点 |
| :--- | :--- | :--- |
| 原神 (Genshin Impact) | GIMI | [GameBanana](https://gamebanana.com/games/8552) · [Nexus Mods](https://www.nexusmods.com/genshinimpact) |
| 崩坏：星穹铁道 (Honkai Star Rail) | SRMI | [GameBanana](https://gamebanana.com/games/18366) · [Nexus Mods](https://www.nexusmods.com/honkaistarrail) |
| 崩坏3 (Honkai Impact 3rd) | HIMI | [GameBanana](https://gamebanana.com/games/10349) |
| 绝区零 (Zenless Zone Zero) | ZZMI | [GameBanana](https://gamebanana.com/games/19567) · [Nexus Mods](https://www.nexusmods.com/games/zenlesszonezero) |
| 鸣潮 (Wuthering Waves) | WWMI | [GameBanana](https://gamebanana.com/games/20357) · [Nexus Mods](https://www.nexusmods.com/wutheringwaves) |
| 尘白禁区 (Snowbreak Containment Zone) | — | [GameBanana](https://gamebanana.com/games/19719) · [Nexus Mods](https://www.nexusmods.com/snowbreakcontainmentzone) |

> 更多模组资源及创作者社区信息请参考 [模组资源页面](https://d3dxskinmanage.numlinka.com/resources/modules)。

---

## 社区

| 平台 | 链接/信息 |
| :--- | :--- |
| GitHub | [numlinka/d3dxSkinManage](https://github.com/numlinka/d3dxSkinManage) |
| QQ 群 | **743841257** / **823171515** / **783983577** / **150020584**（QQ 等级 ≥ 16 自动审批） |

---

## 目录结构

```
d3dxSkinManage/
├── home/                   # 用户环境文件夹
│   └── <用户名>/
│       ├── classification/     # 分类参照
│       ├── modsIndex/          # 模组索引
│       ├── work/               # 工作目录（3DMigoto 释放位置）
│       ├── thumbnail/          # 头像缩略图
│       ├── configuration       # 用户配置
│       └── ...
├── local/                  # 程序资源
├── resources/              # 用户共享资源
│   ├── 3dmigoto/              # 加载器版本包
│   ├── mods/                  # 模组文件存储
│   ├── preview/               # 预览图
│   └── ...
├── plugins/                # 扩展插件
├── logs/                   # 日志文件
├── d3dxSkinManage.exe      # 主程序
└── update.exe              # 更新程序
```

---

## 启动参数

| 参数 | 说明 |
| :--- | :--- |
| `--autologin {userenv}` | 自动登录到指定用户环境 |
| `--noupdatecheck {key}` | 禁用更新检查 |
| `--noplugin` | 禁用插件 |
| `--demomode` | 演示模式 |

---

## 技术信息

- **开发语言**：Python 3.12
- **许可证**：[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.zh-cn.html)
- **项目作者**：[numlinka](https://github.com/numlinka)
- **文档站点**：[d3dxskinmanage.numlinka.com](https://d3dxskinmanage.numlinka.com)

---

## 贡献

我们欢迎任何形式的贡献！项目贡献者信息请查看 [贡献者页面](https://d3dxskinmanage.numlinka.com/contribution)。

---

<div align="center">

<sub>
  赞助页面：<a href="https://afdian.com/a/numlinka">爱发电</a> ·
  联系方式：numlinka@163.com
</sub>

</div>

</div>
