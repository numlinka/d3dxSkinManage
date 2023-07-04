# -*- coding: utf-8 -*-

import ttkbootstrap


class Block (object):
    def __init__(self, master):
        self.master = master
        self.text_message = ttkbootstrap.Text(self.master, state="disabled", borderwidth=0, highlightthickness=0)
        self.text_message.pack(side="top", fill="both", expand=True, padx=10, pady=10)


    def setcontent(self, content: str) -> None:
        self.text_message.config(state="normal")
        self.text_message.delete(0.0, "end")
        self.text_message.insert(0.0, content)
        self.text_message.config(state="disabled")
