# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import os
import time
import hashlib
import threading

# site
import ttkbootstrap

# local
import core
from constant import *


class containe ():
    action = threading.Lock()

    mods_path: str
    item_list: list

    status_running = False
    stop = False



class OldMigration(object):
    def __init__ (self):
        result = containe.action.acquire(timeout=0.01)
        if not result:
            core.window.messagebox.showerror(title="操作已被阻止", message="请勿重复启动该工具")
            return

        containe.status_running = False
        containe.stop = False

        self.window = ttkbootstrap.Toplevel()
        core.window.methods.fake_withdraw(self.window)
        self.window.title("数据迁移工具")
        self.window.resizable(width=False, height=False)
        self.window.transient(core.window.mainwindow)
        self.window.grab_set()

        try:
            self.window.iconbitmap(default=core.env.file.local.iconbitmap)
            self.window.iconbitmap(bitmap=core.env.file.local.iconbitmap)
        except Exception:
            ...

        self.window.protocol('WM_DELETE_WINDOW', self.bin_close)

        self.frame_choice = ttkbootstrap.Frame(self.window)
        self.frame_inquire = ttkbootstrap.Frame(self.window)
        self.frame_execute = ttkbootstrap.Frame(self.window)
        self.frame_complete = ttkbootstrap.Frame(self.window)

        Tcl.window = self.window
        Tcl.main = self
        Tcl.choice = Choice(self.frame_choice)
        Tcl.inquire = ScanInquire(self.frame_inquire)
        Tcl.execute = Execute(self.frame_execute)
        Tcl.eomplete = Eomplete(self.frame_complete)

        core.window.methods.center_window_for_window(self.window, core.window.mainwindow, 500, 300, True)

        # width = self.window.winfo_reqwidth()
        # height = self.window.winfo_reqheight()
        # width = 500
        # height = 300

        # screen_width = self.window.winfo_screenwidth()
        # screen_height = self.window.winfo_screenheight()

        # x_coordinate = (screen_width - width) // 2
        # y_coordinate = (screen_height - height) // 2

        # self.window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

        self.frame_choice.pack(fill="both", expand=True)
        # core.window.mainwindow.withdraw()


    def sbin_entry_scan(self):
        self.frame_choice.pack_forget()
        self.frame_inquire.pack(fill="both", expand=True)
        core.construct.taskpool.addtask(Tcl.inquire.sbin_start_scan, answer=False)


    def sbin_entry_execute(self):
        self.frame_inquire.pack_forget()
        self.frame_execute.pack(fill="both", expand=True)
        Tcl.execute.sbin_start()


    def sbin_entry_eomplete(self):
        self.frame_execute.pack_forget()
        self.frame_complete.pack(fill="both", expand=True)


    def bin_close(self, *_):
        if containe.status_running:
            if core.window.messagebox.askyesno(title="人物中断", message="迁移工作正在进行，是否终止?"):
                containe.stop = True

            else:
                return

        containe.action.release()
        self.window.destroy()
        # core.window.mainwindow.deiconify()



class Choice (object):
    TEXT = (
        "输入 3DMiModsManage 的 Mods 文件夹路径\n"
        "仅支持 3DMiModsManage Type-C 版本\n\n"
        "迁移工具执行期间会频繁请求操作锁\n"
        "为避免其他操作争夺锁 d3dxSkinManage 暂时不可用\n"
    )
    def __init__(self, master):
        self.master = master

        self.label = ttkbootstrap.Label(self.master, text=self.TEXT)
        self.label.pack(side="top", fill="x", padx=10, pady=10)

        self.entry = ttkbootstrap.Entry(self.master)
        self.entry.pack(side="top", fill="x", padx=10)

        self.frame_option = ttkbootstrap.Frame(self.master)
        self.frame_option.pack(side="bottom", fill="x")
        self.button_next = ttkbootstrap.Button(self.frame_option, text="下一步", command=self.bin_next)
        self.button_next.pack(side="right", padx=10, pady=10)


    def bin_next(self, *_):
        path = self.entry.get()
        if not path:
            core.window.messagebox.showerror(title="数据错误", message="目标路径为空或未填写", parent=Tcl.window)
            return

        if not os.path.isdir(path):
            core.window.messagebox.showerror(title="数据错误", message="目标路径不存在或不为文件夹", parent=Tcl.window)
            return
        
        if os.path.basename(path) != "Mods":
            core.window.messagebox.showerror(title="数据错误", message="文件夹名称不是 Mods", parent=Tcl.window)
            return

        containe.mods_path = path
        Tcl.main.sbin_entry_scan()



