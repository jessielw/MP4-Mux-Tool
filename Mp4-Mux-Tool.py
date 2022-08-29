import pathlib
import pyperclip
import subprocess
import threading
import tkinter as tk
import tkinter.scrolledtext as scrolledtextwidget
import webbrowser
from ctypes import windll
from tkinter import filedialog, StringVar, ttk, messagebox, PhotoImage, Menu, LabelFrame, E, N, S, W, Label, \
    Entry, DISABLED, NORMAL, END, Frame, Spinbox, CENTER, Checkbutton, HORIZONTAL, Toplevel, SUNKEN, OptionMenu, Button

from tkinterdnd2 import TkinterDnD, DND_FILES
from pymediainfo import MediaInfo
from ISO_639_2 import *
from packages.about import openaboutwindow
from packages.chapterdemuxer import ChapterDemux
from packages.base64images import icon_image
from packages.configparams import *
from packages.configwriter import config_writer


# Block of code to fix DPI awareness issues on Windows 7 or higher
try:
    windll.shcore.SetProcessDpiAwareness(2)  # if your Windows version >= 8.1
except(Exception,):
    windll.user32.SetProcessDPIAware()  # Windows 8.0 or less
# Block of code to fix DPI awareness issues on Windows 7 or higher


class MainGui:

    def __init__(self, mp4_win):
        self.mp4_win = mp4_win
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
            
        custom_style = ttk.Style()
        custom_style.theme_create('jlw_style', parent='alt', settings={
            # Notebook Theme Settings -------------------
            "TNotebook": {"configure": {"tabmargins": [5, 5, 5, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": 'grey', 'foreground': 'white', 'focuscolor': ''},
                "map": {"background": [("selected", '#434547')], "expand": [("selected", [1, 1, 1, 0])]}},
            # Notebook Theme Settings -------------------
            # ComboBox Theme Settings -------------------
            'TCombobox': {'configure': {'selectbackground': '#23272A', 'fieldbackground': '#23272A',
                                        'background': 'white', 'foreground': 'white'}}}
                                  # ComboBox Theme Settings -------------------
                                  )
        custom_style.theme_use('jlw_style')  # Enable the use of the custom theme
        # ComboBox Mouse Hover Code ----------------------------------
        self.mp4_win.option_add('*TCombobox*Listbox*Background', '#404040')
        self.mp4_win.option_add('*TCombobox*Listbox*Foreground', '#FFFFFF')
        self.mp4_win.option_add('*TCombobox*Listbox*selectBackground', '#FFFFFF')
        self.mp4_win.option_add('*TCombobox*Listbox*selectForeground', '#404040')
        custom_style.map('TCombobox', foreground=[('hover', 'white')], background=[('hover', 'grey')])
        custom_style.configure("purple.Horizontal.TProgressbar", background='purple')

        # create menu bar
        self.my_menu_bar = Menu(self.mp4_win, tearoff=0)
        self.mp4_win.config(menu=self.my_menu_bar)

        # create File menu
        self.file_menu = Menu(self.my_menu_bar, tearoff=0, activebackground='dim grey')
        self.my_menu_bar.add_cascade(label='File', menu=self.file_menu)

        ##
        ##
        ##
        self.file_menu.add_command(label='Clear Inputs', command=self.clear_inputs)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.mp4_win_exit_function)

        self.options_menu = Menu(self.my_menu_bar, tearoff=0, activebackground='dim grey')
        self.my_menu_bar.add_cascade(label='Options', menu=self.options_menu)

        self.options_submenu = Menu(self.mp4_win, tearoff=0, activebackground='dim grey')
        self.options_menu.add_cascade(label='Shell Options', menu=self.options_submenu)
        
        self.shell_options = StringVar()
        self.shell_options.set(config['debug_option']['option'])
        if self.shell_options.get() == '':
            self.shell_options.set('Default')
        elif self.shell_options.get() != '':
            self.shell_options.set(config['debug_option']['option'])
        config_writer(config_file, 'debug_option', 'option', self.shell_options.get())

        self.options_submenu.add_radiobutton(label='Progress Bars', variable=self.shell_options, value="Default",
                                        command=lambda: config_writer(config_file, 'debug_option', 'option', self.shell_options.get()))
        self.options_submenu.add_radiobutton(label='CMD Shell (Debug)', variable=self.shell_options, value="Debug",
                                        command=lambda: config_writer(config_file, 'debug_option', 'option', self.shell_options.get()))

        self.auto_close_window = StringVar()
        self.auto_close_window.set(config['auto_close_progress_window']['option'])
        if self.auto_close_window.get() == '':
            self.auto_close_window.set('on')
        elif self.auto_close_window.get() != '':
            self.auto_close_window.set(config['auto_close_progress_window']['option'])

        config_writer(config_file, 'auto_close_progress_window', 'option', self.auto_close_window.get())
        self.options_submenu2 = Menu(self.mp4_win, tearoff=0, activebackground='dim grey')
        self.options_menu.add_cascade(label='Auto-Close Progress Window On Completion', menu=self.options_submenu2)
        self.options_submenu2.add_radiobutton(label='On', variable=self.auto_close_window, value='on', command=lambda: config_writer(config_file, 'auto_close_progress_window', 'option', self.auto_close_window.get()))
        self.options_submenu2.add_radiobutton(label='Off', variable=self.auto_close_window, value='off',
                                         command=lambda: config_writer(config_file, 'auto_close_progress_window', 'option', self.auto_close_window.get()))

        self.reset_gui_on_start = StringVar()
        self.reset_gui_on_start.set(config['reset_program_on_start_job']['option'])
        if self.reset_gui_on_start.get() == '':
            self.reset_gui_on_start.set('on')
        elif self.reset_gui_on_start.get() != '':
            self.reset_gui_on_start.set(config['reset_program_on_start_job']['option'])
        config_writer(config_file, 'reset_program_on_start_job', 'option', self.reset_gui_on_start.get())

        self.options_submenu3 = Menu(self.mp4_win, tearoff=0, activebackground='dim grey')
        self.options_menu.add_cascade(label='Reset GUI When Start Job Is Selected', menu=self.options_submenu3)
        self.options_submenu3.add_radiobutton(label='On', variable=self.reset_gui_on_start, value='on',
                                         command=lambda: config_writer(config_file, 'reset_program_on_start_job', 'option', self.reset_gui_on_start.get()))
        self.options_submenu3.add_radiobutton(label='Off', variable=self.reset_gui_on_start, value='off',
                                         command=lambda: config_writer(config_file, 'reset_program_on_start_job', 'option', self.reset_gui_on_start.get()))

        self.options_menu.add_separator()
        self.options_menu.add_command(label='Set path to MP4Box', command=self.set_mp4box_path)
        self.options_menu.add_command(label='Set path to mkvextract', command=self.set_mkvextract_path)
        self.options_menu.add_separator()
        self.options_menu.add_command(label='Reset Configuration File', command=self.reset_config)

        self.tools_menu = Menu(self.my_menu_bar, tearoff=0, activebackground="dim grey")
        self.my_menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label='Chapter Demuxer', command=lambda: ChapterDemux(master=self.mp4_win, standalone=False))

        self.help_menu = Menu(self.my_menu_bar, tearoff=0, activebackground="dim grey")
        self.my_menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=openaboutwindow)

        self.video_frame = LabelFrame(self.mp4_win, text=' Video ')
        self.video_frame.grid(row=0, columnspan=3, sticky=E + W + N + S, padx=20, pady=(5, 0))
        self.video_frame.configure(fg="white", bg="#434547", bd=4)

        self.video_frame.grid_columnconfigure(0, weight=1)
        self.video_frame.grid_rowconfigure(0, weight=1)

        self.tabs = ttk.Notebook(self.video_frame, height=110)
        self.tabs.grid(row=0, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)
        self.video_tab = Frame(self.tabs, background="#434547")
        self.video_tab2 = Frame(self.tabs, background="#434547")
        self.tabs.add(self.video_tab, text=' Input ')
        self.tabs.add(self.video_tab2, text=' Options ')

        for vt_c in range(4):
            self.video_tab.grid_columnconfigure(vt_c, weight=1)
        for vt_r in range(3):
            self.video_tab.grid_rowconfigure(vt_r, weight=1)

        self.video_title_cmd = StringVar()
        self.video_title_entry_label = Label(self.video_tab, text='Video Title:', anchor=W, background='#434547',
                                           foreground='white')
        self.video_title_entry_label.grid(row=1, column=1, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        self.video_title_entry = Entry(self.video_tab, textvariable=self.video_title_cmd, borderwidth=4,
                                       background='#CACACA', state=DISABLED)
        self.video_title_entry.grid(row=2, column=1, columnspan=1, padx=(5, 15), pady=(0, 15), sticky=W + E)

        self.input_dnd = StringVar()
        self.input_dnd.trace('w', update_file_input)
        self.input_dnd = HoverButton(self.video_tab, text='Video', command=input_button_commands, foreground='white',
                                   background='#23272A', borderwidth='3', activebackground='grey', width=15)
        self.input_dnd.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=W + E)
        self.input_dnd.drop_target_register(DND_FILES)
        self.input_dnd.dnd_bind('<<Drop>>', video_drop_input)

        self.input_entry = Entry(self.video_tab, borderwidth=4, background='#CACACA', state=DISABLED, width=40)
        self.input_entry.grid(row=0, column=1, columnspan=2, padx=(5, 0), pady=5, sticky=W + E)
        self.input_entry.drop_target_register(DND_FILES)
        self.input_entry.dnd_bind('<<Drop>>', video_drop_input)

        self.delete_input_button = HoverButton(self.video_tab, text='X', command=clear_video_input, foreground='white',
                                          background='#23272A', borderwidth='3', activebackground='grey', width=2)
        self.delete_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=5, sticky=E)

        # FIX
        # def video_title(*args):
        #     global video_title_cmd_input
        #     if self.video_title_cmd.get().strip() == '':  # If title box string is empty or only white space
        #         video_title_cmd_input = ':name='  # .strip() is used to remove all white space from left or right of a string
        #     else:  # If title box string has characters
        #         video_title_cmd_input = ':name=' + self.video_title_cmd.get().strip()
        #
        # self.video_title_cmd.trace('w', video_title)
        # self.video_title_cmd.set('')

        # # Video FPS Selection -----------------------------------------------------------------------------------------------
        # video_fps = StringVar()
        # video_fps_choices = {'Automatic': '',
        #                      '23.976': '-fps 23.976',
        #                      '24': '-fps 24',
        #                      '25': '-fps 25',
        #                      '29.97': '-fps 29.97',
        #                      '30': '-fps 30',
        #                      '50': '-fps 50',
        #                      '59.94': '-fps 59.94',
        #                      '60': '-fps 60'}
        # self.video_fps_menu_label = Label(self.video_tab, text='Framerate (FPS):', background="#434547", foreground="white")
        # self.video_fps_menu_label.grid(row=1, column=3, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        # combo_fps = ttk.Combobox(self.video_tab, values=list(video_fps_choices.keys()), justify="center",
        #                          textvariable=video_fps, width=10)
        # combo_fps.grid(row=2, column=3, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
        # combo_fps['state'] = 'readonly'
        # combo_fps.current(0)

        # Video FPS Label is only for viewing purposes, you need input FPS for program to know what fps to output
        self.video_fps_menu_label = Label(self.video_tab, text='Framerate (FPS):', background="#434547", foreground="white")
        self.video_fps_menu_label.grid(row=1, column=2, columnspan=1, padx=(3, 0), pady=(0, 0), sticky=W)
        self.fps_entry = Entry(self.video_tab, borderwidth=4, background='#CACACA', state=DISABLED, width=10)
        self.fps_entry.grid(row=2, column=2, columnspan=2, padx=(5, 10), pady=(0, 15), sticky=W + E)

        self.video_language = StringVar()
        self.video_language_menu_label = Label(self.video_tab, text='Language:', background="#434547", foreground="white")
        self.video_language_menu_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        self.video_combo_language = ttk.Combobox(self.video_tab, values=list(iso_639_2_codes_dictionary.keys()),
                                            justify="center",
                                            textvariable=self.video_language, width=15)
        self.video_combo_language.grid(row=2, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=W + E + N + S)
        self.video_combo_language['state'] = 'readonly'
        self.video_combo_language.current(0)  # Sets language to index 0 (UND) by default

        # Dolby Vision ---------------------------------------------------------------------------------------------
        self.dolby_profiles = {'None': '', 'Profile 5': ':dv-profile=5:hdr=none',
                          'Profile 8.1 (HDR10)': ':dv-profile=8.hdr10:hdr=none',
                          'Profile 8.2 (bt709)': ':dv-profile=8.bt709:hdr=none'}
        self.dolby_v_profile = StringVar()
        self.dolby_v_profile_menu_label = Label(self.video_tab2, text='Dolby Vision:', background="#434547",
                                           foreground="white")
        self.dolby_v_profile_menu_label.grid(row=0, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        self.dolby_v_profile_combo = ttk.Combobox(self.video_tab2, values=list(self.dolby_profiles.keys()), justify="center",
                                             textvariable=self.dolby_v_profile, width=20)
        self.dolby_v_profile_combo.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=W + E + N + S)
        self.dolby_v_profile_combo['state'] = 'readonly'
        self.dolby_v_profile_combo.current(0)  # Sets profile to index 0 ('') by default
        
        
        
        
        
        
        # AUDIO TAB
        self.audio_frame = LabelFrame(self.mp4_win, text=' Audio ')
        self.audio_frame.grid(row=1, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
        self.audio_frame.configure(fg="white", bg="#434547", bd=4)

        self.audio_frame.grid_columnconfigure(0, weight=1)
        self.audio_frame.grid_rowconfigure(0, weight=1)

        self.tabs = ttk.Notebook(self.audio_frame, height=110)
        self.tabs.grid(row=0, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)
        self.audio_tab = Frame(self.tabs, background="#434547")
        self.tabs.add(self.audio_tab, text=' Track #1 ')

        for n in range(4):
            self.audio_tab.grid_columnconfigure(n, weight=1)
        for n in range(3):
            self.audio_tab.grid_rowconfigure(n, weight=1)

        # def audio_title(*args):
        #     global audio_title_cmd_input
        #     if self.audio_title_cmd.get().strip() == '':
        #         audio_title_cmd_input = ':name='
        #     else:
        #         audio_title_cmd_input = ':name=' + self.audio_title_cmd.get().strip()

        self.audio_title_cmd = StringVar()
        self.audio_title_entry_label = Label(self.audio_tab, text='Audio Title:', anchor=W, background='#434547',
                                           foreground='white')
        self.audio_title_entry_label.grid(row=1, column=1, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        self.audio_title_entry = Entry(self.audio_tab, textvariable=self.audio_title_cmd, borderwidth=4, background='#CACACA',
                                     state=DISABLED)
        self.audio_title_entry.grid(row=2, column=1, columnspan=1, padx=10, pady=(0, 15), sticky=W + E)
        # self.audio_title_cmd.trace('w', audio_title)
        # self.audio_title_cmd.set('')

        self.audio_delay = StringVar()
        self.audio_delay_label = Label(self.audio_tab, text="Delay:", background="#434547", foreground="white")
        self.audio_delay_label.grid(row=1, column=3, columnspan=1, padx=10, pady=1, sticky=W)
        self.audio_delay_spinbox = Spinbox(self.audio_tab, from_=0, to=20000, increment=1.0, justify=CENTER,
                                      wrap=True, textvariable=self.audio_delay, width=14)
        self.audio_delay_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", readonlybackground="#23272A")
        self.audio_delay_spinbox.grid(row=2, column=3, columnspan=1, padx=10, pady=(1, 8), sticky=W)
        self.audio_delay.set(0)

        self.audio_language = StringVar()
        self.audio_language_menu_label = Label(self.audio_tab, text='Language:', background="#434547", foreground="white")
        self.audio_language_menu_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        self.audio_language = ttk.Combobox(self.audio_tab, values=list(iso_639_2_codes_dictionary.keys()), justify="center",
                                      textvariable=self.audio_language)
        self.audio_language.grid(row=2, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
        self.audio_language['state'] = 'readonly'
        self.audio_language.current(0)

    # # Audio Stream Selection ----------------------------------------------------------------------------------
    # def check_audio_tracks_info():
    #     global audio_input
    # 
    #     def audio_track_choice():  # If audio input has only 1 audio track
    #         global acodec_stream, acodec_stream_choices
    #         media_info = MediaInfo.parse(audio_input)  # Uses pymediainfo to get information for track selection
    #         for track in media_info.tracks:
    #             if track.track_type == 'Audio':
    #                 audio_track_id_get = str(track.track_id)  # Code to save track # into a variable
    #         acodec_stream = StringVar()  # Makes a new variable
    #         acodec_stream_choices = {'Only One Track': f'#{audio_track_id_get}'}  # Temp dictionary with audio track ID
    #         acodec_stream.set('Only One Track')  # Sets variable to select #1 for command line
    # 
    #     def audio_track_choices(
    #             *args):  # If audio input has more then 2 audio tracks, makes a new window to select track
    #         global acodec_stream, acodec_stream_choices
    #         audio_track_win = Toplevel()  # Toplevel window
    #         audio_track_win.configure(background='#191a1a')  # Set color of audio_track_win background
    #         window_height = 180  # win height
    #         window_width = 480  # win width
    #         screen_width = audio_track_win.winfo_screenwidth()  # down
    #         screen_height = audio_track_win.winfo_screenheight()  # down
    #         x_coordinate = int((screen_width / 2) - (window_width / 2))  # down
    #         y_coordinate = int((screen_height / 2) - (window_height / 2))  # down
    #         audio_track_win.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')  # code calculates
    #         # middle position of window
    #         audio_track_win.resizable(0, 0)  # makes window not resizable
    #         audio_track_win.overrideredirect(1)  # will remove the top badge of window
    #         audio_track_win.grab_set()  # forces audio_track_win to stay on top of root
    #         self.mp4_win.attributes('-alpha', 0.8)  # Lowers mp4root transparency to .8
    # 
    #         # Input Frame -------------------------------------------------------------------------------------------------
    #         track_frame = LabelFrame(audio_track_win, text=' Track Selection ')
    #         track_frame.grid(row=0, column=0, columnspan=5, sticky=E + W, padx=10, pady=(8, 0))
    #         track_frame.configure(fg="white", bg="#636669", bd=3)
    # 
    #         track_frame.rowconfigure(0, weight=1)
    #         track_frame.grid_columnconfigure(0, weight=1)
    #         # ------------------------------------------------------------------------------------------------- Input Frame
    # 
    #         # Code to gather multiple audio tracks information for use with the gui ---------------------------------------
    #         result = []  # Creates an empty list to be filled with the code below
    #         media_info = MediaInfo.parse(audio_input)  # Uses pymediainfo to get information for track selection
    #         for track in media_info.tracks:
    #             if track.track_type == 'Audio':
    #                 if str(track.format) != 'None':  # Gets format string of tracks (aac, ac3 etc...)
    #                     audio_format = '|  ' + str(track.format) + '  |'
    #                 else:
    #                     audio_format = ''
    #                 if str(track.channel_s) != 'None':  # Gets audio channels of input tracks
    #                     audio_channels = '|  ' + 'Channels: ' + str(track.channel_s) + '  |'
    #                 else:
    #                     audio_channels = ''
    #                 if str(track.other_bit_rate) != 'None':  # Gets audio bitrate of input tracks
    #                     audio_bitrate = '|  ' + str(track.other_bit_rate).replace('[', '') \
    #                         .replace(']', '').replace("'", '') + '  |'
    #                 else:
    #                     audio_bitrate = ''
    #                 if str(track.other_language) != 'None':  # Gets audio language of input tracks
    #                     self.audio_language = '|  ' + str(track.other_language[0]) + '  |'
    #                 else:
    #                     self.audio_language = ''
    #                 if str(track.title) != 'None':  # Gets audio title of input tracks
    #                     if len(str(track.title)) > 50:  # Counts title character length
    #                         audio_title = '|  Title: ' + str(track.title)[:50] + '...  |'  # If title > 50 characters
    #                     else:
    #                         audio_title = '|  Title: ' + str(track.title) + '  |'  # If title is < 50 characters
    #                 else:
    #                     audio_title = ''
    #                 if str(track.other_sampling_rate) != 'None':  # Gets audio sampling rate of input tracks
    #                     audio_sampling_rate = '|  ' + str(track.other_sampling_rate) \
    #                         .replace('[', '').replace(']', '').replace("'", '') + '  |'
    #                 else:
    #                     audio_sampling_rate = ''
    #                 if str(track.other_duration) != 'None':  # Gets audio duration of input tracks
    #                     audio_duration = '|  ' + str(track.other_duration[0]) + '  |'
    #                 else:
    #                     audio_duration = ''
    #                 if str(track.delay) != 'None':  # Gets audio delay of input tracks
    #                     if str(track.delay) == '0':
    #                         self.audio_delay = ''
    #                     else:
    #                         self.audio_delay = '|  Delay: ' + str(track.delay) + '  |'
    #                 else:
    #                     self.audio_delay = ''
    #                 if str(track.track_id) != 'None':  # Gets track ID of audio inputs (this is needed for mp4box input)
    #                     audio_track_id = '|  ID: ' + str(track.track_id) + '  |'  # Code for viewing in drop down
    #                     audio_track_id_get = str(track.track_id)  # Code to save track # into a variable
    #                 else:
    #                     messagebox.showerror(title='Error!', message='Cannot auto detect track ID')
    #                 audio_track_info = audio_format + audio_channels + audio_bitrate + audio_sampling_rate + \
    #                                    self.audio_delay + audio_duration + self.audio_language + audio_title + audio_track_id
    #                 print(audio_track_info)
    #                 for new_list in [audio_track_info]:  # Take all the pymedia input and adds it into a list
    #                     result.append(new_list)
    #         # ---------------------------------------- Code to gather all the audio tracks information for use with the gui
    # 
    #         # Code to take all the information from the newly created list(s) and put it into a dictionary ----------------
    #         audio_stream_info_output = {}
    #         for i in range(int(str(total_audio_tracks)[-1])):
    #             audio_stream_info_output[f'Track #{i + 1}:   {result[i]}'] = f'#{audio_track_id_get}'
    #         # ---------------- Code to take all the information from the newly created list(s) and put it into a dictionary
    # 
    #         # Code uses the above dictionary to create a drop-down menu of audio tracks to display/select included track --
    #         acodec_stream = StringVar()
    #         acodec_stream_choices = audio_stream_info_output
    #         acodec_stream.set(next(iter(audio_stream_info_output)))  # set the default option
    #         acodec_stream_menu = OptionMenu(track_frame, acodec_stream, *acodec_stream_choices.keys())
    #         acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=48,
    #                                   anchor='w')
    #         acodec_stream_menu.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
    #         acodec_stream_menu["menu"].configure(activebackground="dim grey")
    # 
    #         # -- Code uses the above dictionary to create a drop-down menu of audio tracks to display/select included track
    # 
    #         # Saves audio window and closes it while restoring transparency of main GUI -----------------------------------
    #         def close_audio_win():
    #             self.mp4_win.attributes('-alpha', 1.0)  # Restores mp4root transparency to default
    #             audio_track_win.grab_release()
    #             audio_track_win.destroy()  # Closes audio window
    # 
    #         select_track = HoverButton(track_frame, text="Choose Track", command=close_audio_win, foreground="white",
    #                                    background="#23272A", borderwidth="3", activebackground='grey')
    #         select_track.grid(row=1, column=0, columnspan=1, padx=5, pady=(60, 5), sticky=N + S + E + W)
    #         # ----------------------------------- Saves audio window and closes it while restoring transparency of main GUI
    # 
    #     media_info = MediaInfo.parse(audio_input)
    #     for track in media_info.tracks:
    #         if track.track_type == 'General':
    #             total_audio_tracks = track.count_of_audio_streams
    #     if total_audio_tracks is not None and int(total_audio_tracks) == 1:
    #         audio_track_choice()  # Starts single track function
    #     elif total_audio_tracks is not None and int(total_audio_tracks) >= 2:
    #         audio_track_choices()  # Starts function for more than 1 track
    #     else:  # If the input has 0 audio tracks it resets the audio frame gui back to default/none
    #         self.audio_delay.set(0)
    #         self.audio_language.current(0)
    #         self.audio_title_entry.delete(0, END)
    #         self.audio_input_entry.configure(state=NORMAL)
    #         self.audio_input_entry.delete(0, END)
    #         self.audio_input_entry.configure(state=DISABLED)
    #         # Error message explaining why file input failed
    #         messagebox.showinfo(title='Info', message=f'"{pathlib.Path(audio_input).name}"\n\nhas 0 audio streams, '
    #                                                   f'please open a file with at least 1 audio stream.')
    #         del audio_input

    def audio_input_button_commands(self):  # Function for audio input button
        return
        # global audio_input, audio_input_quoted
        audio_extensions = ('.ac3', '.aac', '.mp4', '.m4a', '.mp2', '.mp3', '.opus', '.ogg')
        audio_input = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                 filetypes=[("Supported Formats", audio_extensions)])
        if audio_input:
            self.audio_input_entry.configure(state=NORMAL)
            self.audio_input_entry.delete(0, END)
            if audio_input.endswith(audio_extensions):
                audio_input_quoted = '"' + str(pathlib.Path(audio_input)) + '"'
                self.audio_input_entry.insert(0, audio_input)
                self.audio_input_entry.configure(state=DISABLED)
                self.audio_title_entry.configure(state=NORMAL)
                media_info = MediaInfo.parse(audio_input)
                for track in media_info.tracks:
                    if track.track_type == 'Audio':
                        try:  # Uses mediainfo to detect the language of the file and converts it to 3-digit code
                            detect_index = [len(i) for i in track.other_language].index(3)
                            language_index = list(iso_639_2_codes_dictionary.values()).index(
                                track.other_language[detect_index])
                            self.audio_language.current(language_index)
                            self.audio_title_entry.delete(0, END)
                            self.audio_title_entry.insert(0, track.title)
                        except(Exception,):
                            pass
                check_audio_tracks_info()  # Function to get audio input from input file
            else:  # If file opened isn't a supported format
                messagebox.showinfo(title='Input Not Supported',
                                    message="Try Again With a Supported File Type!\n\nIf this is a "
                                            "file that should be supported, please let me know.\n\n"
                                            + 'Unsupported file extension "' + str(
                                        pathlib.Path(audio_input).suffix) + '"')
                self.audio_delay.set(0)
                self.audio_language.current(0)
                self.audio_title_entry.delete(0, END)
                del audio_input
    # 
    # def update_audio_input(*args):  # Drag and drop function for audio input
    #     global audio_input, audio_input_quoted
    #     self.audio_input_entry.configure(state=NORMAL)
    #     self.audio_input_entry.delete(0, END)
    #     audio_input = str(self.audio_input_dnd.get()).replace("{", "").replace("}", "")
    #     audio_extensions = ('.ac3', '.aac', '.mp4', '.m4a', '.mp2', '.mp3', '.opus', '.ogg')
    #     if audio_input.endswith(audio_extensions):
    #         audio_input_quoted = '"' + str(pathlib.Path(audio_input)) + '"'
    #         self.audio_input_entry.insert(0, audio_input)
    #         self.audio_input_entry.configure(state=DISABLED)
    #         self.audio_title_entry.configure(state=NORMAL)
    #         media_info = MediaInfo.parse(audio_input)
    #         for track in media_info.tracks:
    #             if track.track_type == 'Audio':
    #                 try:
    #                     detect_index = [len(i) for i in track.other_language].index(3)
    #                     language_index = list(iso_639_2_codes_dictionary.values()).index(
    #                         track.other_language[detect_index])
    #                     self.audio_language.current(language_index)
    #                     self.audio_title_entry.delete(0, END)
    #                     self.audio_title_entry.insert(0, track.title)
    #                 except(Exception,):
    #                     pass
    #         check_audio_tracks_info()  # Function to get audio input from input file
    #     else:  # If file opened isn't a supported format
    #         messagebox.showinfo(title='Input Not Supported',
    #                             message="Try Again With a Supported File Type!\n\nIf this is a "
    #                                     "file that should be supported, please let me know.\n\n"
    #                                     + 'Unsupported file extension "' + str(pathlib.Path(audio_input).suffix) + '"')
    #         self.audio_delay.set(0)
    #         self.audio_language.current(0)
    #         self.audio_title_entry.delete(0, END)
    #         del audio_input

        # def audio_drop_input(event):  # Drag and drop function for audio input
        #     self.audio_input_dnd.set(event.data)
        # 
        # 
        # def clear_audio_input():  # Deletes all inputs and sets defaults for audio box #1
        #     global audio_input, self.audio_title_cmd, self.audio_title_entry, self.audio_delay, self.audio_input_entry
        #     try:
        #         self.audio_title_cmd = ''
        #         self.audio_title_entry.delete(0, END)
        #         self.audio_title_entry.configure(state=DISABLED)
        #         self.audio_input_entry.configure(state=NORMAL)
        #         self.audio_input_entry.delete(0, END)
        #         self.audio_input_entry.configure(state=DISABLED)
        #         del audio_input
        #         self.audio_language.current(0)
        #         self.audio_delay.set(0)
        #     except (Exception,):
        #         pass

        self.audio_input_dnd = StringVar()
        # self.audio_input_dnd.trace('w', update_audio_input)
        self.audio_input_button = HoverButton(self.audio_tab, text='Audio', command=audio_input_button_commands,
                                         foreground='white',
                                         background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
        self.audio_input_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)
        self.audio_input_button.drop_target_register(DND_FILES)
        self.audio_input_button.dnd_bind('<<Drop>>', audio_drop_input)
    
        self.audio_input_entry = Entry(self.audio_tab, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
        self.audio_input_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)
        self.audio_input_entry.drop_target_register(DND_FILES)
        self.audio_input_entry.dnd_bind('<<Drop>>', audio_drop_input)
        
        self.delete_audio_input_button = HoverButton(self.audio_tab, text='X', command=clear_audio_input, foreground='white',
                                                background='#23272A', borderwidth='3', activebackground='grey', width=2)
        self.delete_audio_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)







        self.subtitle_frame = LabelFrame(self.mp4_win, text=' Subtitle ')
        self.subtitle_frame.grid(row=2, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
        self.subtitle_frame.configure(fg="white", bg="#434547", bd=4)

        self.subtitle_frame.grid_columnconfigure(0, weight=1)
        self.subtitle_frame.grid_rowconfigure(0, weight=1)

        self.tabs = ttk.Notebook(self.subtitle_frame, height=110)
        self.tabs.grid(row=0, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)
        self.subtitle_tab = Frame(self.tabs, background="#434547")
        self.tabs.add(self.subtitle_tab, text=' Track #1 ')

        for n in range(4):
            self.subtitle_tab.grid_columnconfigure(n, weight=1)
        for n in range(3):
            self.subtitle_tab.grid_rowconfigure(n, weight=1)

        # def subtitle_title(*args):
        #     global subtitle_title_cmd_input
        #     if self.subtitle_title_cmd.get().strip() == '':
        #         subtitle_title_cmd_input = ':name='
        #     else:
        #         subtitle_title_cmd_input = ':name=' + self.subtitle_title_cmd.get().strip()

        self.subtitle_title_cmd = StringVar()
        self.subtitle_title_entry_label = Label(self.subtitle_tab, text='Subtitle Title:', anchor=W, background='#434547',
                                              foreground='white')
        self.subtitle_title_entry_label.grid(row=1, column=1, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        self.subtitle_title_entry = Entry(self.subtitle_tab, textvariable=self.subtitle_title_cmd, borderwidth=4,
                                        background='#CACACA',
                                        state=DISABLED)
        self.subtitle_title_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
        # self.subtitle_title_cmd.trace('w', subtitle_title)
        # self.subtitle_title_cmd.set('')

        self.subtitle_language = StringVar()
        self.subtitle_language_menu_label = Label(self.subtitle_tab, text='Language:', background="#434547", foreground="white")
        self.subtitle_language_menu_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        self.subtitle_language = ttk.Combobox(self.subtitle_tab, values=list(iso_639_2_codes_dictionary.keys()), justify="center",
                                         textvariable=self.subtitle_language)
        self.subtitle_language.grid(row=2, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
        self.subtitle_language['state'] = 'readonly'
        self.subtitle_language.current(0)

        # def subtitle_input_button_commands():
        #     global subtitle_input, subtitle_input_quoted
        #     subtitle_extensions = ('.srt', '.idx', '.ttxt')
        #     subtitle_input = filedialog.askopenfilename(initialdir="/", title="Select A File",
        #                                                 filetypes=[("Supported Formats", subtitle_extensions)])
        #     if subtitle_input:
        #         self.subtitle_input_entry.configure(state=NORMAL)
        #         self.subtitle_input_entry.delete(0, END)
        #         if subtitle_input.endswith(subtitle_extensions):
        #             subtitle_input_quoted = '"' + str(pathlib.Path(subtitle_input)) + '"'
        #             self.subtitle_input_entry.insert(0, subtitle_input)
        #             self.subtitle_input_entry.configure(state=DISABLED)
        #             self.subtitle_title_entry.configure(state=NORMAL)
        #         else:
        #             messagebox.showinfo(title='Input Not Supported',
        #                                 message="Try Again With a Supported File Type!\n\nIf this is a "
        #                                         "file that should be supported, please let me know.\n\n"
        #                                         + 'Unsupported file extension "'
        #                                         + str(pathlib.Path(subtitle_input).suffix) + '"')
        #             self.subtitle_language.current(0)
        #             self.subtitle_title_entry.delete(0, END)
        #             del subtitle_input

        # def update_subtitle_input(*args):
        #     global subtitle_input, subtitle_input_quoted
        #     self.subtitle_input_entry.configure(state=NORMAL)
        #     self.subtitle_input_entry.delete(0, END)
        #     subtitle_input = str(self.subtitle_input_dnd.get()).replace("{", "").replace("}", "")
        #     subtitle_extensions = ('.srt', '.idx', '.ttxt')
        #     if subtitle_input.endswith(subtitle_extensions):
        #         subtitle_input_quoted = '"' + str(pathlib.Path(subtitle_input)) + '"'
        #         self.subtitle_input_entry.insert(0, subtitle_input)
        #         self.subtitle_input_entry.configure(state=DISABLED)
        #         self.subtitle_title_entry.configure(state=NORMAL)
        #     else:
        #         messagebox.showinfo(title='Input Not Supported',
        #                             message="Try Again With a Supported File Type!\n\nIf this is a "
        #                                     "file that should be supported, please let me know.\n\n"
        #                                     + 'Unsupported file extension "' + str(
        #                                 pathlib.Path(subtitle_input).suffix) + '"')
        #         self.subtitle_language.current(0)
        #         self.subtitle_title_entry.delete(0, END)
        #         del subtitle_input

        # def subtitle_drop_input(event):
        #     self.subtitle_input_dnd.set(event.data)

        self.subtitle_input_dnd = StringVar()
        # self.subtitle_input_dnd.trace('w', update_subtitle_input)
        self.subtitle_input_button = HoverButton(self.subtitle_tab, text='Subtitle', command=subtitle_input_button_commands,
                                            foreground='white', background='#23272A', borderwidth='3',
                                            activebackground='grey',
                                            state=DISABLED)
        self.subtitle_input_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)
        self.subtitle_input_button.drop_target_register(DND_FILES)
        self.subtitle_input_button.dnd_bind('<<Drop>>', subtitle_drop_input)

        self.subtitle_input_entry = Entry(self.subtitle_tab, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
        self.subtitle_input_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)
        self.subtitle_input_entry.drop_target_register(DND_FILES)
        self.subtitle_input_entry.dnd_bind('<<Drop>>', subtitle_drop_input)

        # def clear_subtitle_input():  # Deletes all inputs and sets defaults for subtitle box #1
        #     global subtitle_input, self.subtitle_input_entry, self.subtitle_language, subtitle_title_cmd_input, self.subtitle_title_entry
        #     try:
        #         subtitle_title_cmd_input = ''
        #         self.subtitle_input_entry.configure(state=NORMAL)
        #         self.subtitle_input_entry.delete(0, END)
        #         self.subtitle_input_entry.configure(state=DISABLED)
        #         self.subtitle_title_entry.configure(state=NORMAL)
        #         self.subtitle_title_entry.delete(0, END)
        #         self.subtitle_title_entry.configure(state=DISABLED)
        #         del subtitle_input
        #         self.subtitle_language.current(0)
        # 
        #     except (Exception,):
        #         pass

        self.delete_subtitle_input_button = HoverButton(self.subtitle_tab, text='X', command=clear_subtitle_input,
                                                   foreground='white',
                                                   background='#23272A', borderwidth='3', activebackground='grey',
                                                   width=2)
        self.delete_subtitle_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)
        
        
        
        
        

       
        self.chapter_frame = LabelFrame(self.mp4_win, text=' Chapter ')
        self.chapter_frame.grid(row=3, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
        self.chapter_frame.configure(fg="white", bg="#434547", bd=4)

        self.chapter_frame.grid_columnconfigure(0, weight=1)
        self.chapter_frame.grid_rowconfigure(0, weight=1)

        # def chapter_input_button_commands():
        #     global chapter_input, chapter_input_quoted
        #     chapter_extensions = '.txt'
        #     chapter_input = filedialog.askopenfilename(initialdir="/", title="Select A File",
        #                                                filetypes=[("OGG", chapter_extensions)])
        #     if chapter_input:
        #         self.chapter_input_entry.configure(state=NORMAL)
        #         self.chapter_input_entry.delete(0, END)
        #         if chapter_input.endswith(chapter_extensions):
        #             chapter_input_quoted = '"' + str(pathlib.Path(chapter_input)) + '"'
        #             self.chapter_input_entry.insert(0, chapter_input)
        #             self.chapter_input_entry.configure(state=DISABLED)
        #         else:
        #             messagebox.showinfo(title='Input Not Supported',
        #                                 message="Try Again With a Supported File Type!\n\nIf this is a "
        #                                         "file that should be supported, please let me know.\n\n"
        #                                         + 'Unsupported file extension "'
        #                                         + str(pathlib.Path(chapter_input).suffix) + '"')
        #             del chapter_input
        # 
        # def update_chapter_input(*args):
        #     global chapter_input, chapter_input_quoted
        #     self.chapter_input_entry.configure(state=NORMAL)
        #     self.chapter_input_entry.delete(0, END)
        #     chapter_input = str(self.chapter_input_dnd.get()).replace("{", "").replace("}", "")
        #     chapter_extensions = '.txt'
        #     if chapter_input.endswith(chapter_extensions):
        #         chapter_input_quoted = '"' + str(pathlib.Path(chapter_input)) + '"'
        #         self.chapter_input_entry.insert(0, chapter_input)
        #         self.chapter_input_entry.configure(state=DISABLED)
        #     else:
        #         messagebox.showinfo(title='Input Not Supported',
        #                             message="Try Again With a Supported File Type!\n\nIf this is a "
        #                                     "file that should be supported, please let me know.\n\n"
        #                                     + 'Unsupported file extension "' + str(
        #                                 pathlib.Path(chapter_input).suffix) + '"')
        #         del chapter_input
        # 
        # def chapter_drop_input(event):
        #     self.chapter_input_dnd.set(event.data)

        self.chapter_input_dnd = StringVar()
        # self.chapter_input_dnd.trace('w', update_chapter_input)
        self.chapter_input_button = HoverButton(self.chapter_frame, text='Chapter', command=chapter_input_button_commands,
                                           foreground='white', background='#23272A', borderwidth='3',
                                           activebackground='grey',
                                           state=DISABLED)
        self.chapter_input_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 0), sticky=W + E)
        self.chapter_input_button.drop_target_register(DND_FILES)
        self.chapter_input_button.dnd_bind('<<Drop>>', chapter_drop_input)

        self.chapter_input_entry = Entry(self.chapter_frame, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
        self.chapter_input_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 0), sticky=W + E)
        self.chapter_input_entry.drop_target_register(DND_FILES)
        self.chapter_input_entry.dnd_bind('<<Drop>>', chapter_drop_input)

        # def clear_chapter_input():  # Deletes all inputs and sets defaults for chapter box #1
        #     global chapter_input, self.chapter_input_entry, chapter_title_cmd_input
        #     try:
        #         chapter_title_cmd_input = ''
        #         self.chapter_input_entry.configure(state=NORMAL)
        #         self.chapter_input_entry.delete(0, END)
        #         self.chapter_input_entry.configure(state=DISABLED)
        #         del chapter_input
        #     except (Exception,):
        #         pass

        self.delete_chapter_input_button = HoverButton(self.chapter_frame, text='X', command=clear_chapter_input,
                                                  foreground='white',
                                                  background='#23272A', borderwidth='3', activebackground='grey',
                                                  width=2)
        self.delete_chapter_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 0), sticky=E)

        # Auto Chapter Import Checkbutton 
        # def save_chap_import_option():  # Function to write variable to config.ini so program remembers user setting
        #     config.set('auto_chapter_import', 'option', self.auto_chap_import.get())
        #     try:
        #         with open(config_file, 'w') as configfile:
        #             config.write(configfile)
        #     except(Exception,):
        #         pass

        self.auto_chap_import = StringVar()
        self.auto_chap_import_checkbox = Checkbutton(self.chapter_frame, text='Import chapters from video input',
                                                variable=self.auto_chap_import, onvalue='on', offvalue='off',
                                                command=save_chap_import_option, takefocus=False)
        self.auto_chap_import_checkbox.grid(row=1, column=0, columnspan=2, rowspan=1, padx=10, pady=(1, 1), sticky=W)
        self.auto_chap_import_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                            activeforeground="white", selectcolor="#434547", font=("Helvetica", 10))
        self.auto_chap_import.set(str(config['auto_chapter_import']['option']))  # Set's button status from config.ini

        # ----- Auto Chapter Import Checkbutton
        
        
        #
        # Output ----
        self.output_frame = LabelFrame(self.mp4_win, text=' Output ')
        self.output_frame.grid(row=4, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
        self.output_frame.configure(fg="white", bg="#434547", bd=4)

        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)

        # def output_button_commands():
        #     global output, output_quoted
        #     output_window = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir=autofilesave_dir_path,
        #                                                  title="Select a Save Location", initialfile=autosavefilename,
        #                                                  filetypes=[("MP4", "*.mp4")])
        # 
        #     if output_window:
        #         self.output_entry.configure(state=NORMAL)
        #         self.output_entry.delete(0, END)
        #         output_quoted = '"' + str(pathlib.Path(output_window)) + '"'
        #         output = output_window
        #         self.output_entry.insert(0, output)
        #         self.output_entry.configure(state=DISABLED)

        self.output_button = HoverButton(self.output_frame, text='Output', command=output_button_commands, foreground='white',
                                    background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
        self.output_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)
        self.output_entry = Entry(self.output_frame, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
        self.output_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)

        # def clear_output():  # Deletes all inputs and sets defaults for output frame
        #     global output, self.output_entry
        #     try:
        #         self.output_entry.configure(state=NORMAL)
        #         self.output_entry.delete(0, END)
        #         self.output_entry.configure(state=DISABLED)
        #         del output
        #         messagebox.showinfo(title='Information',
        #                             message='You must select an output for the program to continue')
        #     except (Exception,):
        #         pass

        self.delete_output_button = HoverButton(self.output_frame, text='X', command=clear_output, foreground='white',
                                           background='#23272A', borderwidth='3', activebackground='grey', width=2)
        self.delete_output_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)
        

        #
        self.start_button = HoverButton(self.mp4_win, text='Mux', command=check_for_existing_output, foreground='white',
                                   background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
        self.start_button.grid(row=5, column=2, columnspan=1, padx=(10, 20), pady=(15, 2), sticky=E)

    # def start_job():
    #     global output_quoted
    #     total_progress_segments = 2  # Progress segments starts at 2 because video+output has to be defined in order for
    #
    #     # the program to work, they equal 2 progress segments
    #
    #     def error_msg_box():  # Generic error box that shows the error via the 'error_name' variable
    #         messagebox.showerror(title='Error!', message='Please input or clear the ' + error_name + ' input box')
    #
    #     if 'output' not in globals():  # If the variable 'output' doesn't exist in globals
    #         output_error = 1  # Set output error to 1 (error)
    #         messagebox.showinfo(title='Information', message='You must select an output for the program to continue')
    #     if 'output' in globals():  # If the variable exist in globals
    #         output_error = 0  # Set output error to 0 (no error)
    #
    #     try:  # Video is differently checked because it HAS to exist for the program to work, the other
    #         # variables audio, subs, etc. check for globals to see if they exist at all
    #         if detect_video_fps != '':  # If video fps equals anything other than '' (empty string/nothing)
    #             fps_input = ':fps=' + detect_video_fps  # Set fps_input to string + detect_video_fps
    #
    #         # Build video_options for the final command line with all the variables
    #         video_options = ' -add "' + VideoInput + '#1' + video_title_cmd_input + \
    #                         ':lang=' + iso_639_2_codes_dictionary[self.video_language.get()] + fps_input + \
    #                         self.dolby_profiles[self.dolby_v_profile.get()] + ':ID=1"'
    #         video_errors = 0  # Set's video_errors to 0 as long as all variables are found correctly
    #     except (Exception,):
    #         video_errors = 1  # Set's errors to 1 if the above try block cannot execute
    #         error_name = 'video'  # Provides generic error name for the above error box
    #         error_msg_box()  # Runs the error_msg_box function with the error name above
    #
    #     try:
    #         if 'audio_input' in globals():  # If the variable 'audio_input' does exist in globals
    #             total_progress_segments += 1  # Add +1 to total_progress_segments, for final summed count of segments
    #             # Build audio_options for the final command line with all the variables
    #             audio_options = ' -add "' + audio_input + acodec_stream_choices[acodec_stream.get()] + \
    #                             audio_title_cmd_input + ':delay=' + self.audio_delay.get() + ':lang=' + \
    #                             iso_639_2_codes_dictionary[self.audio_language.get()] + ':ID=2"'
    #         elif 'audio_input' not in globals():  # If the variable 'audio_input' doesn't exist in globals
    #             audio_options = ''  # Set's audio_options to '' (nothing/empty string)
    #         audio_one_errors = 0  # Set output error to 0 (no error)
    #     except (Exception,):
    #         audio_one_errors = 1  # Set's errors to 1 if the above try block cannot execute
    #         error_name = 'audio #1'  # Provides generic error name for the above error box
    #         error_msg_box()  # Runs the error_msg_box function with the error name above
    #
    #     try:
    #         if 'subtitle_input' in globals():  # If the variable 'subtitle_input' does exist in globals
    #             total_progress_segments += 1  # Add +1 to total_progress_segments, for final summed count of segments
    #             # Build subtitle_options for the final command line with all the variables
    #             subtitle_options = ' -add "' + subtitle_input + '#1' + subtitle_title_cmd_input + ':lang=' + \
    #                                iso_639_2_codes_dictionary[self.subtitle_language.get()] + ':ID=3"'
    #         elif 'subtitle_input' not in globals():
    #             subtitle_options = ''  # Set's subtitle_options to '' (nothing/empty string)
    #         subtitle_errors = 0  # Set output error to 0 (no error)
    #     except (Exception,):
    #         subtitle_errors = 1  # Set's errors to 1 if the above try block cannot execute
    #         error_name = 'subtitle'  # Provides generic error name for the above error box
    #         error_msg_box()  # Runs the error_msg_box function with the error name above
    #
    #     try:
    #         if 'chapter_input' in globals():  # If the variable 'chapter_input' does exist in globals
    #             # Build subtitle_options for the final command line with all the variables
    #             chapter_options = ' -add "' + chapter_input + fps_input + '"'
    #         elif 'chapter_input' not in globals():  # If the variable 'chapter_input' doesn't exist in globals
    #             chapter_options = ''  # Set's chapter_options to '' (nothing/empty string)
    #         chapter_errors = 0  # Set output error to 0 (no error)
    #     except (Exception,):
    #         chapter_errors = 1  # Set's errors to 1 if the above try block cannot execute
    #         error_name = 'chapter'  # Provides generic error name for the above error box
    #         error_msg_box()  # Runs the error_msg_box function with the error name above
    #
    #     # Combine all above errors, if exists and adds them to a sum (which should be 0), places them into var total_errors
    #     total_errors = video_errors + audio_one_errors + subtitle_errors + chapter_errors + output_error
    #
    #     if self.shell_options.get() == "Default" and total_errors == 0:  # Run block if self.shell_options = Default and errors = 0
    #         def close_encode():  # Block of code to close muxing window progress and terminate all sub-processes
    #             if step_label.cget('text') == 'Job Completed':  # If muxing windows label says 'Job Completed'
    #                 window.destroy()  # Close muxing window only
    #             else:  # If muxing windows label says anything other than 'Job Completed'
    #                 confirm_exit = messagebox.askyesno(title='Prompt',  # Prompt message box
    #                                                    message="Are you sure you want to stop the mux?", parent=window)
    #                 if confirm_exit:  # If user selects yes on the message box
    #                     try:  # Use subprocess.popen/cmd.exe to send a kill order to the job via job.pid
    #                         subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T",
    #                                          creationflags=subprocess.CREATE_NO_WINDOW)
    #                         window.destroy()  # Once the job is destroyed close muxing window
    #                     except (Exception,):
    #                         window.destroy()  # If job already completes or cannot be closed, still close muxing window
    #
    #         def close_window():  # Function to make 'close_encode' multi-threaded, so it can be done while the program runs
    #             threading.Thread(target=close_encode).start()
    #
    #         window = tk.Toplevel(self.mp4_win)  # Define muxing window
    #         window.title(
    #             str(pathlib.Path(VideoInput).stem))  # Set's muxing window title to VideoInput (no path no ext.)
    #         window.configure(background="#434547")  # Set's muxing window background color
    #         encode_label = Label(window, text='- ' * 20 + 'Progress' + ' -' * 20,  # Progress Label
    #                              font=("Times New Roman", 14), background='#434547', foreground="white")
    #         encode_label.grid(column=0, row=0)
    #         window.grid_columnconfigure(0, weight=1)
    #         window.grid_rowconfigure(0, weight=1)
    #         window.grid_rowconfigure(1, weight=1)
    #         window.protocol('WM_DELETE_WINDOW', close_window)
    #         window.geometry("600x450")
    #         encode_window_progress = scrolledtextwidget.ScrolledText(window, width=60, height=15,
    #                                                                  self.tabs = 10, spacing2 = 3,
    #                                                                                             spacing1 = 2, spacing3 = 3)
    #         encode_window_progress.grid(row=1, column=0, pady=(10, 6), padx=10, sticky=E + W)
    #         # Set's 0 out of 'total_progres_segments', the sum of all the progress segments from above
    #         step_label = Label(window, text='Step ' + str(0) + ' out of ' + str(total_progress_segments),
    #                            font=("Times New Roman", 12), background='#434547', foreground="white")
    #         step_label.grid(column=0, row=2, sticky=E, padx=(0, 10))
    #         updated_number = 0  # Set's a var with 0, so it can bne updated from 0 to +1 with every completed segment
    #
    #         def auto_close_window_toggle():  # Function to save input from the checkbox below to config.ini
    #             try:
    #                 config.set('auto_close_progress_window', 'option', self.auto_close_window.get())
    #                 with open(config_file, 'w') as configfile:
    #                     config.write(configfile)
    #             except (Exception,):
    #                 pass
    #
    #         auto_close_window_checkbox = Checkbutton(window, text='Automatically Close',
    #                                                  variable=self.auto_close_window,
    #                                                  onvalue='on', offvalue='off', command=auto_close_window_toggle,
    #                                                  takefocus=False)
    #         auto_close_window_checkbox.grid(row=2, column=0, columnspan=1, rowspan=1, padx=10, pady=(10, 0), sticky=W)
    #         auto_close_window_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
    #                                              activeforeground="white", selectcolor="#434547",
    #                                              font=("Helvetica", 12))
    #         self.auto_close_window.set(config['auto_close_progress_window']['option'])
    #         app_progress_bar = ttk.Progressbar(window, style="purple.Horizontal.TProgressbar", orient=HORIZONTAL,
    #                                            mode='determinate')
    #         app_progress_bar.grid(row=3, pady=(10, 10), padx=15, sticky=E + W)
    #
    #     if self.shell_options.get() == "Default" and total_errors == 0:
    #         finalcommand = '"' + mp4box + video_options + audio_options + subtitle_options + chapter_options + ' -new ' \
    #                        + output_quoted + '"'
    #         job = subprocess.Popen('cmd /c ' + finalcommand, universal_newlines=True,
    #                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
    #                                creationflags=subprocess.CREATE_NO_WINDOW)
    #         if config['reset_program_on_start_job']['option'] == 'on':  # If program is set to reset gui upon successful
    #             # start job command clear all inputs
    #             clear_inputs()
    #         for line in job.stdout:  # Code to put the muxing progress text line by line from stdout into muxing window
    #             encode_window_progress.configure(state=NORMAL)
    #             encode_window_progress.insert(END, line)
    #             encode_window_progress.see(END)
    #             encode_window_progress.configure(state=DISABLED)
    #             try:  # Code to break down stdout information
    #                 strip = line.split()[-1].replace('(', '').replace(')', '').split('/')[0]
    #                 if strip == '00':  # Each time the code 'strip' says '00' add 1 to var update_number
    #                     updated_number = updated_number + 1
    #                     if updated_number == total_progress_segments:  # For final step change label to below
    #                         step_label.configure(text='Muxing imports to .Mp4')
    #                     else:  # If updated number does not equal total_progress_setgments update step by 1 each time
    #                         step_label.configure(text='Step ' + str(updated_number) + ' out of '
    #                                                   + str(total_progress_segments))
    #                 app_progress_bar['value'] = int(strip)  # Code to update the progress bar percentage
    #             except (Exception,):
    #                 pass
    #         encode_window_progress.configure(state=NORMAL)
    #         encode_window_progress.insert(END, 'Job Completed!!')  # Once job is done insert into scroll box
    #         encode_window_progress.see(END)
    #         encode_window_progress.configure(state=DISABLED)
    #         step_label.configure(text='Job Completed')  # Update label to say 'Job Completed' (needed for above code)
    #         if config['auto_close_progress_window']['option'] == 'on':
    #             window.destroy()  # If program is set to auto close muxing window when complete, close the window
    #     if self.shell_options.get() == "Debug" and total_errors == 0:  # Command to muxing process in cmd.exe window
    #         finalcommand = '"' + mp4box + video_options + audio_options + subtitle_options + chapter_options + ' -new ' \
    #                        + output_quoted + '"'
    #         subprocess.Popen('cmd /k ' + finalcommand)
    #         if config['reset_program_on_start_job']['option'] == 'on':
    #             clear_inputs()  # Clear gui after success job start in "Debug Mode"
    #
    # # ------------------------------------------------------------------------------------------------------------- Command
    #
    # # Check to see if output file already exists and asks the user if they want to over-write it --------------------------
    # def check_for_existing_output():
    #     if pathlib.Path(output).is_file():  # Checks if 'output' variable/file already exists
    #         overwrite_output = messagebox.askyesno(title='Overwrite?',  # If exists would you like to over-write?
    #                                                message=f'Would you like to overwrite {str(output)}?')
    #         if overwrite_output:  # If "yes"
    #             threading.Thread(target=start_job).start()  # Run the start job command
    #         if not overwrite_output:  # If "no"
    #             output_button_commands()  # Open Output button function to set a new output file location
    #     else:  # If output doesn't exist go on and run the start job code
    #         threading.Thread(target=start_job).start()
    #
    # # -------------------------- Check to see if output file already exists and asks the user if they want to over-write it

    def mp4_win_exit_function(self):
        return
        """FIX THIS WITH PSTUL"""
        confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
                                                                   "     Note: This will end all current tasks!",
                                           parent=self.mp4_win)
        if confirm_exit:  # If user selects 'Yes', program attempts to kill all tasks then closes GUI
            try:
                subprocess.Popen(f"TASKKILL /F /im MP4-Mux-Tool.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
                self.mp4_win.destroy()
            except (Exception,):
                self.mp4_win.destroy()

    def clear_inputs(self):  # Clears/Resets the entire GUI/variables to "default" or None
        return
        # global VideoInput, video_title_cmd_input, self.video_title_entry, self.video_combo_language, self.dolby_v_profile_combo, \
        #     self.input_entry, detect_video_fps, audio_input, self.audio_title_cmd, self.audio_title_entry, self.audio_delay, \
        #     self.audio_input_entry, subtitle_input, self.subtitle_input_entry, self.subtitle_language, subtitle_title_cmd_input, \
        #     self.subtitle_title_entry, chapter_input, self.chapter_input_entry, chapter_title_cmd_input, output, self.output_entry
        try:  # Video Reset
            video_title_cmd_input = ''
            self.video_title_entry.configure(state=NORMAL)
            self.video_title_entry.delete(0, END)
            self.video_title_entry.configure(state=DISABLED)
            self.video_combo_language.current(0)
            self.input_entry.configure(state=NORMAL)
            self.input_entry.delete(0, END)
            self.input_entry.configure(state=DISABLED)
            self.fps_entry.configure(state=NORMAL)
            self.fps_entry.delete(0, END)
            self.fps_entry.configure(state=DISABLED)
            self.dolby_v_profile_combo.current(0)
            self.status_label.configure(text='Select "Open File" or drag and drop a video file to begin')
            self.show_command.configure(state=DISABLED)
            self.start_button.configure(state=DISABLED)
            del VideoInput
            del detect_video_fps
        except NameError as v:
            v_error = str(v)

        try:  # Audio Reset
            self.audio_title_cmd = ''
            self.audio_title_entry.delete(0, END)
            self.audio_title_entry.configure(state=DISABLED)
            self.audio_input_entry.configure(state=NORMAL)
            self.audio_input_entry.delete(0, END)
            self.audio_input_entry.configure(state=DISABLED)
            self.audio_language.current(0)
            self.audio_delay.set(0)
            self.audio_input_button.configure(state=DISABLED)
            del audio_input
        except NameError as a1:
            a1_error = str(a1)

        try:  # Subtitle Reset
            subtitle_title_cmd_input = ''
            self.subtitle_input_entry.configure(state=NORMAL)
            self.subtitle_input_entry.delete(0, END)
            self.subtitle_input_entry.configure(state=DISABLED)
            self.subtitle_title_entry.configure(state=NORMAL)
            self.subtitle_title_entry.delete(0, END)
            self.subtitle_title_entry.configure(state=DISABLED)
            self.subtitle_language.current(0)
            self.subtitle_input_button.configure(state=DISABLED)
            del subtitle_input
        except NameError as s1:
            s1_error = str(s1)

        try:  # Chapter Reset
            chapter_title_cmd_input = ''
            self.chapter_input_entry.configure(state=NORMAL)
            self.chapter_input_entry.delete(0, END)
            self.chapter_input_entry.configure(state=DISABLED)
            self.chapter_input_button.configure(state=DISABLED)
            del chapter_input
        except NameError as c:
            c_error = str(c)

        try:  # Output Reset
            self.output_entry.configure(state=NORMAL)
            self.output_entry.delete(0, END)
            self.output_entry.configure(state=DISABLED)
            self.output_button.configure(state=DISABLED)
            del output
        except NameError as o:
            o_error = str(o)

        #
        # Show Command --
        # def view_command():  # This function is to show the full command line output into a window, the code is the same as
        #     # the command code above with a few minor changes
        #     global cmd_line_window, encode_window_progress, output, output_quoted
        #     if detect_video_fps != '':
        #         fps_input = ':fps=' + detect_video_fps
        # 
        #     video_options = ' -add "' + VideoInput + '#1' + video_title_cmd_input + \
        #                     ':lang=' + iso_639_2_codes_dictionary[self.video_language.get()] + fps_input + \
        #                     self.dolby_profiles[self.dolby_v_profile.get()] + ':ID=1"'
        # 
        #     if 'audio_input' in globals():
        #         audio_options = ' -add "' + audio_input + acodec_stream_choices[acodec_stream.get()] + \
        #                         audio_title_cmd_input + ':delay=' + self.audio_delay.get() + ':lang=' + \
        #                         iso_639_2_codes_dictionary[self.audio_language.get()] + ':ID=2"'
        #     elif 'audio_input' not in globals():
        #         audio_options = ''
        # 
        #     if 'subtitle_input' in globals():
        #         subtitle_options = ' -add "' + subtitle_input + '#1' + subtitle_title_cmd_input + ':lang=' + \
        #                            iso_639_2_codes_dictionary[self.subtitle_language.get()] + ':ID=3"'
        #     elif 'subtitle_input' not in globals():
        #         subtitle_options = ''
        # 
        #     if 'chapter_input' in globals():
        #         chapter_options = ' -add "' + chapter_input + fps_input + '"'
        #     elif 'chapter_input' not in globals():
        #         chapter_options = ''
        # 
        #     finalcommand = mp4box + video_options + audio_options + subtitle_options + chapter_options + ' -new ' + \
        #                    output_quoted
        #     try:  # Attempt to update already opened window, this prevents spawning a new command window if it already exsists
        #         encode_window_progress.configure(state=NORMAL)
        #         encode_window_progress.delete(1.0, END)
        #         encode_window_progress.insert(END, finalcommand)
        #         encode_window_progress.configure(state=DISABLED)
        #         cmd_line_window.deiconify()
        #     except (AttributeError, NameError):  # If no window exists then spawn a new window with all the commands
        #         cmd_line_window = Toplevel()
        #         cmd_line_window.title('Command Line')
        #         cmd_line_window.configure(background="#434547")
        #         encode_window_progress = scrolledtextwidget.ScrolledText(cmd_line_window, width=60, height=15,
        #                                                                  self.tabs = 10,
        #                                                                              spacing2 = 3, spacing1 = 2, spacing3 = 3)
        #         encode_window_progress.grid(row=0, column=0, pady=(10, 6), padx=10, sticky=E + W)
        #         encode_window_progress.insert(END, finalcommand)
        #         encode_window_progress.configure(state=DISABLED)
        # 
        #         def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
        #             pyperclip.copy(encode_window_progress.get(1.0, END))
        # 
        #         copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
        #                                 foreground='white', background='#23272A', borderwidth='3',
        #                                 activebackground='grey')
        #         copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 10), pady=(15, 2), sticky=W + E)
        # 
        #         def hide_instead():  # This hides the command window instead of fully destroying it/it's variables, it allows
        #             # us to update the window instead of openeing a new one each time
        #             cmd_line_window.withdraw()
        # 
        #         cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        self.show_command = HoverButton(self.mp4_win, text='View Command', command=view_command, foreground='white',
                                   background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
        self.show_command.grid(row=5, column=0, columnspan=1, padx=(20, 10), pady=(15, 2), sticky=W)
        
        
        
        #
        # Status Label at bottom of main GUI ----------------------------------------------------------------- The status
        # label just updates based on the mouse cursor location, when you go over certain buttons it'll give you information
        # based on that location
        self.status_label = Label(self.mp4_win, text='Select "Open File" or drag and drop a video file to begin',
                             bd=4, relief=SUNKEN, anchor=E, background='#717171', foreground="white")
        self.status_label.grid(column=0, row=6, columnspan=4, sticky=W + E, pady=(0, 2), padx=3)

        def auto_chap_checkbtn_on_enter(e):
            self.status_label.configure(text='Import embedded chapter file from video input')

        def auto_chap_checkbtn_on_leave(e):
            self.status_label.configure(text='')

        self.auto_chap_import_checkbox.bind("<Enter>", auto_chap_checkbtn_on_enter)
        self.auto_chap_import_checkbox.bind("<Leave>", auto_chap_checkbtn_on_leave)

        # ----------------------------------------------------------------- Status Label at bottom of main GUI
        
        



    def set_mp4box_path(self):
        """dialog to set the path to mp4box"""
        path = filedialog.askopenfilename(parent=self.mp4_win, title='Select Location to "mp4box.exe"',
                                          filetypes=[('MP4Box', 'mp4box.exe')])
        if pathlib.Path(path).is_file():
            config_writer(config_file, 'mp4box_path', 'path', str(pathlib.Path(path)))

    def set_mkvextract_path(self):
        """dialog to set the path to mkvextract"""
        path = filedialog.askopenfilename(parent=self.mp4_win, title='Select Location to "mkvextract.exe"',
                                          filetypes=[('mkvextract', 'mkvextract.exe')])
        if pathlib.Path(path).is_file():
            config_writer(config_file, 'mkvextract_path', 'path', str(pathlib.Path(path)))

    def reset_config(self):
        """dialog for user to confirm config reset"""
        msg = messagebox.askyesno(parent=self.mp4_win, title='Warning',
                                  message='Are you sure you want to reset the config.ini file settings?')
        if msg:
            config_writer(config_file, 'mp4box_path', 'path', '')
            config_writer(config_file, 'mkvextract_path', 'path', '')
            config_writer(config_file, 'debug_option', 'option', '')
            config_writer(config_file, 'auto_close_progress_window', 'option', '')
            config_writer(config_file, 'reset_program_on_start_job', 'option', '')
            self.mp4_win_exit_function()


class HoverButton(Button):
    """simple class to convert button to a hoverbutton"""

    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["background"] = self["activebackground"]
        if self.cget("text") == "Video":
            self.status_label.configure(text='Video inputs supported (.avi, .mp4, .m1v/.m2v, .m4v, .264, .h264, .hevc, or '
                                        '.h265)')
        if self.cget("text") == "Audio":
            self.status_label.configure(text='Audio inputs supported (.ac3, .aac, .mp4, .m4a, .mp2, .mp3, .opus, or .ogg)')
        if self.cget("text") == "Subtitle":
            self.status_label.configure(text='Subtitle inputs supported (.srt, .idx, .ttxt)')
        if self.cget("text") == "Chapter":
            self.status_label.configure(text='Chapter input supported OGG (.txt)')
        if self.cget("text") == "Output":
            self.status_label.configure(text='Select File Save Location (*.mp4)')
        if self.cget("text") == "X":
            self.status_label.configure(text='Remove input and settings')
        if self.cget("text") == "View Command":
            self.status_label.configure(text='Select to show complete command line')
        if self.cget("text") == "Mux":
            self.status_label.configure(text='Select to begin muxing')

    def on_leave(self, e):
        self["background"] = self.defaultBackground
        self.status_label.configure(text="")

# Bundled apps --------------------------------------------------------------------------------------------------------
mp4box = config['mp4box_path']['path']

if not pathlib.Path(mp4box.replace('"', '')).is_file():  # Checks config for bundled app paths path
    # mp4box -----------------------------------------------------------------------
    if pathlib.Path('apps/mp4box/MP4Box.exe').is_file():  # If mp4box.exe is located in the apps folder
        messagebox.showinfo(title='Info', message='Program will use the included '
                                                  '"mp4box.exe" located in the "apps" folder')
        mp4box = '"' + str(pathlib.Path('apps/mp4box/MP4Box.exe')) + '"'  # sets variable to mp4box.exe
        try:  # Write path location to config.ini file
            config.set('mp4box_path', 'path', mp4box)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):  # If unable to write path to mp4box.exe present error message
            messagebox.showerror(title='Error!', message=f'Could not save path to mp4box at '
                                                         f'\n{mp4box}\n please try again')
    elif not pathlib.Path('apps/mp4box/MP4Box.exe').is_file():  # If mp4box.exe does not exist
        messagebox.showerror(title='Error!', message='Please download mp4box.exe and set path to '
                                                     'mp4box.exe in the Options menu')  # Error message
        webbrowser.open('https://www.mediafire.com/file/8pymy2869rmy5x5/mp4box.zip/file')  # Gets recent build
    # mp4box ------------------------------------------------------------------------

