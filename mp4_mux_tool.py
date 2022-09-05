import pathlib
import subprocess
import webbrowser
from ctypes import windll
from tkinter import filedialog, StringVar, ttk, messagebox, PhotoImage, Menu, LabelFrame, E, N, S, W, Label, \
    Entry, DISABLED, NORMAL, END, Frame, SUNKEN, Button

from tkinterdnd2 import TkinterDnD, DND_FILES
from pymediainfo import MediaInfo
from packages.iso_639_2 import *
from packages.about import openaboutwindow
from packages.chapterdemuxer import ChapterDemux
from packages.base64_images import icon_image
from packages.config_params import *
from packages.config_writer import config_writer
from packages.hoverbutton import HoverButton
from packages.style import GuiStyle
from packages.main_menu import MainMenu
from packages.video_frame import VideoSection
from packages.audio_frame import AudioSection
from packages.subtitle_frame import SubtitleSection
from packages.chapter_frame import ChapterSection
from packages.output_frame import OutputSection
from packages.progress_window import ProgressWindow
from packages.show_command import ShowCommand
from packages.apps import BundledApps


# Block of code to fix DPI awareness issues on Windows 7 or higher
try:
    windll.shcore.SetProcessDpiAwareness(2)  # if your Windows version >= 8.1
except(Exception,):
    windll.user32.SetProcessDPIAware()  # Windows 8.0 or less
# Block of code to fix DPI awareness issues on Windows 7 or higher


class MainGui:

    def __init__(self, master):
        self.mp4_win = master
        self.mp4_win.title("MP4-Mux-Tool v1.13")
        self.mp4_win.iconphoto(True, PhotoImage(data=icon_image))
        self.mp4_win.configure(background="#434547")
        self.window_height = 800
        self.window_width = 800
        self.screen_width = self.mp4_win.winfo_screenwidth()
        self.screen_height = self.mp4_win.winfo_screenheight()
        self.x_coordinate = int((self.screen_width / 2) - (self.window_width / 2))
        self.y_coordinate = int((self.screen_height / 2) - (self.window_height / 2))
        self.mp4_win.geometry(f'{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}')
        self.mp4_win.protocol('WM_DELETE_WINDOW', self.mp4_win_exit_function)

        for mp4_c in range(3):
            self.mp4_win.grid_columnconfigure(mp4_c, weight=1)
        for mp4_r in range(6):
            self.mp4_win.grid_rowconfigure(mp4_r, weight=1)
            
        self.style_instance = GuiStyle(main_gui=self)
        self.main_menu_instance = MainMenu(main_gui=self)
        self.video_section_instance = VideoSection(main_gui=self)
        self.audio_section_instance = AudioSection(main_gui=self)
        self.subtitle_section_instance = SubtitleSection(main_gui=self)
        self.chapter_section_instance = ChapterSection(main_gui=self)
        self.output_section_instance = OutputSection(main_gui=self)
        self.bundled_apps_instance = BundledApps(main_gui=self)


        self.show_command = HoverButton(self.mp4_win, text='View Command', command=lambda: ShowCommand, foreground='white',
                                   background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
        self.show_command.grid(row=5, column=0, columnspan=1, padx=(20, 10), pady=(15, 2), sticky=W)


        self.status_label = Label(self.mp4_win, text='Select "Open File" or drag and drop a video file to begin',
                             bd=4, relief=SUNKEN, anchor=E, background='#717171', foreground="white")
        self.status_label.grid(column=0, row=6, columnspan=4, sticky=W + E, pady=(0, 2), padx=3)

        # def auto_chap_checkbtn_on_enter(e):
        #     self.status_label.configure(text='Import embedded chapter file from video input')
        #
        # def auto_chap_checkbtn_on_leave(e):
        #     self.status_label.configure(text='')
        #
        # self.auto_chap_import_checkbox.bind("<Enter>", auto_chap_checkbtn_on_enter)
        # self.auto_chap_import_checkbox.bind("<Leave>", auto_chap_checkbtn_on_leave)

    def mp4_win_exit_function(self):
        self.mp4_win.destroy()
        """FIX THIS WITH PSTUL"""

        # confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
        #                                                            "     Note: This will end all current tasks!",
        #                                    parent=self.mp4_win)
        # if confirm_exit:  # If user selects 'Yes', program attempts to kill all tasks then closes GUI
        #     try:
        #         subprocess.Popen(f"TASKKILL /F /im MP4-Mux-Tool.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
        #         self.mp4_win.destroy()
        #     except (Exception,):
        #         self.mp4_win.destroy()
        
        
        
        #
        # Status Label at bottom of main GUI ----------------------------------------------------------------- The status
        # label just updates based on the mouse cursor location, when you go over certain buttons it'll give you information
        # based on that location


        # ----------------------------------------------------------------- Status Label at bottom of main GUI

# class HoverButton(Button):
#     """simple class to convert button to a hoverbutton"""
#
#     def __init__(self, master, **kw):
#         Button.__init__(self, master=master, **kw)
#         self.defaultBackground = self["background"]
#         self.bind("<Enter>", self.on_enter)
#         self.bind("<Leave>", self.on_leave)
#
#     def on_enter(self, e):
#         self["background"] = self["activebackground"]
#         # if self.cget("text") == "Video":
#         #     self.status_label.configure(text='Video inputs supported (.avi, .mp4, .m1v/.m2v, .m4v, .264, .h264, .hevc, or '
#         #                                 '.h265)')
#         # if self.cget("text") == "Audio":
#         #     self.status_label.configure(text='Audio inputs supported (.ac3, .aac, .mp4, .m4a, .mp2, .mp3, .opus, or .ogg)')
#         # if self.cget("text") == "Subtitle":
#         #     self.status_label.configure(text='Subtitle inputs supported (.srt, .idx, .ttxt)')
#         # if self.cget("text") == "Chapter":
#         #     self.status_label.configure(text='Chapter input supported OGG (.txt)')
#         # if self.cget("text") == "Output":
#         #     self.status_label.configure(text='Select File Save Location (*.mp4)')
#         # if self.cget("text") == "X":
#         #     self.status_label.configure(text='Remove input and settings')
#         # if self.cget("text") == "View Command":
#         #     self.status_label.configure(text='Select to show complete command line')
#         # if self.cget("text") == "Mux":
#         #     self.status_label.configure(text='Select to begin muxing')
#
#     def on_leave(self, e):
#         self["background"] = self.defaultBackground
#         # self.status_label.configure(text="")



if __name__ == "__main__":
    root = TkinterDnD.Tk()
    MainGui(root)
    root.mainloop()
