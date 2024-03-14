
# std
import os
import shutil
import threading

# site
import ttkbootstrap

# libs
import core
from constant import *



class containe ():
    action = threading.Lock()
    operation = threading.Lock()



class CountItemFrame (ttkbootstrap.Frame):
    def __init__(self, *args, **kwds) -> None:
        super().__init__(*args, **kwds)

        self.frame_prefix = ttkbootstrap.Frame(self)
        self.frame_suffix = ttkbootstrap.Frame(self)
        self.frame_counts = ttkbootstrap.Frame(self)

        self.label_prefix_file = ttkbootstrap.Label(self.frame_prefix, text="项目数量:")
        self.label_prefix_size = ttkbootstrap.Label(self.frame_prefix, text="占用空间:")

        self.label_suffix_file = ttkbootstrap.Label(self.frame_suffix, text="Items")
        self.label_suffix_size = ttkbootstrap.Label(self.frame_suffix, text="MiBytes")

        self.label_counts_file = ttkbootstrap.Label(self.frame_counts, text="-", anchor="e", width=32)
        self.label_counts_size = ttkbootstrap.Label(self.frame_counts, text="-", anchor="e", width=32)

        self.frame_prefix.pack(side="left", fill="y", padx=10, pady=10)
        self.frame_suffix.pack(side="right", fill="y", padx=10, pady=10)
        self.frame_counts.pack(side="top", fill="x", pady=10)

        self.label_prefix_file.pack(side="top", fill="x")
        self.label_prefix_size.pack(side="top", fill="x")

        self.label_suffix_file.pack(side="top", fill="x")
        self.label_suffix_size.pack(side="top", fill="x")

        self.label_counts_file.pack(side="top", fill="x")
        self.label_counts_size.pack(side="top", fill="x")


    def sbin_update(self, file_count: int = 0, size_count: int = 0):
        self.sbin_update_file(file_count)
        self.sbin_update_size(size_count)


    def sbin_update_file(self, count: int = 0):
        self.label_counts_file.config(text=f"{count}")


    def sbin_update_size(self, count: int = 0):
        value = count / 1024 / 1024
        self.label_counts_size.config(text=f"{value:.2f}")


    def sbin_clean(self):
        self.label_counts_file.config(text=f"-")
        self.label_counts_size.config(text=f"-")



