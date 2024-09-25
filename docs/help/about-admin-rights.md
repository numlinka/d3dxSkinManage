# 关于管理员权限

当我们需要修改系统设置或执行某些敏感操作时，通常需要管理员权限。然而，大多数程序运行时并不需要管理员权限，例如 d3dxSkanManage。不要主动给予程序管理员权限，当程序确实需要时，它会自行请求。

首先，不要轻易为不熟悉的程序授予管理员权限，这可能导致系统设置被篡改，甚至危及系统安全。提高安全意识，避免设备遭受网络病毒的攻击。

其次，Windows 文件钩子不支持跨用户数据传输，除非关闭 UAC 或以管理员权限运行资源管理器，否则文件拖拽功能将无法使用。
