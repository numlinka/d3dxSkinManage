# -*- coding: utf-8 -*-

import requests


class WebGet(object):
    __table = {}


    def wget(self, url: str, mode: str) -> bytes | None:
        if mode not in self.__table:
            return None

        try:
            content = self.__table[mode](url)

        except Exception:
            content = None

        return content


    @staticmethod
    def lanzou(url: str) -> bytes | None:
        analysis_url = f"https://api.hanximeng.com/lanzou/?url={url}"

        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
            'referer': url,
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
            }

        analysis_requests = requests.get(analysis_url)

        if analysis_requests.status_code != 200:
            return analysis_requests.status_code

        analysis_result = analysis_requests.json()

        finally_url = analysis_result['downUrl']

        result = requests.get(finally_url, headers=headers)

        if result.status_code != 200:
            return result.status_code

        return result.content


    @staticmethod
    def direct(url: str) -> bytes | None:
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
            }

        result = requests.get(url, headers=headers)

        if result.status_code != 200:
            return None

        return result.content



    __table['lanzou'] = lanzou
    __table['direct'] = direct


    def __init__(self):
        self.__table = {}
        self.__table['lanzou'] = self.lanzou
        self.__table['direct'] = self.direct