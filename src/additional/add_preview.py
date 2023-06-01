# -*- coding: utf-8 -*-

# std
import os

# project
import core



def add_preview(filepath: str):
    SHA = core.UI.ModsManage.sbin_get_select_choices()

    if SHA is None:
        object_ = core.UI.ModsManage.sbin_get_select_objects()
        SHA = core.Module.ModsManage.get_load_object_SHA(object_)

    if SHA is None:
        core.UI.Messagebox.showerror(title='未选中错误', message='需要先选中一个 Mod\n才能添加预览图')
        return

    item = core.Module.ModsIndex.get_item(SHA)
    object_ = item['object']
    name = item['name']

    answer = core.UI.Messagebox.askyesno(title='操作确认',message=(f'是否将图片设置为\n{SHA}\n{object_} :: {name}\n的预览图'))
    if not answer: return

    basename = os.path.basename(filepath)
    suffix = basename[basename.rfind('.'):]

    try:
        with open(filepath, 'rb') as fileobject:
            content = fileobject.read()
        with open(os.path.join(core.environment.resources.preview, f'{SHA}{suffix}'), 'wb') as fileobject:
            fileobject.write(content)
    except Exception:
        core.UI.Messagebox.showerror(title='操作失败', message='预览图设置失败\n未知错误')

    core.UI.ModsManage.sbin_update_preview(SHA)
