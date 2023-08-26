# -*- coding: utf-8 -*-

# std
import io
import os
import time
import threading

# install
import win32gui
import ttkbootstrap
from PIL import Image, ImageGrab

# project
import core


class AddPreview (object):
    def __init__(self, SHA, filepath):
        with open(filepath, 'rb') as f: self.content = f.read()

        self.basename = os.path.basename(filepath)
        self.suffix = self.basename[self.basename.rfind('.'):]

        self.SHA = SHA

        item = core.module.mods_index.get_item(SHA)
        object_ = item['object']
        name = item['name']

        self.windows = ttkbootstrap.Toplevel('操作确认')
        self.windows.attributes("-topmost", True)
        self.windows.transient(core.window.mainwindow)
        # self.windows.grab_set()

        try:
            self.windows.iconbitmap(default=core.env.file.local.iconbitmap)
            self.windows.iconbitmap(bitmap=core.env.file.local.iconbitmap)
        except Exception:
            ...

        text = f'SHA :: {SHA}\n{object_} :: {name}\n\n你希望将图片设置为\n\n' +\
                '　　预览图：在窗口右侧显示\n全屏预览图：点击预览图后全屏显示\n'

        self.Label = ttkbootstrap.Label(self.windows, text=text)
        self.Label.pack(side='top', padx=10, pady=10)

        self.Button_surface = ttkbootstrap.Button(self.windows, text='预览图', width=10, bootstyle='success-outline', command=self.bin_to_surface)
        self.Button_inside = ttkbootstrap.Button(self.windows, text='全屏预览图', width=10, bootstyle='info-outline', command=self.bin_to_inside)

        self.Button_inside.pack(side='left', fill='x', expand=True, padx=10, pady=(0, 10))
        self.Button_surface.pack(side='left', fill='x', expand=True, padx=(0, 10), pady=(0, 10))

        self.windows.update()

        width = self.windows.winfo_width()
        height = self.windows.winfo_height()

        _x, _y = win32gui.GetCursorInfo()[2]

        x = _x - width // 2
        y = _y - height // 2 - 20

        if x < 0: x = 0
        if y < 0: y = 0

        self.windows.geometry(f'+{x}+{y}')
        self.windows.resizable(False, False)
        # self.bin_to_surface()

    def bin_to_surface(self, *args):
        if not os.path.isdir(core.env.directory.resources.preview): os.mkdir(core.env.directory.resources.preview)
        with open(os.path.join(core.env.directory.resources.preview, f'{self.SHA}{self.suffix}'), 'wb') as fileobject:
            fileobject.write(self.content)
        # core.UI.ModsManage.sbin_update_preview(self.SHA)
        core.window.interface.mods_manage.sbin_update_preview()
        self.windows.destroy()


    def bin_to_inside(self, *args):
        if not os.path.isdir(core.env.directory.resources.preview_screen): os.mkdir(core.env.directory.resources.preview_screen)
        with open(os.path.join(core.env.directory.resources.preview_screen, f'{self.SHA}{self.suffix}'), 'wb') as fileobject:
            fileobject.write(self.content)
        self.windows.destroy()


def add_preview(filepath: str):
    SHA = core.window.interface.mods_manage.sbin_get_select_choices()

    if SHA is None:
        object_ = core.window.interface.mods_manage.sbin_get_select_objects()
        SHA = core.module.mods_manage.get_load_object_sha(object_)

    if SHA is None:
        core.window.messagebox.showerror(title='未选中错误', message='需要先选中一个 Mod\n才能添加预览图')
        return

    threading.Thread(None, AddPreview, 'Add-Preview', (SHA, filepath), daemon=True).start()
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


def add_preview_from_clipboard(*_):
    image = ImageGrab.grabclipboard()

    tempfilename = hex(int(time.time() * 10 ** 8)) + '.png'
    path = os.path.join(core.env.directory.resources.cache, tempfilename)
    if isinstance(image, Image.Image):
        image.save(path)
        add_preview(path)
