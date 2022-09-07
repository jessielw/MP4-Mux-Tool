from configparser import ConfigParser

from packages.config_writer import config_file
from packages.themes import bhd_theme
from packages.themes.system_theme import SystemTheme


class OpenTheme:
    def __init__(self, main_gui):
        """define tk window, open the config file, and run the check theme method"""
        self.mp4_win = main_gui.mp4_win

        self.config_parser = ConfigParser()
        self.config_parser.read(config_file)

        self.__check_theme()

    def __check_theme(self):
        """define theme parameters based off of config selection"""
        if self.config_parser["theme"]["selected_theme"] == "system_default":
            self.colors = SystemTheme(main_gui=self)

            self.custom_window_bg_color = self.colors.custom_window_bg_color
            self.custom_button_colors = self.colors.custom_button_colors
            self.custom_entry_colors = self.colors.custom_entry_colors
            self.custom_label_frame_colors = self.colors.custom_label_frame_colors
            self.custom_frame_bg_colors = self.colors.custom_frame_bg_colors
            self.custom_label_colors = self.colors.custom_label_colors
            self.custom_scrolled_text_widget_color = (
                self.colors.custom_scrolled_text_widget_color
            )
            self.custom_listbox_color = self.colors.custom_listbox_color
            self.custom_spinbox_color = self.colors.custom_spinbox_color
            self.custom_text_color = self.colors.custom_text_color

        else:
            if self.config_parser["theme"]["selected_theme"] == "bhd_theme":
                values = bhd_theme.BHDTheme()

            self.__theme(values)

    def __theme(self, values):
        self.custom_window_bg_color = values.custom_window_bg_color
        self.custom_button_colors = values.custom_button_colors
        self.custom_entry_colors = values.custom_entry_colors
        self.custom_label_frame_colors = values.custom_label_frame_colors
        self.custom_frame_bg_colors = values.custom_frame_bg_colors
        self.custom_label_colors = values.custom_label_colors
        self.custom_scrolled_text_widget_color = (
            values.custom_scrolled_text_widget_color
        )
        self.custom_listbox_color = values.custom_listbox_color
        self.custom_spinbox_color = values.custom_spinbox_color
        self.custom_text_color = values.custom_text_color
