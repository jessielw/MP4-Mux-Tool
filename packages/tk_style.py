from tkinter import ttk


class GuiStyle:
    """control ttk style here"""

    def __init__(self, main_gui):
        self.mp4_win = main_gui.mp4_win

        # create ttk.Style instance
        custom_style = ttk.Style()

        # create theme
        custom_style.theme_create(
            "jlw_style",
            parent="alt",
            settings={
                # notebook theme
                "TNotebook": {"configure": {"tabmargins": [5, 5, 5, 0]}},
                "TNotebook.Tab": {
                    "configure": {
                        "padding": [5, 1],
                        "background": "grey",
                        "foreground": "white",
                        "focuscolor": "",
                    },
                    "map": {
                        "background": [("selected", "#434547")],
                        "expand": [("selected", [1, 1, 1, 0])],
                    },
                },
                # combobox theme
                "TCombobox": {
                    "configure": {
                        "selectbackground": "#23272A",
                        "fieldbackground": "#23272A",
                        "background": "white",
                        "foreground": "white",
                    }
                },
            },
        )

        # enable the newly defined theme
        custom_style.theme_use("jlw_style")

        # combobox mouse hover code
        self.mp4_win.option_add("*TCombobox*Listbox*Background", "#404040")
        self.mp4_win.option_add("*TCombobox*Listbox*Foreground", "#FFFFFF")
        self.mp4_win.option_add("*TCombobox*Listbox*selectBackground", "#FFFFFF")
        self.mp4_win.option_add("*TCombobox*Listbox*selectForeground", "#404040")
        custom_style.map(
            "TCombobox", foreground=[("hover", "white")], background=[("hover", "grey")]
        )
        custom_style.configure("purple.Horizontal.TProgressbar", background="purple")