mkvextract = config['mkvextract_path']['path']
if not pathlib.Path(mkvextract.replace('"', '')).is_file():  # Checks config for bundled app paths path
    # mkvextract -----------------------------------------------------------------------
    if pathlib.Path('apps/mkvextract/mkvextract.exe').is_file():  # If mkvextract.exe is located in the apps folder
        messagebox.showinfo(title='Info', message='Program will use the included '
                                                  '"mkvextract.exe" located in the "apps" folder')
        mkvextract = '"' + str(pathlib.Path('apps/mkvextract/mkvextract.exe')) + '"'  # sets variable to mkvextract.exe
        try:  # Write path location to config.ini file
            config.set('mkvextract_path', 'path', mkvextract)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):  # If unable to write path to mp4box.exe present error message
            messagebox.showerror(title='Error!', message=f'Could not save path to mkvextract at '
                                                         f'\n{mkvextract}\n please try again')
    elif not pathlib.Path('apps/mkvextract/mkvextract.exe').is_file():  # If mkvextract.exe does not exist
        messagebox.showerror(title='Error!', message='Please download mkvextract.exe and set path to '
                                                     'mkvextract.exe in the Options menu')  # Error message
        webbrowser.open('https://www.fosshub.com/MKVToolNix.html?dwl=mkvtoolnix-64-bit-64.0.0.7z')
        # Opens default web-browser to mkvextract (mkvtoolnix)
    # mkvextract ------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------- Bundled apps


