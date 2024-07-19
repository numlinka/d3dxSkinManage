# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# std
import os
import locale
import tkinter.filedialog
import datetime
import threading

# site
import PIL.Image
import PIL.ImageTk
import windnd
import ttkbootstrap

# local
import core
import module
import window
from constant import T, L


class Fool (object):
    effective = False # datetime.datetime.now().strftime("%m-%d") == "04-01"
    frame_width = 0
    frame_height = 0
    widget_width = 0
    widget_height = 0
    x = 0
    y = 0
    XL = 0
    XR = 0
    YT = 0
    YB = 0
    count = 0



class Login(object):
    def __init__(self, master):
        self.master = master

        self.frame_userlist = ttkbootstrap.Frame(self.master)
        self.frame_options = ttkbootstrap.Frame(self.master)
        self.frame_description = ttkbootstrap.Frame(self.master)

        self.treeview_users = ttkbootstrap.Treeview(self.frame_userlist, selectmode="extended", show="tree")
        self.button_new_userenv = ttkbootstrap.Button(self.frame_userlist, text="新建用户环境", width=25, command=self.bin_new_userenv, cursor="hand2", takefocus=False)

        self.button_login = ttkbootstrap.Button(self.frame_options, text="Login", width=25, command=self.bin_login, cursor="hand2", takefocus=False)

        self.label_description = ttkbootstrap.Label(self.frame_description)

        self.frame_userlist.pack(side="left", fill="y", padx=10, pady=10)
        self.frame_options.pack(side="bottom", fill="x", padx=(0, 10), pady=10)
        self.frame_description.pack(side="top", fill="both", expand=True, padx=(0, 10), pady=10)

        self.treeview_users.column("#0", width=300, anchor="w")
        self.treeview_users.pack(side="top", fill="both", expand=True)
        self.button_new_userenv.pack(side="bottom", fill="x", pady=(10, 0))

        self.button_login.pack(side="bottom", padx=10, pady=(60, 60))

        self.label_description.pack(side="top", fill="both", padx=20, pady=20)

        # if not Fool.effective:
        #     self.button_login.pack(side="bottom", padx=10, pady=(20, 100))

        # else:
        #     self.button_login.configure(width=15)
        #     self.frame_login.bind("<Configure>", self._fool_configure_update)

        self.treeview_users.bind("<<TreeviewSelect>>", self.bin_users_TreeviewSelect, True)
        self.treeview_users.bind("<Double-1>", self.bin_login_double_1, True)


    def update_user_list(self):
        self.userList = []
        path = core.env.base.home
        lst = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
        self.userList = lst


    def update_image_group(self):
        self.user_image = module.image.ImageTkThumbnailGroup(40, 40)
        for name in self.userList:
            for suffix in [".png", ".jpg"]:
                path = os.path.join(core.env.base.home, name, f"picture{suffix}")
                if os.path.isfile(path):
                    break
                else:
                    path = None

            if path is None: continue
            self.user_image.add_image(path, name)


    def update_treeview(self):
        [self.treeview_users.delete(i) for i in self.treeview_users.get_children()]
        for name in self.userList:
            self.treeview_users.insert("", "end", text=f"{name}", tags=(name,), image=self.user_image.get(name))


    def initial(self):
        core.log.info("初始化登录用户列表...", L.WINDOW_LOGIN)
        self.update_user_list()
        self.update_image_group()
        self.update_treeview()


    def bin_users_TreeviewSelect(self, *args):
        name = self.treeview_users.item(self.treeview_users.focus())["text"]
        if not name: return None
        path = os.path.join(core.env.base.home, name, "description.txt")

        self.label_description["text"] = "<没有描述文件>"
        if not os.path.isfile(path): return None

        try:
            for encodeing in ["utf-8", "gb18030"]:
                with open(path, "r", encoding=encodeing) as fileobject:
                    content = fileobject.read()

                    self.label_description["text"] = content
                    break

        except Exception:
            ...

        # self._fool_first_place()


    def bin_new_userenv(self, *args):
        kernel = ModifyUserEnv()
        if kernel.wait():
            self.initial()


    def bin_login(self, *args, no_warn=False):
        name = self.treeview_users.item(self.treeview_users.focus())["text"]
        if not name:
            if no_warn: return None
            window.messagebox.showerror(title="用户名为空", message="你没有选择要登录的用户\n不要偷懒好不好")
            return None

        try:
            core.login(name)

        except Exception as e:
            core.window.messagebox.showerror(title="操作异常", message=e)


    def bin_login_double_1(self, *_):
        self.bin_login(no_warn=True)


    def _fool_first_place(self, *_):
        if not Fool.effective: return
        self.frame_login.update_idletasks()
        Fool.frame_width = self.frame_login.winfo_width()
        Fool.frame_height = self.frame_login.winfo_height()

        self.button_login.place(x=Fool.frame_width, y=Fool.frame_height)
        self.frame_login.update_idletasks()
        Fool.widget_width = self.button_login.winfo_width()
        Fool.widget_height = self.button_login.winfo_height()

        Fool.x = (Fool.frame_width - Fool.widget_width) // 2
        Fool.y = (Fool.frame_height - Fool.widget_height) // 2
        self.button_login.place(x=Fool.x, y=Fool.y)
        self._fool_update_range()
        self.frame_login.bind("<Motion>", self._fool_motion, None)


    def _fool_configure_update(self, *_):
        Fool.frame_width = self.frame_login.winfo_width()
        Fool.frame_height = self.frame_login.winfo_height()


    def _fool_update_range(self, *_):
        Fool.XL = Fool.x - Fool.widget_width // 2
        Fool.XR = Fool.x + Fool.widget_width // 2 + Fool.widget_width

        Fool.YT = Fool.y - Fool.widget_height
        Fool.YB = Fool.y + Fool.widget_height + Fool.widget_height


    def _fool_motion(self, event):
        px = event.x
        py = event.y

        if not Fool.XL < px < Fool.XR or not Fool.YT < py < Fool.YB: return

        oxs = (px - Fool.XL, px - Fool.XR)
        oys = (py - Fool.YT, py - Fool.YB)
        ox = oxs[0] if oxs[0] < abs(oxs[1]) else oxs[1]
        oy = oys[0] if oys[0] < abs(oys[1]) else oys[1]

        if abs(ox) > Fool.widget_width // 2:
            Fool.y += oy
        elif abs(oy) > Fool.widget_height // 2:
            Fool.x += ox
        else:
            Fool.y += oy
            Fool.x += ox


        self._fool_update_range()

        if Fool.XL < 0: Fool.x = Fool.frame_width - Fool.widget_width - Fool.widget_width // 2; Fool.count += 100
        if Fool.XR > Fool.frame_width: Fool.x = Fool.widget_width // 2; Fool.count += 100

        if Fool.YT < 0: Fool.y = Fool.frame_height - Fool.widget_height - Fool.widget_height; Fool.count += 100
        if Fool.YB > Fool.frame_height: Fool.y = Fool.widget_height; Fool.count += 100
        self._fool_update_range()

        self.button_login.place(x=Fool.x, y=Fool.y)

        Fool.count += 1
        if Fool.count > 1000:
            result = window.messagebox.askyesno(title="这屌按钮乱跑怎么办", message="是否受不了直接投降？\n\nY - 大丈夫能屈能伸\nN - 我决不会倒下")
            Fool.count = 0
            if not result: return
            self.frame_login.bind("<Motion>", lambda *_: None, None)



