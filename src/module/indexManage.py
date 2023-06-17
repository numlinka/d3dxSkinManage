# -*- coding: utf-8 -*-

import os

import core



class IndexManage(object):
    def __init__(self):
        self.exec_index_file_list = []
        self.json_index_file_list = []
        self.dirModsIndex = ''


    def update(self):
        self.dirModsIndex = core.environment.user.modsIndex
        self.exec_index_file_list = []
        self.json_index_file_list = []


    def update_index_file_list(self):
        lst = [x for x in os.listdir(self.dirModsIndex) if os.path.isfile(os.path.join(self.dirModsIndex, x))]
        for name in lst:
            if len(name) >= 6 and name[-5:] == '.json':
                self.json_index_file_list.append(name)

            elif len(name) >= 7 and name[-6:] == '.stone':
                self.exec_index_file_list.append(name)

            else:
                msg = f"{name} 不是有效文件后缀名或不被支持\n请检查 {self.dirModsIndex} 文件夹或将它移除"
                core.Log.warn(f"{name} 不是有效文件后缀名")
                core.UI.Messagebox.showwarning(title="意外的模组索引文件", message=msg)


    def load_file(self, filename: str, mode: str, action: str = 'raise'):
        filepath = os.path.join(self.dirModsIndex, filename)
        try:
            answer = core.Module.ModsIndex.load(filepath, mode, action)

        except Exception as e:
            print(e.__class__, e)
            msg = f"{filename} 解析失败或序列化错误\n请检查 {self.dirModsIndex} 文件夹或将它移除"
            core.Log.error(f"{filename} 解析异常 {e.__class__} {e}")
            core.UI.Messagebox.showerror(title="编码错误", message=msg)

        if answer is None: return None

        elif isinstance(answer, list):
            msg = f"{filename} 数据产生交集\n是否仍然加载该文件"
            choice = core.UI.Messagebox.askyesno(title="数据产生交集", message=msg)

        else:
            msg = f"模组索引模块在加载 {filename} 文件时返回了一个未定义的值\n程序可能发生了内部错误"
            core.Log.error(f"模组索引模块在加载 {filename} 文件时返回了一个未定义的值: {answer}")
            core.UI.Messagebox.showerror(title="内部错误", message=msg)
            raise Exception("内部错误")

        if choice:
            length = len(answer)
            msg = f"{filename} 中共有 {length} 项 SHA 产生交集\n\n"

            if length > 4:
                msg += '\n'.join(answer[:3])
                msg += '\n...'

            else:
                msg += '\n'.join(answer)


            msg += "\n\n是否覆盖这些数据?"
            choice = core.UI.Messagebox.askyesno(title="数据产生交集", message=msg)

        else: return None
        if choice:
            return self.load_file(filename, mode, 'cover')
        else:
            return self.load_file(filename, mode, 'skip')


    def first_load(self):
        self.update_index_file_list()
        for filename in self.exec_index_file_list:
            answer = self.load_file(filename, 'npy')
            if answer is not None: return answer

        for filename in self.json_index_file_list:
            answer = self.load_file(filename, 'json')
            if answer is not None: return answer

