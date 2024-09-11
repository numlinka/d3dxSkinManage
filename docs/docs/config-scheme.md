# 加载器行为文件

## 背景

加载器行为文件通常储存在 `./home/<userenv>/work/` 位置，是一个名为 `scheme.json` 的 JSON 文件。该配置文件不是必要的，它不是**加载器的配置文件**，而是决定程序**如何操作加载器**的配置文件，叫它**行为文件**是为了避免与**加载器的配置文件**混淆。


## 配置文件格式

配置文件需要提供以下键值对：

### `dll`

加载器使用的 DLL 文件名，默认为 `d3d11.dll` 。

### `version`

表示加载器的版本名称，根据自己的个性设置，可以是任意的字符串。

### `launch`

启动加载器时要运行的程序文件名，默认为 `3DMigoto Loader.exe` 。

### `set-mode`

修改**加载器的配置文件**的模式：

- `conventional`：将 `d3dx.ini` 中的 `target` 项设置为**游戏路径**。

_注：**游戏路径**来至于管理器内部的配置。_

### `set-need`

决定 [`set-mode`](#set-mode) 是否生效，为 `false` 时不进行任何操作。

### `loading-mode`

加载模式：

- `inject`: 注入 DLL 到游戏进程。


## 示例参考

::: warning 注意
示例仅供参考，请根据实际情况修改。
:::

```json
{
	"dll": "d3d11.dll",
	"version": "v7.0 playing mods",
	"launch": "3DMigoto Loader.exe",
	"set-mode": "conventional",
	"set-need": true,
	"loading-mode": "inject"
}
```