class ModifyUserEnv(object):
    def __init__(self, userenv: str = ""):
        self._edit_mode = bool(userenv)
        self.result = False
        self.window = ttkbootstrap.Toplevel("修改用户环境" if self._edit_mode else "新建用户环境")
        self.window.transient(core.window.mainwindow)
        self.window.grab_set()
        core.window.methods.fake_withdraw(self.window)
        self.install()
        self.window.update()
        core.window.methods.center_window_for_window(self.window, core.window.mainwindow, 600, 480, True)
        self.window.resizable(False, False)
        self.window.focus()


    def install(self):
        self._image = PIL.ImageTk.PhotoImage(PIL.Image.new("RGBA", (40, 40), "#00000000"))

        self.labelframe_username = ttkbootstrap.LabelFrame(self.window, text="用户名称")
        self.labelframe_userimage = ttkbootstrap.LabelFrame(self.window, text="用户头像")
        self.labelframe_userdescription = ttkbootstrap.Frame(self.window)
        self.labelframe_options = ttkbootstrap.Frame(self.window)

        self.entry_username = ttkbootstrap.Entry(self.labelframe_username)

        self.label_image = ttkbootstrap.Label(self.labelframe_userimage, image=self._image)
        self.entry_image = ttkbootstrap.Entry(self.labelframe_userimage, state="readonly")
        self.label_hint = ttkbootstrap.Label(self.labelframe_userimage, text="请将图片拖拽至此或使用右侧的工具")
        self.button_image = ttkbootstrap.Button(self.labelframe_userimage, text="选择图片", width=10, bootstyle="success-outline", command=self.bin_choice_image)
        self.button_reset = ttkbootstrap.Button(self.labelframe_userimage, text="重置图片", width=10, bootstyle="success-outline", command=self.bin_reset_image)

        self.text_description = ttkbootstrap.Text(self.labelframe_userdescription, height=10)
        self.scrollbar = ttkbootstrap.Scrollbar(self.labelframe_userdescription, orient="vertical", command=self.text_description.yview)
        self.text_description.configure(yscrollcommand=self.scrollbar.set)

        self.button_sure = ttkbootstrap.Button(self.labelframe_options, text="确定", width=10, bootstyle="success-outline", command=self.bin_sure)
        self.button_cancel = ttkbootstrap.Button(self.labelframe_options, text="取消", width=10, bootstyle="warning-outline", command=self.bin_cancel)
        self.warn = ttkbootstrap.Label(self.labelframe_options, text="", bootstyle="danger")

        self.labelframe_username.pack(side="top", fill="x", padx=10, pady=(10, 10))
        self.labelframe_userimage.pack(side="top", fill="x", padx=10, pady=(0, 10))
        self.labelframe_userdescription.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))
        self.labelframe_options.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

        self.entry_username.pack(side="top", fill="x", expand=True, padx=5, pady=5)

        self.labelframe_userimage.columnconfigure(1, weight=10)
        self.label_image.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
        self.entry_image.grid(row=0, column=1, columnspan=3, padx=(0, 5), pady=(5, 5), sticky="ew")
        self.label_hint.grid(row=1, column=1, padx=(0, 5), pady=5, sticky="w")
        self.button_image.grid(row=1, column=2, padx=(0, 5), pady=(0, 5))
        self.button_reset.grid(row=1, column=3, padx=(0, 5), pady=(0, 5))

        self.text_description.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", padx=(5, 0))

        self.button_sure.pack(side="right")
        self.button_cancel.pack(side="right", padx=(0, 5))
        self.warn.pack(side="left", padx=(0, 5))

        windnd.hook_dropfiles(self.labelframe_userimage, func=self.bin_hook_dropfiles)

        _alt_set = core.window.annotation_toplevel.register
        _alt_set(self.entry_username, T.ANNOTATION_USER_NAME, 2)
        _alt_set(self.label_image, T.ANNOTATION_USER_IMAGE, 2)
        _alt_set(self.entry_image, T.ANNOTATION_USER_IMAGE, 2)
        _alt_set(self.text_description, T.ANNOTATION_USER_EDIT_DESCRIPTION, 2)


    def sbin_set_image_path(self, path: str):
        self.entry_image.configure(state="normal")
        self.entry_image.delete(0, "end")
        self.entry_image.insert(0, path)
        self.entry_image.configure(state="readonly")
        # self._image = core.module.image.image_canvas(path, 40, 40, True)
        # self.label_image.configure(image=self._image)


    def sbin_set_warning(self, text: str = ""):
        self.warn.configure(text=text)


    def sbin_set_image(self, path: str = ""):
        for suffix in [".png", ".jpg"]:
            if path.endswith(suffix):
                break
        else:
            return

        self.sbin_set_image_path("处理中...")
        self._image = core.module.image.image_canvas(path, 40, 40, True)
        self.label_image.configure(image=self._image)
        self.sbin_set_image_path(path)

    def bin_hook_dropfiles(self, original_items: list[bytes]):
        threading.Thread(None, self.bin_hook_dropfiles_new, "async.dropfiles", (original_items, ), daemon=True).start()

    def bin_hook_dropfiles_new(self, original_items: list[bytes]):
        core.log.debug(f"dropfiles_new 钩子 {original_items}")
        oscode = locale.getpreferredencoding()
        try:
            items = [x.decode(oscode) for x in original_items]

        except Exception:
            core.window.messagebox.showerror(title="dropfiles: 编码不可解", message=f"无法解码消息内容\n目标与系统编码冲突 {oscode}")
            return

        item = items[0]
        self.window.after(0, self.sbin_set_image, item)

    def bin_choice_image(self, *_):
        path = tkinter.filedialog.askopenfilename(parent=self.window, title="选择图片", filetypes=[("图片文件", ["*.png", "*.jpg"])])
        if not path: return
        self.sbin_set_image(path)


    def bin_reset_image(self, *_):
        self.sbin_set_image_path("")
        self._image = PIL.ImageTk.PhotoImage(PIL.Image.new("RGBA", (40, 40), "#00000000"))
        self.label_image.configure(image=self._image)


    def bin_sure(self, *_):
        try:
            new_username = self.entry_username.get().strip()

            if not new_username:
                self.sbin_set_warning("用户名不能为空")
                return

            for chat in ["/", "\\", ":", "*", "?", "\"", "<", ">", "|"]:
                if chat in new_username:
                    self.sbin_set_warning("用户名称包含非法字符 \\ / : * ? < > |")
                    return

            new_description = self.text_description.get(0.0, "end")[:-1]
            new_image_path = self.entry_image.get()

            new_profile = os.path.join(core.env.base.home, new_username)

            if self._edit_mode:
                ...  # 没做编辑模式
                return

            else:
                if os.path.exists(new_profile):
                    self.sbin_set_warning("用户名已存在")
                    return

                else:
                    os.makedirs(new_profile)

            if new_image_path:
                try:
                    with open(new_image_path, "rb") as image_file:
                        new_image_content = image_file.read()

                    _, suffix = os.path.splitext(new_image_path)
                    new_save_path = os.path.join(new_profile, f"picture{suffix}")

                    with open(new_save_path, "wb") as image_file:
                        image_file.write(new_image_content)

                except PermissionError as e:
                    core.window.messagebox.showerror(title="权限错误", message=f"{e}\n\n无法访问目标位置\n请检查权限组设置", parent=self.window)

                except Exception as e:
                    core.window.messagebox.showerror("未定义错误", f"保存用户头像失败：\n{e.__class__} {e}", parent=self.window)

            if new_description:
                description_path = os.path.join(new_profile, "description.txt")

                with open(description_path, "w", encoding="utf-8") as description_file:
                    description_file.write(new_description)

        except PermissionError as e:
            core.window.messagebox.showerror(title="权限错误", message=f"{e}\n\n无法访问目标位置\n请检查权限组设置", parent=self.window)

        except Exception as e:
            core.window.messagebox.showerror("未定义错误", f"{e.__class__} {e}", parent=self.window)

        self.result = True
        self.bin_cancel()


    def bin_cancel(self, *_):
        self.window.destroy()


    def wait(self):
        self.window.wait_window()
        return self.result
