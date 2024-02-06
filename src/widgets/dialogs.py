
import core
import ttkbootstrap
from ttkbootstrap.constants import *

from .scrollframe import ScrollFrame



class SelectTags (object):
    def __init__(
            self,
            title: str = "",
            optional: str | list[str] | list[list[str]] = "",
            selected: str | list[str] = "",
            extracos: bool = True,
            *,
            window_width: int = 500,
            window_height: int = 400,
            parent: ttkbootstrap.Window = None
            ):
        """
        ## 标签选择器

        ```TEXT
        args:
            title: str 窗口标题
            optional: str | list[str] | list[list[str]] 选择器可选项，支持多行，每行支持多个标签
            selected: str | list[str] 选择器默认选中项，支持多选
            extracos: bool 是否允许额外添加标签
            window_width: int 窗口宽度, 不能小于 100，默认为 500
            window_height: int 窗口高度，不能小于 100，默认为 400
            parent: ttkbootstrap.Window 父窗口
        ```
        """
        self.title = title
        self.optional = optional
        self.selected = selected
        self.extracos = extracos
        self.window_width = 500 if not isinstance(window_width, int) or window_width < 100 else window_width
        self.window_height = 400 if not isinstance(window_height, int) or window_height < 100 else window_height
        self.parent = parent

        self._initial()
        self._initial_window()
        self._initial_widget()
        self._construct()


    def _initial(self):
        self.lst_optional = self._format_optional(self.optional)
        self.lst_selected = self._format_selected(self.selected)
        self.result: list[str] = self.lst_selected

        self.vtags: dict[str: ttkbootstrap.BooleanVar] = {}
        self.wtags: list[ttkbootstrap.Checkbutton] = []


    def _initial_window(self):
        self.window = ttkbootstrap.Toplevel()
        self.window.title(self.title)
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.focus_set()
        core.window.methods.center_window_for_window(self.window, self.parent, self.window_width, self.window_height, True)


    def _initial_widget(self):
        self.wsl_tags = ScrollFrame(self.window, scb_pad=2)
        self.wfe_option = ttkbootstrap.Frame(self.window)
        self.wet_extra = ttkbootstrap.Entry(self.window)
        self.wbn_sure = ttkbootstrap.Button(self.wfe_option, text="确定", width=10, bootstyle=(INFO, OUTLINE, TOOLBUTTON), command=self.bin_sure)
        self.wbn_cancel = ttkbootstrap.Button(self.wfe_option, text="取消", width=10, bootstyle=(WARNING, OUTLINE, TOOLBUTTON), command=self.bin_cancel)

        self.wsl_tags.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        if self.extracos: self.wet_extra.pack(side=TOP, fill=X, padx=5, pady=(0, 5))
        self.wfe_option.pack(side=TOP, fill=X, padx=5, pady=(0, 5))
        self.wbn_sure.pack(side=RIGHT)
        self.wbn_cancel.pack(side=RIGHT, padx=(0, 5))

    def _construct(self):
        for row, row_content in enumerate(self.lst_optional):
            pady = (0, 0) if row == 0 else (5, 0)

            _fe = ttkbootstrap.Frame(self.wsl_tags)
            _fe.pack(side=TOP, fill=X, pady=pady)

            for column, tag in enumerate(row_content):
                padx = (0, 0) if column == 0 else (5, 0)
                if tag not in self.vtags:
                    _v = ttkbootstrap.BooleanVar()
                    _v.set(True if tag in self.lst_selected else False)
                    self.vtags[tag] = _v
                else:
                    _v = self.vtags[tag]

                _w = ttkbootstrap.Checkbutton(_fe, text=tag, variable=_v, bootstyle=(SUCCESS, OUTLINE, TOOLBUTTON))
                _w.pack(side=LEFT, padx=padx)
                self.wtags.append(_w)

        _extra_lst = [tag for tag in self.lst_selected if tag not in self.vtags]
        self.wet_extra.delete(0, END)
        self.wet_extra.insert(0, " ".join(_extra_lst))


    def _format_optional(self, optional: str | list[str] | list[list[str]] = "") -> list[list[str]]:
        exception = TypeError("optional must be a string, list of strings, or list of lists of strings.")
        if not isinstance(optional, (str, list)):
            raise exception

        result = []
        lst_rows = optional.split("\n") if isinstance(optional, str) else optional

        for row in lst_rows:
            if not isinstance(row, (str, list)):
                raise exception

            try: row_content = row if isinstance(row, str) else " ".join(row)
            except Exception as _: raise exception

            lst_items = row_content.split(" ")
            lst = [item for item in lst_items if item]
            if not lst: continue
            result.append(lst)

        return result


    def _format_selected(self, selected: str | list[str]) -> list[str]:
        exception = TypeError("selected must be a string or list of strings.")
        if not isinstance(selected, (str, list)):
            raise exception

        try: content = selected if isinstance(selected, str) else " ".join(selected)
        except Exception as _: raise exception

        lst = [item.strip() for item in content.split(" ") if item]
        return lst


    def bin_sure(self, *_):
        self.result = [x for x in self.vtags if self.vtags[x].get()]
        if self.extracos: self.result.extend(self._format_selected(self.wet_extra.get()))
        self.window.destroy()


    def bin_cancel(self, *_):
        self.result = self.lst_selected
        self.window.destroy()


    def wait(self) -> list[str]:
        """
        ## 等待窗口关闭

        ```TEXT
        return: list[str] 返回已选择的标签
        ```
        """
        self.window.wait_window()
        return self.result



