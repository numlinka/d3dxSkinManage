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
R0 = random.randint(0, 999)

RANDOMNUM = f"{R1}-{R2}-{R3}-{R4}-{R5}-{R6}-{R7}-{R8}-{R9}-{R0}"

CONTENT = """d3dxSkinManage

d3dxSkinManage 是一个免费 ( free ) 开源 ( open source ) 软件
对于软件的修改和再分发请遵守 GNU General Public License v3.0 协议

d3dxSkinManage 并非用于商业用途，仅限个人使用。
该工具仅供学术研究和交流目的，如果您选择使用，请自行承担风险。

d3dxSkinManage 不会以任何形式收集您的任何信息，
也不会将您的任何信息上传到任何服务器。

若在使用过程中遇到问题，请先阅读帮助文档，
点击窗口右下方的 " [帮助] " 按钮前往页面能解答大多数疑问，
教程、帮助文档和常见问题解答，它们不是摆设，
即便是错误弹窗也会提供关键信息或解决方法。

当你遇到一些特殊或比较棘手的问题时，
可以联系技术人员以寻求帮助。

对于软件的 bug 反馈或建议，请在 GitHub 页面提交 issue
或发送邮件至 numlinka@163.com

不要使用管理员权限运行该软件，
在操作需要提升时我们会主动请求，
你不该把管理员权限随意交给陌生的程序。
另外，
文件钩子不能跨用户传递消息，
这意味着文件拖拽会失效。



如果你喜欢这个项目，
可以在 GitHub 上给一个 star，
或是在爱发电上赞助我们。

同时我们也会在项目网站上附上一些 Mod 创作者的链接，
你可以在这些链接中找到、关注他们的创作，并支持他们。

如果这些链接中没有出现你的名字，
或是你不希望你的名字出现在上面，
可以联系我们更进。



有关 d3dxSkinManage 的更多信息请访问
    - https://github.com/numlinka/d3dxSkinManage
    - https://d3dxskinmanage.numlinka.com



你可以在以下链接赞助我们
    - numLinka
        - https://afdian.net/a/numlinka

    - 黎愔
        - https://afdian.net/a/ticca



d3dxSkinManage 官方不会以任何形式在任何平台上售卖该软件，
也不会售卖软件的程序扩展 ( 如插件 ) 或 Mod ( 皮肤模组 ) 等资源。

我知道我的软件被其他人连同一些 Mod 插件等资源打包之后，
在咸鱼、淘宝、拼多多等平台售卖，也有人在向我反馈这些事情。

如果你已经购买了，那么你需要注意一些事情：
首先，不要在我这里或其它交流群 ( 频道 ) 推荐你的购买渠道，
很多人不欢迎你这么做，尤其是创作者，
他们 ( 包括我 ) 可能会对你和售卖者产生反感 ( 或敌意 )。

其次，你需要学会自己解决问题，尤其是那些基础的问题，
遇到棘手的问题，去寻求你的客服，在多数情况下，
那些售卖者在赚到钱后不会惠及创作者一分一厘，
那些创作者包括我们，没有必要且不乐意去帮这个忙。

他们赚了钱，却不会给创作者带去任何价值，
而你遇到了问题却选择让创作者帮你解决，
你认为这合适吗？

我承认，他们确实给更多的人提供了接触 Mod 的机会，
我也承认，他们确实也付出了时间做资源整理，
于此之上的同时，他们也赚到钱。( 如果你认可他们的行为 )

但是！
在这之中存在着一个问题，
多数售卖者在展示的图片中刻意的抹去了软件和作者的名字，
包括其打包在内的资源，绝大多数都没有标注作者，
他们无时无刻不在制造信息差。

许多创作者用爱发电，分享着自己的创作成果，
但是却看到自己的作品被冠上了别人的名字、被别人倒卖，
这是多么一件令人心寒的事情，不论出于何种原因，
尊重并正确标注原作者是对创作者劳动成果的基本认可。




"""

YOU_DO_NOT_KNOW = "你晓得就有鬼了\n你看都没看"



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
        self.text.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=(5, 0))

        self.scrollbar = ttkbootstrap.Scrollbar(self.text, command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.text.insert(0.0, CONTENT)
        self.text.configure(state=DISABLED)

        self.text.bind("<Enter>", lambda *_: self.scrollbar.pack(side="right", fill="y"), "+")
        self.text.bind("<Leave>", lambda *_: self.scrollbar.pack_forget(), "+")


    def know(self):
        if self.v_time.get() > 0:
            window.messagebox.showinfo("当真？", YOU_DO_NOT_KNOW, parent=self.window)
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
