# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import tkinter.messagebox
import threading


OK = tkinter.messagebox.OK
CANCEL = tkinter.messagebox.CANCEL
YES = tkinter.messagebox.YES
NO = tkinter.messagebox.NO

class _ok(str): ...
class _yes(str): ...
class _no(str): ...


def is_main_thread() -> bool:
    """Returns True if the current thread is the main thread, False otherwise."""
    return threading.current_thread() is threading.main_thread()


class Messagebox(object):
    """A class that wraps the tkinter.messagebox module and provides asynchronous methods for non-main threads."""
    def __init__(self, windows):
        self.windows = windows

        from_ = ["showinfo", "showwarning", "showerror", "askquestion", "askokcancel", "askyesno", "askyesnocancel", "askretrycancel"]
        self.__modeslst = {x: getattr(tkinter.messagebox, x) for x in from_}


    def __async_msgbox(self, mode: str, **options) -> str | bool | None:
        """Shows a message box in an asynchronous way for non-main threads."""
        callobject = self.__modeslst[mode]
        event = threading.Event()
        answer = {}
        answer["answer"] = None

        _async_exec_ = lambda callobject, event, answer, kwds: (answer.update({"answer": callobject(**kwds)}), event.set())[-1]

        self.windows.after(0, _async_exec_, callobject, event, answer, options)
        event.wait()
        return answer["answer"]


    def __msgbox(self, mode: str,  **options) -> str | bool | None:
        """Shows a message box in a synchronous way for the main thread."""
        callobject = self.__modeslst[mode]
        return callobject(**options)


    def __allocation(self, mode: str, message: str, title: str = None, **options) -> str | bool | None:
        """Allocates the appropriate message box method based on the mode and the thread."""
        if mode not in self.__modeslst: return None
        if is_main_thread(): return self.__msgbox(mode=mode, title=title, message=message, **options)
        else: return self.__async_msgbox(mode=mode, title=title, message=message, **options)


    def showinfo(self, title: str = None, message: str = None, **options) -> _ok:
        """Shows an information message box with the given title and message."""
        return self.__allocation("showinfo", title=title, message=message, **options)

    def showwarning(self, title: str = None, message: str = None, **options) -> _ok:
        """Shows a warning message box with the given title and message."""
        return self.__allocation("showwarning", title=title, message=message, **options)

    def showerror(self, title: str = None, message: str = None, **options) -> _ok:
        """Shows an error message box with the given title and message."""
        return self.__allocation("showerror", title=title, message=message, **options)

    def askquestion(self, title: str = None, message: str = None, **options) -> _yes | _no:
        """Shows a question message box with the given title and message."""
        return self.__allocation("askquestion", title=title, message=message, **options)

    def askokcancel(self, title: str = None, message: str = None, **options) -> bool:
        """Shows an ok-cancel message box with the given title and message."""
        return self.__allocation("askokcancel", title=title, message=message, **options)

    def askyesno(self, title: str = None, message: str = None, **options) -> bool:
        """Shows a yes-no message box with the given title and message."""
        return self.__allocation("askyesno", title=title, message=message, **options)

    def askyesnocancel(self, title: str = None, message: str = None, **options) -> bool | None:
        """Shows a yes-no-cancel message box with the given title and message."""
        return self.__allocation("askyesnocancel", title=title, message=message, **options)

    def askretrycancel(self, title: str = None, message: str = None, **options) -> bool:
        """Shows a retry-cancel message box with the given title and message."""
        return self.__allocation("askretrycancel", title=title, message=message, **options)
