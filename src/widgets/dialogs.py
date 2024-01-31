
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
            parent: ttkbootstrap.Window = None
            ):

        self.title = title
        self.optional = optional
        self.selected = selected
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
        core.window.methods.center_window_for_window(self.window, self.parent, 500, 400, True)


    def _initial_widget(self):
        self.wsl_tags = ScrollFrame(self.window, scb_pad=2)
        self.wfe_option = ttkbootstrap.Frame(self.window)
        self.wet_extra = ttkbootstrap.Entry(self.window)
        self.wbn_sure = ttkbootstrap.Button(self.wfe_option, text="确定", width=10, bootstyle=(INFO, OUTLINE, TOOLBUTTON), command=self.bin_sure)
        self.wbn_cancel = ttkbootstrap.Button(self.wfe_option, text="取消", width=10, bootstyle=(WARNING, OUTLINE, TOOLBUTTON), command=self.bin_cancel)

        self.wsl_tags.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.wet_extra.pack(side=TOP, fill=X, padx=5, pady=(0, 5))
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
        self.result.extend(self._format_selected(self.wet_extra.get()))
        self.window.destroy()


    def bin_cancel(self, *_):
        self.result = self.lst_selected
        self.window.destroy()


    def wait(self) -> list[str]:
        self.window.wait_window()
        return self.result



class TextEdit (object):
    def __init__(
            self,
            title: str = "",
            content: str = "",
            width: int = ...,
            height: int = ...,
            parent: ttkbootstrap.Window = None
            ):

        self.title = title
        self.content = content
        self.width = width if isinstance(width, int) else 500
        self.height = height if isinstance(height, int) else 400
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
        core.window.methods.center_window_for_window(self.window, self.parent, self.width, self.height, True)


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
        parent: ttkbootstrap.Window = None
        ) -> list[str]:

    conobj = SelectTags(title=title, optional=optional, selected=selected, parent=parent)
    result = conobj.wait()
    return result


def textedit(
        title: str = "",
        content: str = "",
        width: int = ...,
        height: int = ...,
        parent: ttkbootstrap.Window = None
        ) -> str:
    
    conobj = TextEdit(title=title, content=content, width=width, height=height, parent=parent)
    result = conobj.wait()
    return result
