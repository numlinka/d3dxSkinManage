# -*- coding: utf-8 -*-

# std
import os
import re
import threading

import core
from constant import *


class IndexManage (object):
    def __init__(self):
        # index 文件夹路径
        self.__index_directory = ""

        # json index 文件列表
        self.__json_index_file_list = []

        # 操作锁
        self.__call_lock = threading._RLock()


    def update_index_file_list(self):
        "更新 index 文件列表"
        core.log.info("更新 index 文件列表", L.MODULE)
        with self.__call_lock:
            self.__index_directory = core.userenv.directory.mods_index

            usable_file_list = [
                os.path.join(root, filename)
                for root, dirs, files in os.walk(self.__index_directory)
                if len([dirname for dirname in re.split(K.RE.PATH_SPLIT, root) if dirname.lower().startswith(K.DISABLED)]) == 0
                for filename in files
                if not filename.lower().startswith(K.DISABLED)
            ]

            self.__json_index_file_list = [filepath for filepath in usable_file_list if filepath.lower().endswith(K.SUFFIX_JSON)]

            core.log.debug(f"index file list: [{self.__json_index_file_list}]", L.MODULE)


    def load_index_file(self, file_path: str, mode: str, action: str = K.ACTION_VALUE.RAISE):
        file_name = os.path.basename(file_path)
        try:
            answer = core.module.mods_index.load(file_path, mode, action)

        except Exception as e:
            msg = f"{file_name} 解析失败或序列化错误\n请检查 {self.__index_directory} 文件夹或将它移除"
            core.log.error(f"{file_name} 解析异常 {e.__class__} {e}")
            core.window.messagebox.showerror(title="编码错误", message=msg)
            return

        if answer is None: return None

        elif isinstance(answer, list):
            msg = f"{file_name} 数据产生交集\n是否仍然加载该文件"
            choice = core.window.messagebox.askyesno(title="数据产生交集", message=msg)

        else:
            msg = f"模组索引模块在加载 {file_name} 文件时返回了一个未定义的值\n程序可能发生了内部错误"
            core.log.error(f"模组索引模块在加载 {file_name} 文件时返回了一个未定义的值: {answer}")
            core.window.messagebox.showerror(title="内部错误", message=msg)
            raise Exception("内部错误")

        if choice:
            length = len(answer)
            msg = f"{file_name} 中共有 {length} 项 SHA 产生交集\n\n"

            if length > 4:
                msg += "\n".join(answer[:3])
                msg += "\n..."

            else:
                msg += "\n".join(answer)


            msg += "\n\n是否覆盖这些数据?"
            choice = core.window.messagebox.askyesno(title="数据产生交集", message=msg)

        else: return None
        if choice:
            return self.load_index_file(file_path, mode, K.ACTION_VALUE.COVER)

        else:
            return self.load_index_file(file_path, mode, K.ACTION_VALUE.SKIP)


    def load_all_index_file(self):
        for file_path in self.__json_index_file_list:
            self.load_index_file(file_path, "json")


    def save_all_index_file(self):
        for file_path in self.__json_index_file_list:
            core.module.mods_index.save_index_file(file_path)


    def auto_load_all_index_file(self):
        self.update_index_file_list()
        self.load_all_index_file()