def input_button_commands():  # Open file block of code (non drag and drop)
    return
    # global VideoInput, autosavefilename, autofilesave_dir_path, VideoInputQuoted, output, detect_video_fps, \
    #     self.fps_entry, output_quoted, chapter_input
    video_extensions = ('.avi', '.mp4', '.m1v', '.m2v', '.m4v', '.264', '.h264', '.hevc', '.h265')
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=[("Supported Formats", video_extensions)])
    if VideoInput:
        self.input_entry.configure(state=NORMAL)
        self.input_entry.delete(0, END)
        if VideoInput.endswith(video_extensions):
            autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
            autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
            VideoInputQuoted = '"' + str(pathlib.Path(VideoInput)) + '"'
            self.input_entry.insert(0, str(pathlib.Path(VideoInput)))
            filename = pathlib.Path(VideoInput)
            VideoOut = filename.with_suffix('')
            autosavefilename = str(VideoOut.name) + '.muxed_output'
            autosave_file_dir = pathlib.Path(str(f'{autofilesave_dir_path}\\') + str(autosavefilename + '.mp4'))
            output = str(autosave_file_dir)
            output_quoted = '"' + output + '"'
            self.input_entry.configure(state=DISABLED)
            self.video_title_entry.configure(state=NORMAL)
            self.output_entry.configure(state=NORMAL)
            self.output_entry.delete(0, END)
            self.output_entry.configure(state=DISABLED)
            self.output_entry.configure(state=NORMAL)
            self.output_entry.insert(0, str(autosave_file_dir))
            self.output_entry.configure(state=DISABLED)
            self.output_button.configure(state=NORMAL)
            self.audio_input_button.configure(state=NORMAL)
            self.subtitle_input_button.configure(state=NORMAL)
            self.chapter_input_button.configure(state=NORMAL)
            self.output_button.configure(state=NORMAL)
            self.start_button.configure(state=NORMAL)
            self.show_command.configure(state=NORMAL)
            media_info = MediaInfo.parse(filename)
            for track in media_info.tracks:  # Use mediainfo module to parse video section to collect frame rate
                if track.track_type == "Video":
                    detect_video_fps = track.frame_rate
                    self.fps_entry.configure(state=NORMAL)
                    self.fps_entry.delete(0, END)
                    self.fps_entry.insert(0, detect_video_fps)
                    self.fps_entry.configure(state=DISABLED)
                    try:  # Code to detect the position of the language code, for 3 digit, and set it to a variable
                        detect_index = [len(i) for i in track.other_language].index(3)
                        language_index = list(iso_639_2_codes_dictionary.values()).index(
                            track.other_language[detect_index])
                        self.video_combo_language.current(language_index)
                        self.video_title_entry.delete(0, END)
                        self.video_title_entry.insert(0, track.title)
                    except(Exception,):
                        pass
                if config['auto_chapter_import']['option'] == 'on':  # If checkbox to auto import chapter is checked
                    if track.track_type == 'General':
                        if track.count_of_menu_streams is not None:  # If source has chapters continue code
                            finalcommand = '"' + mp4box + ' ' + f'"{filename}"' + ' -dump-chap-ogg -out ' + \
                                           f'"{pathlib.Path(filename).with_suffix(".txt")}"' + '"'
                            # Use subprocess.run to execute, then wait to finish executing before code moves to next
                            subprocess.run('cmd /c ' + finalcommand, universal_newlines=True,
                                           creationflags=subprocess.CREATE_NO_WINDOW)
                            if pathlib.Path(filename).with_suffix(".txt").is_file():
                                self.chapter_input_entry.configure(state=NORMAL)
                                self.chapter_input_entry.delete(0, END)
                                self.chapter_input_entry.insert(0, f'Imported chapters from: "{filename.name}"')
                                self.chapter_input_entry.configure(state=DISABLED)
                                chapter_input = str(pathlib.Path(filename).with_suffix(".txt"))
        else:
            messagebox.showinfo(title='Input Not Supported',  # Error message if input is not a supported file type
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.\n\n"
                                        + 'Unsupported file extension "' + str(pathlib.Path(VideoInput).suffix) + '"')
            self.video_combo_language.current(0)
            self.video_title_entry.delete(0, END)
            self.fps_entry.configure(state=NORMAL)
            self.fps_entry.delete(0, END)
            self.fps_entry.configure(state=DISABLED)
            del detect_video_fps
            del VideoInput