class TextEdit (object):
    def __init__(
            self,
            title: str = "",
            content: str = "",
            *,
            window_width: int = 500,
            window_height: int = 400,
            parent: ttkbootstrap.Window = None
            ):
        """
        ## 文本编辑器

        ```TEXT
        args:
            title: str 窗口标题
            content: str 编辑器初始内容
            window_width: int 编辑器宽度
            window_height: int 编辑器高度
            parent: ttkbootstrap.Window 父窗口
        ```
        """
        self.title = title
        self.content = content
        self.window_width = 500 if not isinstance(window_width, int) or window_width < 100 else window_width
        self.window_height = 400 if not isinstance(window_height, int) or window_height < 100 else window_height
        self.parent = parent

        self._initial()
        self._initial_window()
        self._initial_widget()
        self._construct()

    def _initial(self):
        self.result = self.content


    def _initial_window(self):
        self.window = ttkbootstrap.Toplevel()
        self.window.title(self.title)
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.focus_set()
        core.window.methods.center_window_for_window(self.window, self.parent, self.window_width, self.window_height, True)


    def _initial_widget(self):
        self.wtt = ttkbootstrap.Text(self.window, width=0, height=0)
        self.wfe_option = ttkbootstrap.Frame(self.window)
        self.wbn_sure = ttkbootstrap.Button(self.wfe_option, text="确定", width=10, bootstyle=(INFO, OUTLINE, TOOLBUTTON), command=self.bin_sure)
        self.wbn_cancel = ttkbootstrap.Button(self.wfe_option, text="取消", width=10, bootstyle=(WARNING, OUTLINE, TOOLBUTTON), command=self.bin_cancel)

        self.wtt.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.wfe_option.pack(side=TOP, fill=X, padx=5, pady=(0, 5))
        self.wbn_sure.pack(side=RIGHT)
        self.wbn_cancel.pack(side=RIGHT, padx=(0, 5))


    def _construct(self):
        self.wtt.insert(0.0, self.content)


    def bin_sure(self, *_):
        self.result = self.wtt.get(0.0, END)
        self.window.destroy()


    def bin_cancel(self, *_):
        self.result = self.content
        self.window.destroy()


    def wait(self) -> list[str]:
        self.window.wait_window()
        return self.result



def select2ags (
        title: str = "",
        optional: str | list[str] | list[list[str]] = "",
        selected: str | list[str] = "",
        extracos: bool = True,
        *,
        window_width: int = 500,
        window_height: int = 400,
        parent: ttkbootstrap.Window = None
        ) -> list[str]:
    """
    ## 标签选择器

    ```TEXT
    args:
        title: str 窗口标题
        optional: str | list[str] | list[list[str]] 选择器可选项，支持多行，每行支持多个标签
        selected: str | list[str] 选择器默认选中项，支持多选
        extracos: bool 是否允许额外添加标签
        window_width: int 窗口宽度, 不能小于 100，默认为 500
        window_height: int 窗口高度，不能小于 100，默认为 400
        parent: ttkbootstrap.Window 父窗口

    return:
        list[str] 返回已选择的标签
        若点击了取消则返回 selected 的内容
    ```
    """
    kwargs = locals()
    kernel = SelectTags(**kwargs)
    result = kernel.wait()
    return result


def textedit(
        title: str = "",
        content: str = "",
        *,
        window_width: int = 500,
        window_height: int = 400,
        parent: ttkbootstrap.Window = None
        ) -> str:
    """
    ## 文本编辑器

    ```TEXT
    args:
        title: str 窗口标题
        content: str 编辑器初始内容
        window_width: int 编辑器宽度
        window_height: int 编辑器高度
        parent: ttkbootstrap.Window 父窗口

    return:
        str 返回编辑器内容
        若点击了取消则返回 content 的内容
    ```
    """
    kwargs = locals()
    kernel = TextEdit(**kwargs)
    result = kernel.wait()
    return result
