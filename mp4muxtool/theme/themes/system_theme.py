from tkinter import (
    Button,
    Entry,
    LabelFrame,
    Frame,
    Label,
    Listbox,
    Spinbox,
    Text,
    scrolledtext,
)


class SystemTheme:
    """
    Creates temporary widgets that never gets displayed to extract their default color/theme
    After the values are extracted the widgets are immediately destroyed
    """

    def __init__(self, main_gui):
        """create mp4 window variable and run the system theme method"""

        self.mp4_win = main_gui.mp4_win
        self.__system_theme()

    def __system_theme(self):
        """create temporary widgets that are never displayed on screen and get their default values"""

        self.custom_window_bg_color = self.mp4_win.cget("bg")

        temp_btn = Button()
        self.custom_button_colors = {
            "foreground": temp_btn.cget("fg"),
            "background": temp_btn.cget("bg"),
            "activeforeground": temp_btn.cget("activeforeground"),
            "activebackground": temp_btn.cget("activebackground"),
            "disabledforeground": temp_btn.cget("disabledforeground"),
        }
        temp_btn.destroy()

        temp_entry = Entry()
        self.custom_entry_colors = {
            "foreground": temp_entry.cget("fg"),
            "background": temp_entry.cget("bg"),
            "disabledforeground": temp_entry.cget("disabledforeground"),
            "disabledbackground": temp_entry.cget("disabledbackground"),
        }
        temp_entry.destroy()

        temp_lbl_frame = LabelFrame()
        self.custom_label_frame_colors = {
            "foreground": temp_lbl_frame.cget("fg"),
            "background": temp_lbl_frame.cget("bg"),
        }
        temp_lbl_frame.destroy()

        temp_frame = Frame()
        self.custom_frame_bg_colors = {
            "background": temp_frame.cget("bg"),
            "highlightcolor": temp_frame.cget("highlightcolor"),
            "specialbg": temp_frame.cget("bg"),
        }
        temp_frame.destroy()

        temp_label = Label()
        self.custom_label_colors = {
            "foreground": temp_label.cget("fg"),
            "background": temp_label.cget("bg"),
        }
        temp_label.destroy()

        temp_scrolled_text = scrolledtext.ScrolledText()
        self.custom_scrolled_text_widget_color = {
            "foreground": temp_scrolled_text.cget("fg"),
            "background": temp_scrolled_text.cget("bg"),
        }
        temp_scrolled_text.destroy()

        temp_listbox = Listbox()
        self.custom_listbox_color = {
            "foreground": temp_listbox.cget("fg"),
            "background": temp_listbox.cget("bg"),
            "selectbackground": temp_listbox.cget("selectbackground"),
            "selectforeground": temp_listbox.cget("selectforeground"),
        }
        temp_listbox.destroy()

        temp_spinbox = Spinbox()
        self.custom_spinbox_color = {
            "foreground": temp_spinbox.cget("fg"),
            "background": temp_spinbox.cget("bg"),
            "buttonbackground": temp_spinbox.cget("buttonbackground"),
            "readonlybackground": temp_spinbox.cget("readonlybackground"),
        }
        temp_spinbox.destroy()

        temp_text = Text()
        self.custom_text_color = {
            "background": temp_text.cget("bg"),
            "foreground": temp_text.cget("fg"),
        }
        temp_text.destroy()