class ScanInquire (object):
    def __init__(self, master):
        self.master = master

        self.status_scan_complete = False
        self.status_size = 0

        self.label = ttkbootstrap.Label(self.master, text="项目数量: \n占用空间: \n")
        self.label.pack(side="top", fill="x", padx=10, pady=10)


        self.frame_option = ttkbootstrap.Frame(self.master)
        self.frame_option.pack(side="bottom", fill="x")
        self.button_next = ttkbootstrap.Button(self.frame_option, text="下一步", command=self.bin_next)
        self.button_next.pack(side="right", padx=10, pady=10)


    def bin_next(self):
        if self.status_scan_complete is not True:
            core.window.messagebox.showinfo(title="操作阻塞", message="请等待项目扫描完成", parent=Tcl.window)
            return

        Tcl.main.sbin_entry_execute()


    def sbin_update_info(self):
        text = (
            f"项目数量: {len(containe.item_list)}\n"
            f"占用空间: {self.status_size/1024/1024:.3f} MB"
            "\n\n扫描完成\n点击下一步开始导入" if self.status_scan_complete else ""
        )
        self.label.config(text=text)


    def sbin_start_scan(self):
        root_path = containe.mods_path
        containe.item_list = []

        try:
            for class_ in os.listdir(root_path):
                class_path = os.path.join(root_path, class_)

                if not os.path.isdir(class_path):
                    continue

                for object_ in os.listdir(class_path):
                    object_path = os.path.join(class_path, object_)

                    if not os.path.isdir(object_path):
                        continue

                    for item_ in os.listdir(object_path):
                        item_path = os.path.join(object_path, item_)

                        if os.path.isdir(item_path):
                            size = get_folder_size(item_path)
                            self.status_size += size

                            info = {
                                K.INDEX.OBJECT: object_,
                                K.INDEX.NAME: item_,
                                "path": item_path
                            }
                            containe.item_list.append(info)
                            self.sbin_update_info()

                        if os.path.isfile(item_path):
                            if item_.endswith(".7z") or item_.endswith(".zip"):
                                size = os.path.getsize(item_path)
                                self.status_size += size

                                name = item_[:item_.rfind(".")]

                                info = {
                                    K.INDEX.OBJECT: object_,
                                    K.INDEX.NAME: name,
                                    "path": item_path
                                }
                                containe.item_list.append(info)
                                self.sbin_update_info()

            self.status_scan_complete = True
            self.sbin_update_info()

            if len(containe.item_list) == 0:
                core.window.messagebox.showerror(title="What are you doing?", message="这里面什么都没有\n你怕不是在消遣洒家", parent=Tcl.window)
                Tcl.main.bin_close()


        except Exception:
            core.window.messagebox.showerror(title="意外错误", message="扫描过程中出现异常", parent=Tcl.window)
            Tcl.main.bin_close()



class Execute (object):
    def __init__(self, master):
        self.master = master
        self.value_residue = 0
        self.lock = threading.RLock()

        self.label = ttkbootstrap.Label(self.master, text="剩余项目数量: 0")
        self.label.pack(side="top", fill="x", padx=10, pady=10)


    def sbin_update_info(self):
        text = f"剩余项目数量: {self.value_residue}"
        self.label.config(text=text)

        if self.value_residue == 0:
            Tcl.main.sbin_entry_eomplete()
            core.construct.event.set_event(E.MODS_INDEX_UPDATE)
            containe.status_running = False

    def sbin_start(self):
        containe.status_running = True
        self.value_residue = len(containe.item_list)
        for _ in range(8):
            core.construct.taskpool.addtask(Tcl.execute.unit_run, answer=False)


    def unit_run(self):
        while True:
            try:
                with self.lock:
                    if not containe.item_list:
                        raise SystemExit()

                    if containe.stop:
                        raise SystemExit()

                    task = containe.item_list.pop(0)

                s_object = task[K.INDEX.OBJECT]
                s_name = task[K.INDEX.NAME]
                s_path = task["path"]

                if os.path.isdir(s_path):
                    tempfilename = hex(int(time.time() * 10 ** 8)) + '.7z'
                    tempfilepath = os.path.join(core.env.directory.resources.cache, tempfilename)
                    core.external.a7z(os.path.join(s_path, '*'), tempfilepath)

                    suffix = '7z'

                    with open(tempfilepath, 'rb') as fileobject:
                        content = fileobject.read()

                    sha1 = hashlib.sha1()
                    sha1.update(content)
                    SHA = sha1.hexdigest().upper()

                elif os.path.isfile(s_path):
                    suffix = s_path[s_path.rfind(".")+1:]

                    with open(s_path, 'rb') as fileobject:
                        content = fileobject.read()

                    sha1 = hashlib.sha1()
                    sha1.update(content)
                    SHA = sha1.hexdigest().upper()

                else:
                    continue

                data = {
                    'object': s_object,
                    'type': suffix,
                    'name': s_name,
                    'author': "",
                    'grading': "G",
                    "explain": "",
                    'tags': []
                }

                filepath = os.path.join(core.userenv.directory.mods_index, 'old-migration.json')
                core.module.mods_index.item_data_new(filepath, SHA, data, restrain=True)

                with open(os.path.join(core.env.directory.resources.mods, SHA), 'wb') as fileobject:
                    fileobject.write(content)

                if os.path.isdir(s_path):
                    os.remove(tempfilepath)

            except Exception as e:
                ...

            finally:
                with self.lock:
                    self.value_residue -= 1
                    self.sbin_update_info()






class Eomplete (object):
    def __init__(self, master):
        self.master = master

        self.label = ttkbootstrap.Label(self.master, text="迁移完成")
        self.label.pack(side="top", fill="x", padx=10, pady=10)

        # self.frame_option = ttkbootstrap.Frame(self.master)
        # self.frame_option.pack(side="bottom", fill="x")
        # self.button_next = ttkbootstrap.Button(self.frame_option, text="下一步", command=self.ok)
        # self.button_next.pack(side="right", padx=10, pady=10)


class Tcl (object):
    window: ttkbootstrap.Toplevel
    main: OldMigration
    choice: Choice
    inquire: ScanInquire
    execute: Execute
    eomplete: Eomplete


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size


def get_file_sha(path):
    with open(path, 'rb') as fileobject:
        content = fileobject.read()

    sha1 = hashlib.sha1()
    sha1.update(content)
    return sha1.hexdigest().upper()
