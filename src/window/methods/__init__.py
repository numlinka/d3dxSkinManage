# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import ctypes
from ctypes import wintypes

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


def get_screen_coordinates() -> list[tuple[tuple[int, int]]]:
    user32 = ctypes.windll.user32
    
    class MONITORINFOEX(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("rcMonitor", wintypes.RECT),
            ("rcWork", wintypes.RECT),
            ("dwFlags", wintypes.DWORD),
            ("szDevice", ctypes.c_wchar * 32)
        ]

    MonitorEnumProc = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        ctypes.POINTER(wintypes.HMONITOR),
        ctypes.POINTER(wintypes.HDC),
        ctypes.POINTER(wintypes.RECT),
        ctypes.POINTER(ctypes.c_void_p)
    )

    def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        mi = MONITORINFOEX()
        mi.cbSize = ctypes.sizeof(MONITORINFOEX)
        user32.GetMonitorInfoW(hMonitor, ctypes.byref(mi))
        left_top = (mi.rcMonitor.left, mi.rcMonitor.top)
        right_bottom = (mi.rcMonitor.right, mi.rcMonitor.bottom)
        screens.append((left_top, right_bottom))
        return 1

    screens = []
    user32.EnumDisplayMonitors(
        None, None, MonitorEnumProc(monitor_enum_proc), None
    )
    return screens


__all__ = ["motion", center_window_for_window]
