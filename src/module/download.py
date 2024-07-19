# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import re
import os
import hashlib
import threading

# libs
import requests

# local
import core
from constant import *

# self
from .exceptions import *

class ModDownload (object):
    def __init__ (self):
        self.doing_list = []
        self.__call_lock = threading.RLock()


    def __add_sha(self, SHA):
        with self.__call_lock:
            self.doing_list.append(SHA)

        core.construct.event.set_event(E.MOD_DOWNLOAD_TASK_ALTERATION)


    def __del_sha(self, SHA):
        with self.__call_lock:
            if SHA in self.doing_list:
                index = self.doing_list.index(SHA)
                del self.doing_list[index]

        core.construct.event.set_event(E.MOD_DOWNLOAD_TASK_ALTERATION)


    def download_task(self, SHA: str):
        core.log.info(f"下载 Mod {SHA} ...", L.MODULE_WGET)
        item = core.module.mods_index.get_item(SHA)
        getMethod = item.get("get", None)

        name = item["name"]
        object_ = item["object"]

        if getMethod is None:
            core.window.messagebox.showerror(title="缺省数据", message=f"f{SHA}\n{object_} :: {name}\n该 SHA 没有提供 get 参数")
            return

        local_path = os.path.join(core.env.directory.resources.mods, SHA)
        if os.path.isfile(local_path):
            msg = f"{SHA}\n{object_} :: {name} 已存在\n是否仍然下载\n这会覆盖本地文件"
            an = core.window.messagebox.askyesno(title="文件已存在", message=msg)
            if not an: return

        with self.__call_lock:
            is_going = SHA in self.doing_list

            if not is_going:
                self.__add_sha(SHA)


        if is_going:
            # 消息窗口会阻塞锁
            # 从而影响其他刷新事件
            # 所以它应该在锁外面进行
            msg = f"{SHA}\n{object_} :: {name}\n已存在于下载任务中\n请不要重复添加任务"
            core.window.messagebox.showerror(title="任务重复", message=msg)
            return


        finally_exception = None

        for method_ in getMethod:
            try:
                url = method_["url"]
                mode = method_.get("mode", "get")
                headers = method_.get("headers", ...)
                content = core.module.wget.wget(url, mode, headers)

                sha1 = hashlib.sha1()
                sha1.update(content)
                contentSHA = sha1.hexdigest()

                if SHA != contentSHA.upper():
                    raise SHA1VerifyError("文件散列值不一致")

                with open(local_path, "wb") as fileobject:
                    fileobject.write(content)

                # 如果下载成功则取消异常信息
                finally_exception = None
                break

            except DownloadModeError as e:
                core.log.error(f"Mod {SHA} 下载失败 下载模式错误 {e}", L.MODULE_WGET)
                finally_exception = e

            except StatusCodeError as e:
                core.log.error(f"Mod {SHA} 下载失败 状态码错误 {e}", L.MODULE_WGET)
                finally_exception = e

            except requests.exceptions.ProxyError as e:
                core.log.error(f"Mod {SHA} 下载失败 代理错误 {e}", L.MODULE_WGET)
                finally_exception = e

            except AnalyzeError as e:
                core.log.error(f"Mod {SHA} 下载失败 解析错误 {e}", L.MODULE_WGET)
                finally_exception = e

            except SHA1VerifyError as e:
                core.log.error(f"Mod {SHA} 下载失败 校验错误 {e}", L.MODULE_WGET)
                finally_exception = e

            except Exception as e:
                core.log.error(f"Mod {SHA} 下载失败 {e.__class__} {e}", L.MODULE_WGET)
                finally_exception = e


        self.__del_sha(SHA)


        e = finally_exception
        base_msg = f"{SHA}\n{object_} :: {name}"

        if e is None:
            # 什么事情都没有发生
            ...

        elif isinstance(e, DownloadModeError):
            core.window.messagebox.showerror(title="下载失败", message=f"{base_msg}\下载模式错误\n{e}")
            return

        elif isinstance(e, StatusCodeError):
            core.window.messagebox.showerror(title="下载失败", message=f"{base_msg}\状态码错误\n{e}")
            return

        elif isinstance(e, requests.exceptions.ProxyError):
            core.window.messagebox.showerror(title="下载失败", message=f"{base_msg}\n网络代理错误\n{e}")
            return

        elif isinstance(e, AnalyzeError):
            core.window.messagebox.showerror(title="下载失败", message=f"{base_msg}\n蓝奏云直链解析错误\n{e}")
            return

        elif isinstance(e, SHA1VerifyError):
            core.window.messagebox.showerror(title="下载失败", message=f"{base_msg}\n校验错误\n{e}")
            return

        else:
            core.window.messagebox.showerror(title="下载失败", message=f"{base_msg}\n未定义错误: {e.__class__}\n{e}")
            return


        core.log.info(f"Mod {SHA} / {object_} :: {name} 下载完成", L.MODULE_WGET)
        core.module.mods_manage.refresh()


    def is_downloading(self, SHA):
        with self.__call_lock:
            return SHA in self.doing_list
