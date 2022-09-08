from tkinter import Button


class HoverButton(Button):
    """hoverbutton class to replace the normal function of the tkinter button"""

    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["foreground"] = self["activeforeground"]

    def on_leave(self, e):
        self["foreground"] = self.defaultBackground
