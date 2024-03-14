# std
import types
import typing
import tkinter
import threading


class settings (object):
    tk_mainwindow: tkinter.Misc = None
    tk_after_ms: int = 0



class tkasyncmain (object):
    def __init__(self, func: types.FunctionType) -> None:
        self.func = func
        self.args = ()
        self.kwds = {}

        self.code = 0
        self.result = None
        self.asynccall = threading.Event()


    def asynccallable(self, *_) -> typing.NoReturn:
        try:
            self.result = self.func(*self.args, **self.kwds)

        except BaseException as e:
            self.code = 1
            self.result = e

        self.asynccall.set()


    def agent(self, *args, **kwargs) -> typing.Any:
        if settings.tk_mainwindow is None:
            return self.func(*args, **kwargs)
            # No need to assert, just let it execute the original function.
            assert False, "tkinter main window object not set."

        if threading.main_thread() is threading.current_thread():
            return self.func(*args, **kwargs)

        self.args = args
        self.kwds = kwargs

        settings.tk_mainwindow.after(settings.tk_after_ms, self.asynccallable)
        self.asynccall.wait()
        self.asynccall.clear()

        if self.code == 0:
            return self.result

        else:
            raise self.result


    __call__ = agent



__all__ = [
    "tkasyncmain"
]