class CacheCleanup (object):
    def __init__(self):
        result = containe.action.acquire(timeout=0.01)
        if not result:
            core.window.messagebox.showerror(title="操作已被阻止", message="请勿重复启动该工具")
            return

        self.window = ttkbootstrap.Toplevel()
        self.window.title("缓存清理工具")
        self.window.resizable(width=False, height=False)
        # self.window.geometry(f"500x300")
        self.window.protocol('WM_DELETE_WINDOW', self.bin_close)

        try:
            self.window.iconbitmap(default=core.env.file.local.iconbitmap)
            self.window.iconbitmap(bitmap=core.env.file.local.iconbitmap)
        except Exception:
            ...

        self.value_invalid_count_files = 0
        self.value_invalid_count_bytes = 0
        self.value_invalid_direc_lists = []

        self.value_rarely_count_files = 0
        self.value_rarely_count_bytes = 0
        self.value_rarely_direc_lists = []

        self.value_often_count_files = 0
        self.value_often_count_bytes = 0
        self.value_often_direc_lists = []

        self.labelframe_invalid = ttkbootstrap.LabelFrame(self.window, text="无效缓存")
        self.labelframe_rarely = ttkbootstrap.LabelFrame(self.window, text="不常用缓存")
        self.labelframe_often = ttkbootstrap.LabelFrame(self.window, text="常用缓存")
        self.frame_option = ttkbootstrap.Frame(self.window)

        self.labelframe_invalid.pack(side="top", fill="x", padx=10, pady=10)
        self.labelframe_rarely.pack(side="top", fill="x", padx=10, pady=(0, 10))
        self.labelframe_often.pack(side="top", fill="x", padx=10, pady=(0, 10))
        self.frame_option.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

        self.button_invalid_clean = ttkbootstrap.Button(self.labelframe_invalid, text="清理", width=10, bootstyle="success-outline", cursor="hand2")
        self.countitem_invalid = CountItemFrame(self.labelframe_invalid)
        self.button_invalid_clean.pack(side="right", padx=10)
        self.countitem_invalid.pack(side="left", fill="x", expand=True)

        self.button_rarely_clean = ttkbootstrap.Button(self.labelframe_rarely, text="清理", width=10, bootstyle="warning-outline", cursor="hand2")
        self.countitem_rarely = CountItemFrame(self.labelframe_rarely)
        self.button_rarely_clean.pack(side="right", padx=10)
        self.countitem_rarely.pack(side="left", fill="x", expand=True)

        self.button_often_clean = ttkbootstrap.Button(self.labelframe_often, text="清理", width=10, bootstyle="danger-outline", cursor="hand2")
        self.countitem_often = CountItemFrame(self.labelframe_often)
        self.button_often_clean.pack(side="right", padx=10)
        self.countitem_often.pack(side="left", fill="x", expand=True)

        self.button_scan = ttkbootstrap.Button(self.frame_option, text="重新扫描缓存文件", width=30, bootstyle="info-outline", cursor="hand2")
        self.button_scan.pack(side="right")

        self.button_invalid_clean.config(command=lambda *_: core.construct.taskpool.addtask(self.bin_clean_invalid))
        self.button_rarely_clean.config(command=lambda *_: core.construct.taskpool.addtask(self.bin_clean_rarely))
        self.button_often_clean.config(command=lambda *_: core.construct.taskpool.addtask(self.bin_clean_often))

        self.button_scan.config(command=lambda *_: core.construct.taskpool.addtask(self.bin_scan))


        self.window.update_idletasks()
        # width = self.window.winfo_reqwidth()
        # height = self.window.winfo_reqheight()

        # screen_width = self.window.winfo_screenwidth()
        # screen_height = self.window.winfo_screenheight()

        # x_coordinate = (screen_width - width) // 2
        # y_coordinate = (screen_height - height) // 2

        # self.window.geometry(f"+{x_coordinate}+{y_coordinate}")
        core.window.methods.center_window_for_window(self.window, core.window.mainwindow)

        core.construct.taskpool.addtask(self.bin_scan)


    def sbin_get_operation_lock(self, *_):
        result = containe.operation.acquire(timeout=0.01)
        if not result:
            core.window.messagebox.showerror(title="互斥动作", message="操作锁请求超时\n请等待其他操作完成", parent=self.window)

        return result


    def sbin_update_invalid(self, reset: bool = False):
        if reset:
            self.countitem_invalid.sbin_clean()

        else:
            self.countitem_invalid.sbin_update(self.value_invalid_count_files, self.value_invalid_count_bytes)


    def sbin_update_rarely(self, reset: bool = False):
        if reset:
            self.countitem_rarely.sbin_clean()

        else:
            self.countitem_rarely.sbin_update(self.value_rarely_count_files, self.value_rarely_count_bytes)


    def sbin_update_often(self, reset: bool = False):
        if reset:
            self.countitem_often.sbin_clean()

        else:
            self.countitem_often.sbin_update(self.value_often_count_files, self.value_often_count_bytes)


    def bin_close(self, *_):
        if not self.sbin_get_operation_lock():
            return

        self.window.destroy()
        containe.action.release()
        containe.operation.release()


    def bin_scan(self, *_):
        if not self.sbin_get_operation_lock():
            return

        try:
            all_sha_list = core.module.mods_index.get_all_sha_list()
            self.value_invalid_count_files = 0
            self.value_invalid_count_bytes = 0
            self.value_invalid_direc_lists = []

            self.value_rarely_count_files = 0
            self.value_rarely_count_bytes = 0
            self.value_rarely_direc_lists = []

            self.value_often_count_files = 0
            self.value_often_count_bytes = 0
            self.value_often_direc_lists = []

            for dirname in os.listdir(core.userenv.directory.work_mods):
                if not os.path.isdir(os.path.join(core.userenv.directory.work_mods, dirname)):
                    continue

                if dirname.upper().startswith(f"{K.DISABLED_UPPER}-"):
                    length = len(K.DISABLED_UPPER)+1
                    SHA = dirname[length:length+40]

                elif dirname.upper().startswith(f"{K.DISABLED_UPPER}"):
                    length = len(K.DISABLED_UPPER)
                    SHA = dirname[length:length+40]

                else:
                    continue

                dir_path = os.path.join(core.userenv.directory.work_mods, dirname)

                # 若为本地 SHA 则为常用缓存
                if core.module.mods_manage.is_local_sha(SHA):
                    self.value_often_count_files += 1
                    self.value_often_direc_lists += [dir_path]
                    self.value_often_count_bytes += get_folder_size(dir_path)
                    self.sbin_update_often()

                # 若只存在于 SHA 表中则为不常用缓存
                elif SHA in all_sha_list:
                    self.value_rarely_count_files += 1
                    self.value_rarely_direc_lists += [dir_path]
                    self.value_rarely_count_bytes += get_folder_size(dir_path)
                    self.sbin_update_rarely()

                # 若均不存在则为无效缓存
                else:
                    self.value_invalid_count_files += 1
                    self.value_invalid_direc_lists += [dir_path]
                    self.value_invalid_count_bytes += get_folder_size(dir_path)
                    self.sbin_update_invalid()

        except:
            ...

        finally:
            containe.operation.release()


    def bin_clean_invalid(self, *_):
        if not self.sbin_get_operation_lock():
            return

        for _ in range(self.value_invalid_count_files):
            try:
                dir_path = self.value_invalid_direc_lists.pop(0)

                self.value_invalid_count_files -= 1
                self.value_invalid_count_bytes -= get_folder_size(dir_path)

                shutil.rmtree(dir_path)

            except Exception as e:
                print(e)

            finally:
                self.sbin_update_invalid()

        containe.operation.release()
        self.sbin_update_invalid(True)


    def bin_clean_rarely(self, *_):
        if not self.sbin_get_operation_lock():
            return

        for _ in range(self.value_rarely_count_files):
            try:
                dir_path = self.value_rarely_direc_lists.pop(0)

                self.value_rarely_count_files -= 1
                self.value_rarely_count_bytes -= get_folder_size(dir_path)

                shutil.rmtree(dir_path)

            except Exception as e:
                print(e)

            finally:
                self.sbin_update_rarely()

        containe.operation.release()
        self.sbin_update_rarely(True)


    def bin_clean_often(self, *_):
        if not self.sbin_get_operation_lock():
            return

        for _ in range(self.value_often_count_files):
            try:
                dir_path = self.value_often_direc_lists.pop(0)

                self.value_often_count_files -= 1
                self.value_often_count_bytes -= get_folder_size(dir_path)

                shutil.rmtree(dir_path)

            except Exception as e:
                print(e)

            finally:
                self.sbin_update_often()

        containe.operation.release()
        self.sbin_update_often(True)


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size
