# -*- coding: utf-8 -*-

import os

import PIL.Image
import PIL.ImageTk
# import PIL.ImageDraw

from typing import Union

import core


def image_resize(image_: Union[PIL.Image.Image, str], width: int, height: int, tkimg: bool = False) -> PIL.Image.Image:
    """调整图片大小, 保持原图片比例"""
    if isinstance(image_, PIL.Image.Image): picture = image_
    elif isinstance(image_, str): picture = PIL.Image.open(image_)
    else: raise TypeError("The image_ type is not Image or str.")

    raw_width, raw_height = picture.size[0], picture.size[1]
    max_width, max_height = raw_width, height        
    min_width = max(raw_width, max_width)

    min_height = int(raw_height * min_width / raw_width)
    while min_height > height: min_height = int(min_height * .9533)
    while min_height < height: min_height += 1
    min_width = int(raw_width * min_height / raw_height)
    while min_width > width: min_width -= 1
    min_height = int(raw_height * min_width / raw_width)

    result = picture.resize((min_width, min_height))
    if tkimg: return PIL.ImageTk.PhotoImage(result)
    else: return result


def image_canvas(image_: Union[PIL.Image.Image, str], width: int, height: int, tkimg: bool = False) -> PIL.Image.Image:
    """调整图片大小, 使用指定比例, 透明背景"""
    if isinstance(image_, PIL.Image.Image): picture = image_
    elif isinstance(image_, str): picture = PIL.Image.open(image_)
    else: raise TypeError("The image_ type is not Image or str.")

    background = PIL.Image.new('RGBA', (width, height), "#00000000")
    picture = image_resize(picture, width, height)
    bx, by = background.size; ix, iy = picture.size
    ox = (bx - ix) // 2; oy = (by - iy) // 2
    background.paste(picture, (ox, oy))

    if tkimg: return PIL.ImageTk.PhotoImage(background)
    else: return background



def get_preview_image(SHA: str | None, width: int, height: int):
        if SHA is None:
            return PIL.ImageTk.PhotoImage(PIL.Image.new('RGBA', (width, height), "#00000000"))

        for suffix in ['.png', '.jpg']:
            target = os.path.join(core.environment.resources.preview, f'{SHA}{suffix}')
            if os.path.isfile(target):
                return core.module.image.image_resize(target, width, height, tkimg=True)

        for suffix in ['.png', '.jpg']:
            target = os.path.join(core.environment.user.loadMods, SHA, f'preview{suffix}')
            if os.path.isfile(target):
                with open(target, 'rb') as fileobject:
                    with open(os.path.join(core.environment.resources.preview, f'{SHA}{suffix}'), 'wb') as tofileobject:
                        tofileobject.write(fileobject.read())

                return core.module.image.image_resize(target, width, height, tkimg=True)

        return None
        return PIL.ImageTk.PhotoImage(PIL.Image.new('RGBA', (width, height), "#00000000"))


class ImageTkThumbnailGroup(object):
    """Tk 图像 - 缩略图容器

    *注意: 这个对象的方法不是线程安全的
    """
    def __init__(self, width: int = 16, height: int = 16):
        self.__table = {}
        self.setSize(width, height)
        self.__none = PIL.ImageTk.PhotoImage(PIL.Image.new('RGBA', (width, height), "#00000000"))


    def setSize(self, width: int, height: int) -> None:
        """设置预览图大小

        影响图片的大小和比例

        *注意: 你必须谨慎使用这个方法, 它会导致原有的图像失真 (不, 它现在会舍弃原有的图像)
        """
        if not isinstance(width, int): raise TypeError("The width type is not int.")
        if not isinstance(height, int): raise TypeError("The height type is not int.")

        if width < 10: raise ValueError("The width should not be less than 10.")
        if height < 10: raise ValueError("The height should not be less than 10.")

        self._width = width
        self._height = height

        self.__table = {}
        return

        newTable = {}
        for name, item in self.__table.items():
            newTable[name] = image_canvas(item, self._width, self._height)

        self.__table = newTable


    def add_image(self, image_: Union[PIL.Image.Image, str], name_: str = ...) -> None:
        if isinstance(image_, PIL.Image.Image):
            if name_ is Ellipsis:
                raise ValueError("name_ must be provided when image_ is an Image object.")

        if isinstance(image_, str):
            if not os.path.isfile(image_):
                raise FileNotFoundError("File path not found.")

            filename = os.path.basename(image_)

            if name_ is Ellipsis:
                name_ = filename[:filename.rfind('.')]

        if not isinstance(name_, str):
            raise TypeError("The name_ type is not str.")

        img = image_canvas(image_, self._width, self._height, tkimg=True)
        self.__table[name_] = img


    def add_image_from_dirs(self, path: str) -> None:
        if not isinstance(path, str):
            raise TypeError("The path type is not str.")

        if not os.path.isdir(path):
            raise FileNotFoundError("FileNotFoundError ac .")

        filenamelst = os.listdir(path)

        for filename in filenamelst:
            filepath = os.path.join(path, filename)
            if not os.path.isfile(filepath): continue
            try: self.add_image(filepath)
            except Exception: ...


    def add_image_from_redirectionConfigFile(self, path: str) -> None:
        if not isinstance(path, str):
            raise TypeError("The path type is not str.")

        if not os.path.isfile(path):
            raise FileNotFoundError("FileNotFoundError as .")

        with open(path, 'r', encoding='utf-8') as fileobject: contentlst = fileobject.readlines()
        statementlst = [x.strip() for x in contentlst if x.strip()]
        filedirname = os.path.dirname(path)

        for statement in statementlst:
            if '=' in statement:
                try:
                    index = statement.find('=')
                    name = statement[:index].strip()
                    filename = statement[index + 1:].strip()
                    filepath = os.path.join(filedirname, filename)

                    self.add_image(filepath, name)

                except:
                    ...

            elif len(statement) >= 7 and statement[:4] == '[*] ' and statement[-2:] == '\*':
                dirname = statement[4:-2]
                dirpath = os.path.join(filedirname, dirname)
                try:
                    self.add_image_from_dirs(dirpath)

                except Exception:
                    ...


    def get(self, name: str) -> PIL.ImageTk.PhotoImage:
        return self.__table.get(name, self.__none)

