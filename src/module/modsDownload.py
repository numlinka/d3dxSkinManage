# -*- coding: utf-8 -*-


import os
import hashlib

import requests

import core

from . import exceptions


class ModsDownload(object):
    def wget(self, url: str, mode: str, headers: dict = ...) -> bytes | None:
        if mode not in self.__table:
            core.Log.error(f"不被支持的下载模式 {mode}")
            raise exceptions.ModDownloadException(f"不被支持的下载模式 {mode}")

        core.Log.debug(f"wget {url} {mode} 模式")
        content = self.__table[mode](url, headers)

        return content


    def lanzou(self, url: str, headers: dict = ...) -> bytes | None:
        analysis_url = f"https://api.hanximeng.com/lanzou/?url={url}"

        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
            'referer': url,
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
            } if not isinstance(headers, dict) else headers

        analysis_requests = requests.get(analysis_url)

        if analysis_requests.status_code != 200:
            raise exceptions.ModDownloadException(f"lanzou 解析失败 {analysis_requests.status_code} 错误")

        analysis_result = analysis_requests.json()

        finally_url = analysis_result['downUrl']

        result = requests.get(finally_url, headers=headers)

        if result.status_code != 200:
            raise exceptions.ModDownloadException(f"{result.status_code} 错误")

        return result.content


    def direct(self, url: str, headers: dict = ...) -> bytes | None:
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
            } if not isinstance(headers, dict) else headers

        result = requests.get(url, headers=headers)

        if result.status_code != 200:
            raise exceptions.ModDownloadException(f"{result.status_code} 错误")

        return result.content


    def __init__(self):
        self.__table = {}
        self.__table['lanzou'] = self.lanzou
        self.__table['direct'] = self.direct
        self.__table['get'] = self.direct


    def downloadTask(self, SHA: str):
        item = core.Module.ModsIndex.get_item(SHA)
        getMethod = item.get('get', None)
        if getMethod is None: return

        name = item['name']
        object_ = item['object']

        LOCAL = os.path.join(core.environment.resources.mods, SHA)
        if os.path.isfile(LOCAL):
            msg = f'{SHA}\n{object_} :: {name} 已存在\n是否仍然下载\n这会覆盖本地文件'
            an = core.UI.Messagebox.askyesno(msg, '文件已存在')
            if not an: return

        for method_ in getMethod:
            try:
                url = method_['url']
                mode = method_.get('mode', 'get')
                headers = method_.get('headers', ...)
                content = self.wget(url, mode, headers)

                sha1 = hashlib.sha1()
                sha1.update(content)
                contentSHA = sha1.hexdigest()

                if SHA != contentSHA.upper():
                    raise exceptions.SHA1VerifyError("文件散列值不一致")

                with open(LOCAL, 'wb') as fileobject:
                    fileobject.write(content)

                core.Module.ModsManage.refresh()
                core.UI.Windows.after(0, core.UI.ModsManage.reload_classification)
                core.UI.Windows.after(0, core.UI.ModsWarehouse.refresh)
                break

            except Exception as e:
                core.Log.error(f"{e.__class__} {e}")
                Exc = e

        else:
            raise Exc

