# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import re
import os
import hashlib

# site
import requests

# local
import core
from constant import *

# self
from .exceptions import *


def get_lanzou_direct_from_api_hanximeng(url: str, headers: dict = ...) -> str:
    analysis_url = f"https://api.hanximeng.com/lanzou/?url={url}"

    headers = {
        "user-agent": S.USER_AGENT,
        "referer": url,
        "accept-language": S.ACCEPT_LANGUAGE
        } if not isinstance(headers, dict) else headers

    analysis_requests = requests.get(analysis_url)

    if analysis_requests.status_code != 200:
        raise AnalyzeError(f"lanzou 解析失败 {analysis_requests.status_code} 错误")

    analysis_result = analysis_requests.json()

    if analysis_result["code"] != 200:
        raise AnalyzeError(f"lanzou 解析失败 {analysis_result['msg']}")

    return analysis_result["downUrl"]


def get_lanzou_direct_from_self_api(url: str, headers: dict = ...) -> str:
    analysis_url = f"http://lanzou-api.numlinka.com?url={url}"

    headers = {
        "user-agent": S.USER_AGENT,
        "referer": url,
        "accept-language": S.ACCEPT_LANGUAGE
        } if not isinstance(headers, dict) else headers

    analysis_requests = requests.get(analysis_url)

    if analysis_requests.status_code != 200:
        raise AnalyzeError(f"lanzou 解析失败 {analysis_requests.status_code} 错误")

    analysis_result = analysis_requests.json()

    if analysis_result["code"] != 200:
        raise AnalyzeError(analysis_result["msg"])

    return analysis_result["data"]["url"]


def direct(url: str, headers: dict = ...) -> bytes | None:
    headers = {
        "user-agent": S.USER_AGENT,
        "accept-language": S.ACCEPT_LANGUAGE
        } if not isinstance(headers, dict) else headers

    result = requests.get(url, headers=headers)

    if result.status_code != 200:
        raise StatusCodeError(f"{result.status_code} 错误")

    return result.content


def lanzou(url: str, headers: dict = ...) -> bytes | None:
    headers = {
        "user-agent": S.USER_AGENT,
        "referer": url,
        "accept-language": S.ACCEPT_LANGUAGE
        } if not isinstance(headers, dict) else headers

    core.log.debug("解析蓝奏云直链...", L.MODULE_WGET)
    finally_url = get_lanzou_direct_from_api_hanximeng(url)

    core.log.debug("获取蓝奏云文件...", L.MODULE_WGET)
    result = requests.get(finally_url, headers=headers)

    if result.status_code != 200:
        raise StatusCodeError(f"{result.status_code} 错误")

    return result.content


__table = {
    "lanzou": lanzou,
    "direct": direct,
    "get": direct
}


def wget(url: str, mode: str, headers: dict = ...) -> bytes | None:
    if mode not in __table:
        core.log.error(f"不被支持的下载模式 {mode}", L.MODULE_WGET)
        raise DownloadModeError(f"不被支持的下载模式 {mode}")

    core.log.debug(f"wget-{mode} {url}", L.MODULE_WGET)
    content = __table[mode](url, headers)

    return content