# ---------------------------------------------------------------------------------------------- Input Functions Button

# Drag and Drop Functions ---------------------------------------------------------------------------------------------
def video_drop_input(event):  # Drag and drop function
    return
    self.input_dnd.set(event.data)


def update_file_input(*args):  # Drag and drop block of code
    return
    # global VideoInput, autofilesave_dir_path, VideoInputQuoted, output, autosavefilename, detect_video_fps, \
    #     self.fps_entry, output_quoted, chapter_input
    self.input_entry.configure(state=NORMAL)
    self.input_entry.delete(0, END)
    VideoInput = str(self.input_dnd.get()).replace("{", "").replace("}", "")
    video_extensions = ('.avi', '.mp4', '.m1v', '.m2v', '.m4v', '.264', '.h264', '.hevc', '.h265')
    if VideoInput.endswith(video_extensions):
        autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
        autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
        VideoInputQuoted = '"' + str(pathlib.Path(VideoInput)) + '"'
        self.input_entry.insert(0, str(self.input_dnd.get()).replace("{", "").replace("}", ""))
        filename = pathlib.Path(VideoInput)
        VideoOut = filename.with_suffix('')
        autosavefilename = str(VideoOut.name) + '.muxed_output'
        autosave_file_dir = pathlib.Path(str(f'{autofilesave_dir_path}\\') + str(autosavefilename + '.mp4'))
        output = str(autosave_file_dir)
        output_quoted = '"' + output + '"'
        self.input_entry.configure(state=DISABLED)
        self.video_title_entry.configure(state=NORMAL)
        self.output_entry.configure(state=NORMAL)
        self.output_entry.delete(0, END)
        self.output_entry.configure(state=DISABLED)
        self.output_entry.configure(state=NORMAL)
        self.output_entry.insert(0, str(autosave_file_dir))
        self.output_entry.configure(state=DISABLED)
        self.output_button.configure(state=NORMAL)
        self.audio_input_button.configure(state=NORMAL)
        self.subtitle_input_button.configure(state=NORMAL)
        self.chapter_input_button.configure(state=NORMAL)
        self.output_button.configure(state=NORMAL)
        self.start_button.configure(state=NORMAL)
        self.show_command.configure(state=NORMAL)
        media_info = MediaInfo.parse(filename)
        for track in media_info.tracks:
            if track.track_type == "Video":
                detect_video_fps = track.frame_rate
                self.fps_entry.configure(state=NORMAL)
                self.fps_entry.delete(0, END)
                self.fps_entry.insert(0, detect_video_fps)
                self.fps_entry.configure(state=DISABLED)
                try:
                    detect_index = [len(i) for i in track.other_language].index(3)
                    language_index = list(iso_639_2_codes_dictionary.values()).index(
                        track.other_language[detect_index])
                    self.video_combo_language.current(language_index)
                    self.video_title_entry.delete(0, END)
                    self.video_title_entry.insert(0, track.title)
                except(Exception,):
                    pass
            if config['auto_chapter_import']['option'] == 'on':  # If checkbox to auto import chapter is checked
                if track.track_type == 'General':
                    if track.count_of_menu_streams is not None:  # If source has chapters continue code
                        finalcommand = '"' + mp4box + ' ' + f'"{filename}"' + ' -dump-chap-ogg -out ' + \
                                       f'"{pathlib.Path(filename).with_suffix(".txt")}"' + '"'
                        # Use subprocess.run to execute, then wait to finish executing before code moves to next
                        subprocess.run('cmd /c ' + finalcommand, universal_newlines=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                        if pathlib.Path(filename).with_suffix(".txt").is_file():
                            self.chapter_input_entry.configure(state=NORMAL)
                            self.chapter_input_entry.delete(0, END)
                            self.chapter_input_entry.insert(0, f'Imported chapters from: "{filename.name}"')
                            self.chapter_input_entry.configure(state=DISABLED)
                            chapter_input = str(pathlib.Path(filename).with_suffix(".txt"))
    else:
        messagebox.showinfo(title='Input Not Supported',
                            message="Try Again With a Supported File Type!\n\nIf this is a "
                                    "file that should be supported, please let me know.\n\n"
                                    + 'Unsupported file extension "' + str(pathlib.Path(VideoInput).suffix) + '"')
        self.video_combo_language.current(0)
        self.video_title_entry.delete(0, END)
        self.fps_entry.configure(state=NORMAL)
        self.fps_entry.delete(0, END)
        self.fps_entry.configure(state=DISABLED)
        del detect_video_fps
        del VideoInput


def clear_video_input():  # When user selects 'X' to clear input box
    return
    # global VideoInput, video_title_cmd_input, self.video_title_entry, self.video_combo_language, self.input_entry, \
    #     detect_video_fps, self.dolby_v_profile_combo
    try:
        video_title_cmd_input = ''
        self.video_title_entry.configure(state=NORMAL)
        self.video_title_entry.delete(0, END)
        self.video_title_entry.configure(state=DISABLED)
        self.video_combo_language.current(0)
        self.input_entry.configure(state=NORMAL)
        self.input_entry.delete(0, END)
        self.input_entry.configure(state=DISABLED)
        self.fps_entry.configure(state=NORMAL)
        self.fps_entry.delete(0, END)
        self.fps_entry.configure(state=DISABLED)
        self.dolby_v_profile_combo.current(0)
        del VideoInput
        del detect_video_fps
    except (Exception,):
        pass


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    MainGui(root)
    root.mainloop()
