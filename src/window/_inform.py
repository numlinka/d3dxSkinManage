import random

import ttkbootstrap
from ttkbootstrap.constants import *

import core
import window


R1 = random.randint(0, 99)
R2 = random.randint(0, 99)
R3 = random.randint(0, 99)
R4 = random.randint(0, 99)
R5 = random.randint(0, 99)
R6 = random.randint(0, 99)
R7 = random.randint(0, 99)
R8 = random.randint(0, 99)
R9 = random.randint(0, 99)
R0 = random.randint(0, 99)

RANDOMNUM = f"{R1}-{R2}-{R3}-{R4}-{R5}-{R6}-{R7}-{R8}-{R9}-{R0}"

CONTENT = """d3dxSkinManage

GNU General Public License 3.0

Copyright (C) 2023 numlinka

This program is free software: you can redistribute it and/or modify it under the \
terms of the GNU General Public License as published by the Free Software Foundation, \
either version 3 of the License, or (at your option) any later version. 

This program is distributed in the hope that it will be useful, but WITHOUT ANY \
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A \
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this \
program. If not, see <https://www.gnu.org/licenses/>.



　　本软件由 numlinka 开发，并受 GPLv3 协议保护，项目源代码在 GitHub 上公开。

　　本项目按“原样”提供，不提供任何明示或暗示的保证，包括但不限于适销性、特定用途的适\
用性和非侵权性。在任何情况下，版权持有者或贡献者不对因使用本软件而产生的任何索赔、损\
害或其他责任负责，无论是在合同诉讼、侵权行为还是其他情况下。如果你无法对自己的行为负\
责或不信任该项目带来的任何内容，请立即关闭此程序，并将它在你的计算机设备上永久性移除。

　　在 1.6 版本中，我们计划改变部分目录结构，将部分资源逐步私有到用户环境内，这可能\
需要使用者在后续更新中手动移动资源文件或修改配置文件，如果不希望接受此更新，请关闭程\
序，在项目主页下载 1.5 版本替换，并参考帮助文档的《禁用更新检查》以不再接受后续更新，\
你已经被提醒过了。

　　如果你喜欢这个项目，可以在 GitHub 上给一个 star ，或是在爱发电上赞助我们。同时我\
们也会在项目网站上附上一些 Mod 创作者的链接，你可以在这些链接中找到、关注他们的创作，\
并支持他们。如果这些链接中没有出现你的名字，或是你不希望你的名字出现在上面，可以联系\
我们更进。

　　d3dxSkinManage 是一款免费 (free) 自由 (free) 的开源 (open source) 软件，它并非用\
于商业用途，官方不会以任何形式在任何平台上售卖该软件，在使用一切非官方资源时，我们将\
有权拒绝为其提供任何形式的技术支持，即便你是其中的受害者。

　　在使用时遇到问题请先阅读帮助文档、常见问题解答或观看视频流媒体教程，在提问时请详\
细描述你的问题，表达你的意图、描述你已有的操作并附上相关截图或日志，以便我们能更快更\
好的帮助你解决。

　　你可以通过我们的官方渠道提交任何使用过程中遇到的问题或建议，我们会在合理的时间内\
进行处理，任何包含有损害其他用户或创作者权益的内容均不予受理。

　　除非在有官方和创作者的连携支持下，否则无论出于何种原因，不得在官方频道或社区宣传\
任何第三方卖家，无论对方的质量、安全性、可用性和可靠性。如果你的资源来着第三方卖家，\
遇到问题时请找你的客服，不要拿我们当售后，开发者包括其他用户均没有义务回复你的问题。

　　我们保留对 d3dxSkinManage 进行升级和维护的权利，并可能在无需提前通知的情况下发布\
更新版本或进行服务维护。

　　无论你是否已认真阅读上述内容，在你点击 "我已知晓" 按钮之后我们均认为你已阅读并理\
解上述内容，在这之后一切与 d3dxSkinManage 的交流，均应遵循相应规定。



有关 d3dxSkinManage 的更多信息请访问

- 开源地址： https://github.com/numlinka/d3dxSkinManage
- 项目主页： https://d3dxskinmanage.numlinka.com



你可以在以下链接赞助我们
    - numLinka
        - https://afdian.net/a/numlinka

    - 黎愔
        - https://afdian.net/a/ticca




"""

YOU_DO_NOT_KNOW = "你晓得就有鬼了\n你看都没看"
MAYBE_YOU_KNOW = "慢慢看\n或许你需要知道一些信息"
I_KNOW_YOU_KNOW = "或许你已经看完了\n但是你仍然需要等待倒计时"


class Inform (object):
    def __init__(self):
        self.version = 1
        self.window = ttkbootstrap.Toplevel(RANDOMNUM)
        self.window.withdraw()

        self.v_time = ttkbootstrap.IntVar()
        self.v_time.set(30)

        self.frame = ttkbootstrap.Frame(self.window)
        self.button_know = ttkbootstrap.Button(self.frame, text="我已知晓", bootstyle=(OUTLINE, SUCCESS), command=self.know)
        self.time = ttkbootstrap.Label(self.frame, textvariable=self.v_time)
        self.text = ttkbootstrap.Text(self.window)

        self.frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
        self.button_know.pack(side=RIGHT)
        self.time.pack(side=LEFT)
        self.text.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=(5, 0))

        self.scrollbar = ttkbootstrap.Scrollbar(self.window, command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.text.insert(0.0, CONTENT)
        self.text.configure(state=DISABLED)

        self.scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 5), pady=(5, 0))

        # self.text.bind("<Enter>", lambda *_: self.scrollbar.pack(side="right", fill="y"), "+")
        # self.text.bind("<Leave>", lambda *_: self.scrollbar.pack_forget(), "+")


    def know(self):
        if self.v_time.get() > 20:
            window.messagebox.showinfo("当真？", YOU_DO_NOT_KNOW, parent=self.window)
        elif self.v_time.get() > 10:
            window.messagebox.showinfo("略有蹊跷", MAYBE_YOU_KNOW, parent=self.window)
        elif self.v_time.get() > 0:
            window.messagebox.showinfo("硬控 30 秒", I_KNOW_YOU_KNOW, parent=self.window)
        else:
            core.env.configuration.inform_uuid = core.env.uuid
            core.env.configuration.inform_version = self.version
            self.window.destroy()


    def decrease(self):
        self.v_time.set(self.v_time.get() - 1)
        if self.v_time.get() > 0:
            self.window.after(1000, self.decrease)


    def exhibit(self):
            window.methods.center_window_for_window(self.window, window.mainwindow, 600, 800, True)
            self.window.deiconify()
            self.window.update()
            self.window.focus_set()
            self.window.transient(window.mainwindow)
            self.window.grab_set()
            self.window.protocol("WM_DELETE_WINDOW", core.action.askexit.execute)
            self.window.after(1000, self.decrease)
            self.window.wait_window()


    def check(self):
        if core.env.configuration.inform_white_uuid == core.env.uuid:
            self.window.destroy()

        elif core.env.configuration.inform_uuid != core.env.uuid:
            self.exhibit()

        elif core.env.configuration.inform_version != self.version:
            self.exhibit()

        else:
            self.window.destroy()

        return
