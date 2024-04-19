# 这是一位用户的需求
# 他希望在每次导入新 mod 之后，自动跳转到它添加的对应分类、对象、并选择它
# 但是 addmod2 模块本身不支持外置扩展，我并没有预留接口
# 所以这个功能制作为插件会很困难，且不安全

# 尽管这里的实现方式也不安全
# 但，能用就行

# std
import time
import threading

# local
import core
import core.structure
import module
import window
import constant


_lock = threading.RLock()


def _focus_item(SHA: str, object_: str):
    try:
        # 同一时间只允许一个线程 避免冲突
        # 中途只要有任意一个信号等待超时则放弃条目焦点
        if not _lock.acquire(timeout=0.1): return

        # 等待 MODS_INDEX_UPDATE 事件
        # 确定数据条目已被写入到数据表中
        # if not core.construct.event.wait(constant.E.MODS_INDEX_UPDATE, 1): return

        # 等待 MODS_MANAGE_CACHE_REFRESHED 事件
        # 确认缓存数据区已被刷新
        # if not core.construct.event.wait(constant.E.MODS_MANAGE_CACHE_REFRESHED, 2): return

        # 等待 WINDOW_MODS_MANAGE_TV_CHOICE_UPDATE 事件
        # 确认树视图选择项已被更新
        if not core.construct.event.wait(constant.E.WINDOW_MODS_MANAGE_TV_CLASS_UPDATE, 2): return

        for class_ in module.mods_manage.get_class_list():
            if object_ in module.mods_manage.get_object_list(class_):
                break

        else: return

        window.interface.mods_manage.treeview_classification.focus(class_)
        window.interface.mods_manage.treeview_classification.selection_set(class_)
        if not core.construct.event.wait(constant.E.WINDOW_MODS_MANAGE_TV_OBJECT_UPDATE, 2): return

        window.interface.mods_manage.treeview_objects.focus(object_)
        window.interface.mods_manage.treeview_objects.selection_set(object_)
        if not core.construct.event.wait(constant.E.WINDOW_MODS_MANAGE_TV_CHOICE_UPDATE, 2): return

        window.interface.mods_manage.treeview_choices.focus(SHA)
        window.interface.mods_manage.treeview_choices.selection_set(SHA)
        time.sleep(1) # 额外占用锁一段时间

    finally:
        _lock.release()


def focus_item(SHA: str, object_: str):
    core.construct.taskpool.newtask(_focus_item, (SHA, object_), {}, False)
