# -*- coding: utf-8 -*-

import os
import threading

import win32api
import requests

import core

__event = threading.Event()


def deadlock():
    __event.wait()
    __event.clear()


def release_deadlock():
    __event.set()


def clearLoginList():
    core.UI.Login.Treeview_users
    [core.UI.Login.Treeview_users.delete(row) for row in core.UI.Login.Treeview_users.get_children()]


def stop_control(msg: str = '未知错误'):
    core.UI.Status.set_status(f'{msg}', 1)
    deadlock()


def check():
    try:
        index_requests = requests.get(core.environment.index)
        status_code = index_requests.status_code
        if status_code != 200:
            stop_control(f'检查更新失败: {status_code} 错误')
            return

    except requests.exceptions.ProxyError:
        core.UI.Messagebox.showerror('网络代理错误', '请检查网络代理设置或关闭代理后重试')
        stop_control(f'检查更新失败: 代理错误')
        return

    except Exception as e:
        stop_control(f'{e.__class__} 检查更新失败: 未知错误')
        return


    try:
        index_content = index_requests.json()
        version_code = index_content['version_code']
        version_name = index_content['version_name']
        content = index_content['content']
        message = index_content['message']

        if core.environment.version_code < version_code:
            get_update(index_content)

        if index_content['block']:
            block(message)

    except Exception:
        stop_control(f'检查更新失败: 信息解析异常')
        return

    updateContentFilePath = os.path.join(core.environment.resources.cache, 'update-content')
    if os.path.isfile(updateContentFilePath):
        try:
            with open(updateContentFilePath, 'r', encoding='utf-8') as fileobject:
                updatecontent = fileobject.read()
            core.UI.Messagebox.showinfo(title='更新内容', message=updatecontent)
        except Exception:
            ...
        try:
            os.remove(updateContentFilePath)
        except Exception:
            ...



def get_update(index_content: dict):
    try:
        core.UI.Status.set_status(f'下载更新包')

        version_name = index_content['version_name']
        update_content = index_content['content']

        msg = ''
        msg += f'当前版本：{core.environment.version}\n'
        msg += f'更新版本：{version_name}\n\n'

        if isinstance(update_content, str): msgcn = update_content
        elif isinstance(update_content, list): msgcn = '\n'.join(update_content)
        else: msgcn = ''

        msg += msgcn

        core.windows.LabelMessage['text'] = msg


        if msgcn:
            updateContentFilePath = os.path.join(core.environment.resources.cache, 'update-content')
            try:
                with open(updateContentFilePath, 'w', encoding='utf-8') as fileobject:
                    fileobject.write(msgcn)
            except Exception:
                ...

        url = index_content['get']['url']
        mode = index_content['get']['mode']


        content = core.Module.ModsDownload.wget(url, mode)
        if content is None: raise Exception

        filepath = os.path.join(core.environment.resources.cache, 'update.pack')
        with open(filepath, 'wb') as fileobject: fileobject.write(content)
        target = 'update.exe'
        # win32api.ShellExecute(None, 'open', target, None, os.path.realpath(os.path.dirname(target)), 1)
        os.system(f'start "update" {target}')
        stop_control('等待程序重启')
        os._exit(0)

    except Exception as e:
        stop_control('更新包下载失败')


def block(message):
    core.windows.LabelMessage['text'] = message
    stop_control('启动程序被拒绝')
    ...
