# Licensed under the GPL 3.0 License.
# d3dxSkinManage by numlinka.

# std
import tkinter
import tkinter.font
import threading

# site
import ttkbootstrap

# local
import core


class KEY (object):
    LABEL = "label"
    COMMAND = "command"
    GROUP = "group"
    ORDER = "order"
    CONDITION = "condition"
    STATE_CONDITION = "state_condition"
    NEED_VALUE = "need_value"

try:
    infinity = float('inf')

except Exception as _:
    infinity = 10 ** 10


class DynamicMenu (object):
    def __init__(self, master: tkinter.Widget, sequence: str = "<Button-3>", offsets: tuple[int] = (0, 0), add: bool = None,
                 value_source: object = None, value_source_is_not_callable: bool = False):
        self.master = master
        self.sequence = sequence
        self.offsets = offsets
        self.value_source = value_source
        self.value_source_is_not_callable = value_source_is_not_callable

        self._table: dict[int: list[dict[str: str]]] = {}
        self._table_group_list = []

        self.master.bind(sequence, self.call, add)

        self._lock = threading.RLock()


    def get_value_result(self, event):
        with self._lock:
            try:
                if self.value_source_is_not_callable:
                    return self.value_source

                if callable(self.value_source):
                    return self.value_source(event)

            except Exception as _:
                return None

            return self.value_source


    def call(self, event):
        try:
            default_font = tkinter.font.nametofont("TkDefaultFont")
            menu = ttkbootstrap.Menu(self.master, tearoff=False, font=(default_font.actual("family"), default_font.actual("size")))

        except Exception as _:
            menu = ttkbootstrap.Menu(self.master, tearoff=False)

        value_result = self.get_value_result(event)
        valid_values = 0

        for group in self._table_group_list:
            labelist = self._table[group]

            if valid_values != 0:
                menu.add_separator()
                valid_values = 0

            for labelitem in labelist:
                label = "未知"

                try:
                    label = labelitem[KEY.LABEL]
                    command = labelitem[KEY.COMMAND]
                    need_value = labelitem[KEY.NEED_VALUE]
                    condition = labelitem[KEY.CONDITION]
                    state_condition = labelitem[KEY.STATE_CONDITION]

                    # 检查是否需要显示
                    if isinstance(condition, bool):
                        condition_result = condition

                    elif callable(condition):
                        condition_result = condition(value_result) if need_value else condition()

                    else:
                        condition_result = True

                    if not condition_result:
                        continue

                    # 检查是否置为动作
                    if isinstance(state_condition, bool):
                        state_condition_result = state_condition

                    elif callable(state_condition):
                        state_condition_result = state_condition(value_result) if need_value else state_condition()

                    else:
                        state_condition_result = True

                    state = "active" if state_condition_result else "disabled"

                    # 添加标签
                    menu.add_command(label=label, command=command, state=state)
                    valid_values += 1

                except Exception as e:
                    core.log.error(f"添加菜单标签 \"{label}\" 时出现异常 {e.__class__} {e}")

        offset_x, offset_y = self.offsets
        menu.post(event.x_root+offset_x , event.y_root+offset_y)


    def _sort_order_value(self, item):
        try:
            value = item.get(KEY.ORDER, infinity)

        except Exception as _:
            return infinity

        return value


    def sort(self):
        with self._lock:
            temp_group_list = []
            empty_group_list = []

            for groupkey, labelist in self._table.items():
                if not labelist:
                    empty_group_list.append(groupkey)
                    continue

                temp_group_list.append(groupkey)
                labelist.sort(key=self._sort_order_value)

            temp_group_list.sort()
            self._table_group_list = temp_group_list


    def add_label(self, label: str, command: object, group: int = 100, order: int = -1,
                  condition: bool | object = True, state_condition: bool | object = True, need_value: bool = False):
        """
        ## 添加标签

        ```
        label: str 标签文本内容
        command: object 点击标签后执行的函数
        group: int 所属组, 同时决定组的排序, 不同的组之间会有分割线
        order: int 组内排序, -1 表示排在末尾
        condition: bool | object 显示条件, bool 或者是一个可调用对象, 结果为 Ture 才会显示
        state_condition: bool | object 状态显示条件, bool 或者是一个可调用对象, 结果为 False 时将 state 标记为 disabled
        need_value: bool 可调用对象是否需要参数, 由 value_source 的返回值或本身提供
        ```
        """

        # check parameters
        if not isinstance(label, str):
            TypeError("The type of label must be str.")

        if not callable(command):
            TypeError("The command must be callable.")

        if not isinstance(group, int):
            TypeError("The type of group must be int.")

        if group < 0:
            TypeError("The value of group cannot be less than 0.")

        if not isinstance(order, int):
            TypeError("The type of order must be int.")

        if order < -1:
            TypeError("The value of order cannot be less than 0.")

        if not isinstance(condition, bool) and not callable(condition):
            TypeError("The type of condition must be bool or callable.")

        if not isinstance(state_condition, bool) and not callable(state_condition):
            TypeError("The type of state_condition must be bool or callable.")

        if not isinstance(need_value, bool):
            TypeError("The type of need_value must be bool.")

        # add
        with self._lock:
            if group not in self._table:
                self._table[group] = []

            if order == -1:
                order = infinity

            data = {
                KEY.LABEL: label,
                KEY.COMMAND: command,
                KEY.ORDER: order,
                KEY.CONDITION: condition,
                KEY.STATE_CONDITION: state_condition,
                KEY.NEED_VALUE: need_value
            }

            self._table[group].append(data)
            self.sort()


__all__ = ["DynamicMenu"]
