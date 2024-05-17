# -*- coding: utf-8 -*-

import os
import hashlib
import threading

import requests

import core
from constant import *

__event = threading.Event()


def deadlock():
    __event.wait()
    __event.clear()


def release_deadlock():
    __event.set()


def stop_control(msg: str = "未知错误"):
    core.window.status.set_status(f"{msg}", 1)
    deadlock()


def check():
    core.log.info("检查更新...", L.MODULE_UPDATE)
    try: # 我不是很相信这个东西
        if verify_key(core.argv.noupdatecheck):
            core.log.warning("跳过更新检查", L.MODULE_UPDATE)
            return
    except Exception as _:
        ...
    core.window.block.setcontent("正在检查更新...")
    try:
        index_requests = requests.get(core.env.INDEX)
        status_code = index_requests.status_code
        if status_code != 200:
            stop_control(f"检查更新失败: {status_code} 错误")
            return

    except requests.exceptions.ProxyError:
        core.window.messagebox.showerror("网络代理错误", "请检查网络代理设置或关闭代理后重试")
        stop_control(f"检查更新失败: 代理错误")
        return

    except Exception as e:
        stop_control(f"{e.__class__} 检查更新失败: 未知错误")
        return


    try:
        index_content = index_requests.json()
        version_code = index_content["version_code"]
        version_name = index_content["version_name"]
        content = index_content["content"]
        message = index_content["message"]

        if core.env.VERSION_CODE < version_code:
            get_update(index_content)

        if index_content["block"]:
            block(message)

        try:
            banuuidlst = index_content.get("ban", [])
            if core.env.uuid in banuuidlst:
                msg = ""
                msg += "请求被拒绝\n"
                msg += "该设备被标识为禁用\n\n"
                msg += "当前所使用的设备可能受到其他用户举报\n"
                msg += "请使用其他设备或联系管理员\n\n"
                msg += f"设备编号：{core.env.uuid}\n"
                core.window.block.setcontent(msg)
                stop_control(f"请求被拒绝")
                return

        except Exception as _:
            ...

    except Exception as e:
        stop_control(f"检查更新失败: 信息解析异常")
        return

    # updateContentFilePath = os.path.join(core.env.directory.resources.cache, "update-content")
    # if os.path.isfile(updateContentFilePath):
    #     try:
    #         with open(updateContentFilePath, "r", encoding="utf-8") as fileobject:
    #             updatecontent = fileobject.read()
    #         core.window.messagebox.showinfo(title="更新内容", message=updatecontent)

    #     except Exception:
    #         ...

    #     try:
    #         os.remove(updateContentFilePath)

    #     except Exception:
    #         ...



def get_update(index_content: dict):
    try:
        core.window.status.set_status(f"下载更新包")

        version_name = index_content["version_name"]
        update_content = index_content["content"]

        msg = ""
        msg += f"当前版本：{core.env.VERSION_NAME}\n"
        msg += f"更新版本：{version_name}\n\n"

        if isinstance(update_content, str): msgcn = update_content
        elif isinstance(update_content, list): msgcn = "\n".join(update_content)
        else: msgcn = ""

        msg += msgcn

        core.window.block.setcontent(msg)

        # if msgcn:
        #     updateContentFilePath = os.path.join(core.env.directory.resources.cache, "update-content")
        #     try:
        #         with open(updateContentFilePath, "w", encoding="utf-8") as fileobject:
        #             fileobject.write(msgcn)
        #     except Exception:
        #         ...

        url = index_content["get"]["url"]
        mode = index_content["get"]["mode"]


        # content = core.module.wget.wget(url, mode)
        # if content is None: raise Exception

        filepath = os.path.join(core.env.directory.resources.cache, "update.pack")
        # with open(filepath, "wb") as fileobject: fileobject.write(content)

        headers = {
            "user-agent": S.USER_AGENT,
            "accept-language": S.ACCEPT_LANGUAGE
        }

        response = requests.get(url, stream=True, headers=headers)
        file_size = int(response.headers.get('content-length', 0))

        with open(filepath, 'wb') as file:
            # 使用iter_content方法以1 KB的数据块下载文件，并在下载每个数据块后调用回调函数
            for chunk_number, chunk in enumerate(response.iter_content(chunk_size=1024)):
                file.write(chunk)
                # 调用回调函数来显示下载进度
                progress_bar(chunk_number + 1, 1024, file_size)


        target = "update.exe"
        os.system(f"start \"update\" {target}")
        core.window.status.set_status("等待程序重启", 1)
        os._exit(0)

    except Exception as e:
        stop_control("更新包下载失败")


def progress_bar(chunk_number, chunk_size, total_size):
    percent_complete = int((chunk_number * chunk_size / total_size) * 100)
    core.window.status.set_progress(percent_complete)


def block(message):
    core.window.block.setcontent(message)
    stop_control("启动程序被拒绝")
    ...


def verify_key(key: str):
    # You can clearly see how the key is calculated.
    # It's just a gentleman's agreement.
    u8 = "utf-8"
    s1, s2, s3 = hashlib.sha512(), hashlib.sha512(), hashlib.md5()
    s1.update(key.encode(u8))
    s2.update(s1.hexdigest().encode(u8))
    s3.update(s2.hexdigest().encode(u8))
    return s3.hexdigest() == "c9bca91be66be860c2505d4a93e2b704"
