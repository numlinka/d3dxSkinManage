# 更新时遇到问题

## 1. `d3dxSkinManage.exe` 报错

### 1.1. 未知错误 `ConnectionError`

`<class 'requests.exceptions.ConnectionError'>` 检查更新失败：未知错误

![](/static/image/e2641993.png)

::: info 原因
网络连接问题。
:::

::: tip 解决方法
检查你的网络连接。
:::

### 1.2. 网络代理错误

检查更新失败：代理错误

![](/static/image/6c85d813.png)

::: info 原因
你的网络代理设置错误。
:::

::: tip 解决方法
1. 更换网络代理；
2. 关闭你的系统代理。
:::


### 1.3. 找不到 `update.exe`

Windows 找不到 "update.exe"。请确定文件名是否正确后，再试一次。

![](/static/image/3db7b18c.png)

::: info 原因
`update.exe` 被删除或被隔离，当然这也有可能是人为的。
:::

::: tip 解决方法
在 [这里](/resources/update.md) 下载一个新的 `update.exe` 放在程序的的根目录下。
:::


## 2. `update.exe` 报错

### 2.1. `No administrator rights`

`[ERROR] No administrator rights.`

![](/static/image/e3775596.png)

::: info 原因
玄学报错，它不应该出现的。
:::

::: tip 解决方法
在关闭 d3dxSkinManage 后手动运行 `update.exe` 。
:::


### 2.2. `d3dxSkinManage.exe not exise`

`[ERROR] d3dxSkinManage.exe not exise.`

![](/static/image/f2dc237d.png)

::: info 原因
你修改了 d3dxSkinManage 程序的文件名。
:::

::: tip 解决方法
将 d3dxSkinManage 程序的文件名改回 `d3dxSkinManage.exe` 。
:::



## 3. 其他错误

### 3.1. 循环重启

若启动 `d3dxSkinManage.exe` 在检查更新的过程中，下载更新包的速度非常快，
并在唤醒 `update.exe` 后快速闪过一个报错 ( 或者没有 ) ，
并再次唤醒 `d3dxSkinManage.exe` 然后重复上述过程。

::: info 原因
更新包下载被中断，可能是网络问题，也有可能是服务器拒绝了请求 ( 返回码任然是 200 ) 。
:::

::: tip 解决方法
尝试 [手动替换更新](#_4-手动替换更新) 。
:::



## 4. 手动替换更新

在以下位置获取到更新包

在 [下载](/resources/download) 页面或是在 [社区](/help/community) 下载最新的 `update_xxx.zip` 文件 ( `xxx` 为版本号 )

解压并覆盖当前的文件。

