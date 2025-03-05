# 启动参数

## 背景

在程序启动时，可以设置一些参数，这些参数可以影响程序运行时的行为。该设计的目的是让用户可以开启或关闭某些特殊的功能，和为自动化行为或测试提供支持。


## 参数详列

| 参数                    | 说明 |
| :---                    | :--- |
| `--autologin {userenv}` | 自动登录到指定用户环境 |
| `--noupdatecheck {key}` | 禁用更新检查 |
| `--noplugin`            | 禁用插件 |
| `--demomode`            | 演示模式 |

### `--autologin`

该参数用于自动登录到指定用户环境，`{userenv}` 为用户环境名称，它必须是一个有效值，若指定用户环境不存在则不做任何处理。

示例：
```Shell
./d3dxSkinManage --autologin GenshinImpact
```

### `--noupdatecheck`

跳过程序的联网检查阶段，使得程序可以完全脱机运行，`{key}` 为一个校验值，在不同的程序版本上可能会不同，详细用法参考 [禁用更新检查](/help/disable-update-check) 页面。

示例：
```Shell
./d3dxSkinManage --noupdatecheck tocDl4l4YsvyMcBL
```

### `--noplugin`

禁用插件加载器，程序将不加载任何插件，多数时候用于主程序调试。

### `--demomode`

演示模式，程序会减少一些内容的出现。
