from tkinter import ttk


class GuiStyle:
    """controls ttk style when called"""

    def __init__(self, theme_instance):
        """modifies the ttk theme, notebook, combobox, and the progress bar"""

        # create ttk.Style instance
        custom_style = ttk.Style()

        # create theme
        custom_style.theme_create(
            "jlw_style",
            parent="alt",
            settings={
                # notebook theme settings
                "TNotebook": {
                    "configure": {
                        "tabmargins": [5, 5, 5, 0],
                        "background": theme_instance.custom_frame_bg_colors[
                            "specialbg"
                        ],
                    }
                },
                "TNotebook.Tab": {
                    "configure": {
                        "padding": [5, 1],
                        "background": theme_instance.custom_listbox_color[
                            "selectbackground"
                        ],
                        "foreground": theme_instance.custom_button_colors["foreground"],
                        "focuscolor": "",
                    },
                    "map": {
                        "background": [
                            (
                                "selected",
                                theme_instance.custom_frame_bg_colors["specialbg"],
                            )
                        ],
                        "expand": [("selected", [1, 1, 1, 0])],
                    },
                },
                # combobox theme settings
                "TCombobox": {
                    "configure": {
                        "selectbackground": theme_instance.custom_listbox_color[
                            "selectbackground"
                        ],
                        "fieldbackground": theme_instance.custom_listbox_color[
                            "selectbackground"
                        ],
                        "foreground": theme_instance.custom_listbox_color["foreground"],
                        "selectforeground": theme_instance.custom_listbox_color[
                            "selectforeground"
                        ],
                    }
                },
            },
        )

        # enables the use of the custom theme
        custom_style.theme_use("jlw_style")

        # adjust the progress bar layout
        custom_style.layout(
            "text.Horizontal.TProgressbar",
            [
                (
                    "Horizontal.Progressbar.trough",
                    {
                        "children": [
                            (
                                "Horizontal.Progressbar.pbar",
                                {"side": "left", "sticky": "ns"},
                            )
                        ],
                        "sticky": "nswe",
                    },
                ),
                ("Horizontal.Progressbar.label", {"sticky": "nswe"}),
            ],
        )

        # set initial text
        custom_style.configure(
            "text.Horizontal.TProgressbar",
            text="",
            anchor="center",
            background=theme_instance.custom_button_colors["foreground"],
            foreground=theme_instance.custom_button_colors["activeforeground"],
        )
        custom_style.master.option_add(
            "*TCombobox*Listbox.foreground",
            theme_instance.custom_listbox_color["foreground"],
        )
        custom_style.master.option_add(
            "*TCombobox*Listbox.background",
            theme_instance.custom_listbox_color["background"],
        )
        custom_style.master.option_add(
            "*TCombobox*Listbox.selectBackground",
            theme_instance.custom_listbox_color["background"],
        )
        custom_style.master.option_add(
            "*TCombobox*Listbox.selectForeground",
            theme_instance.custom_listbox_color["selectforeground"],
        )
