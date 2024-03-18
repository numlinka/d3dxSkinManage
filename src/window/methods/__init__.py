# Licensed under the GPL 3.0 License.
# d3dxSkinManage by numlinka.

# site
import ttkbootstrap

# self
from . import motion


def center_window_for_window(window: ttkbootstrap.Toplevel, target_window: ttkbootstrap.Window, window_width: int = ..., window_height: int = ..., set_window_size: bool = False):
    target_window_x = target_window.winfo_x()
    target_window_y = target_window.winfo_y()
    target_window_width = target_window.winfo_width()
    target_window_height = target_window.winfo_height()
    target_window_center_x = target_window_x + target_window_width // 2
    target_window_center_y = target_window_y + target_window_height // 2

    window_width = window.winfo_width() if window_width is Ellipsis else window_width
    window_height = window.winfo_height() if window_height is Ellipsis else window_height
    window_x = target_window_center_x - window_width // 2
    window_y = target_window_center_y - window_height // 2
    result = f"{window_width}x{window_height}+{window_x}+{window_y}" if set_window_size else f"+{window_x}+{window_y}"
    window.geometry(result)


def fake_withdraw(window: ttkbootstrap.Toplevel):
    window.geometry("+32000+32000")


__all__ = ["motion", center_window_for_window]
