# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

# local
import core
import window
import constant


msg = [
    "该软件仅供个人使用，禁止用于商业用途",
    "该软件仅供学术研究和交流目的，使用时请自行承担风险",
    "该软件免费开源，任何第三方变卖所带来的问题不予解决",
    "在使用过程中遇到问题请点击右下角的帮助以阅读帮助文档"
]

index = -1


def title_cycle(*_):
    global index
    index += 1
    if index == len(msg): index = 0
    text = core.env.MAIN_TITLE + "  :  " + msg[index]
    window.mainwindow.title(text)
    window.mainwindow.after(10000, title_cycle)


def ready():
    window.mainwindow.after(5000, title_cycle)


def initial():
    core.construct.event.register(constant.E.ENTER_MAINPOOL, ready)
