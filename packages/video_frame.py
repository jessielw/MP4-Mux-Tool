from tkinter import Label, E, W, N, S, LabelFrame, ttk, Frame, StringVar, DISABLED, Entry, filedialog, messagebox, NORMAL, END
import pathlib
from packages.hoverbutton import HoverButton
from tkinterdnd2 import TkinterDnD, DND_FILES
from packages.iso_639_2 import iso_639_2_codes_dictionary


class VideoSection:

    def __init__(self, main_gui):
        self.mp4_win = main_gui.mp4_win

        # video frame
        self.video_frame = LabelFrame(self.mp4_win, text=' Video ', fg="white", bg="#434547", bd=4)
        self.video_frame.grid(row=0, columnspan=3, sticky=E + W + N + S, padx=20, pady=(5, 0))

        # video frame grid
        self.video_frame.grid_columnconfigure(0, weight=1)
        self.video_frame.grid_rowconfigure(0, weight=1)

        # bind file drop for video input to video frame
        self.video_frame.drop_target_register(DND_FILES)
        self.video_frame.dnd_bind('<<Drop>>', lambda drop_event: self.open_video_source(
            [x for x in self.mp4_win.splitlist(drop_event.data)][0]))

        # video frame notebook tabs
        self.tabs = ttk.Notebook(self.video_frame, height=110)
        self.tabs.grid(row=0, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)
        self.video_tab = Frame(self.tabs, background="#434547")
        self.video_tab2 = Frame(self.tabs, background="#434547")
        self.tabs.add(self.video_tab, text=' Input ')
        self.tabs.add(self.video_tab2, text=' Options ')

        # video frame notebook tabs grid
        for vt_c in range(4):
            self.video_tab.grid_columnconfigure(vt_c, weight=1)
        for vt_r in range(3):
            self.video_tab.grid_rowconfigure(vt_r, weight=1)

        # button video input
        self.input_dnd = StringVar()
        self.input_dnd_button = HoverButton(self.video_tab, text='Video', command=self.manual_video_input,
                                            foreground='white',background='#23272A', borderwidth='3',
                                            activebackground='grey', width=15)
        self.input_dnd_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=W + E)

        # video title
        self.video_title_cmd = StringVar()
        self.video_title_entry_label = Label(self.video_tab, text='Video Title:', anchor=W, background='#434547',
                                             foreground='white')
        self.video_title_entry_label.grid(row=1, column=1, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        self.video_title_entry = Entry(self.video_tab, textvariable=self.video_title_cmd, borderwidth=4,
                                       background='#CACACA', state=DISABLED)
        self.video_title_entry.grid(row=2, column=1, columnspan=1, padx=(5, 15), pady=(0, 15), sticky=W + E)

        self.input_entry = Entry(self.video_tab, borderwidth=4, background='#CACACA', state=DISABLED, width=40)
        self.input_entry.grid(row=0, column=1, columnspan=2, padx=(5, 0), pady=5, sticky=W + E)

        self.delete_input_button = HoverButton(self.video_tab, text='X', command=self.clear_video_input, foreground='white',
                                               background='#23272A', borderwidth='3', activebackground='grey', width=2)
        self.delete_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=5, sticky=E)

        # Video FPS Label is only for viewing purposes, you need input FPS for program to know what fps to output
        self.video_fps_menu_label = Label(self.video_tab, text='Framerate (FPS):', background="#434547",
                                          foreground="white")
        self.video_fps_menu_label.grid(row=1, column=2, columnspan=1, padx=(3, 0), pady=(0, 0), sticky=W)
        self.fps_entry = Entry(self.video_tab, borderwidth=4, background='#CACACA', state=DISABLED, width=10)
        self.fps_entry.grid(row=2, column=2, columnspan=2, padx=(5, 10), pady=(0, 15), sticky=W + E)

        self.video_language = StringVar()
        self.video_language_menu_label = Label(self.video_tab, text='Language:', background="#434547",
                                               foreground="white")
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
        self.dolby_v_profile_combo = ttk.Combobox(self.video_tab2, values=list(self.dolby_profiles.keys()),
                                                  justify="center",
                                                  textvariable=self.dolby_v_profile, width=20)
        self.dolby_v_profile_combo.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=W + E + N + S)
        self.dolby_v_profile_combo['state'] = 'readonly'
        self.dolby_v_profile_combo.current(0)  # Sets profile to index 0 ('') by default

    def manual_video_input(self):
        """gui dialog function for video input when the button is clicked"""
        vid_input = filedialog.askopenfilename(parent=self.mp4_win, initialdir="/", title="Select Video File")

        if vid_input:
            self.open_video_source(vid_input)

    def open_video_source(self, video_input):
        """this will be the open video source for both inputs!"""
        # work here, check extensions, perfect
        # use code from input_button_commands() and adapt
        supported_video_extensions = ('.avi', '.mp4', '.m1v', '.m2v', '.m4v', '.264', '.h264', '.hevc', '.h265')

        print(video_input)
        if pathlib.Path(video_input).suffix in supported_video_extensions:
            print('yes')
        # global VideoInput, autosavefilename, autofilesave_dir_path, VideoInputQuoted, output, detect_video_fps, \
        #     self.fps_entry, output_quoted, chapter_input

        # if VideoInput:
        #     self.input_entry.configure(state=NORMAL)
        #     self.input_entry.delete(0, END)
        #     if VideoInput.endswith(video_extensions):
        #         autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
        #         autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
        #         VideoInputQuoted = '"' + str(pathlib.Path(VideoInput)) + '"'
        #         self.input_entry.insert(0, str(pathlib.Path(VideoInput)))
        #         filename = pathlib.Path(VideoInput)
        #         VideoOut = filename.with_suffix('')
        #         autosavefilename = str(VideoOut.name) + '.muxed_output'
        #         autosave_file_dir = pathlib.Path(str(f'{autofilesave_dir_path}\\') + str(autosavefilename + '.mp4'))
        #         output = str(autosave_file_dir)
        #         output_quoted = '"' + output + '"'
        #         self.input_entry.configure(state=DISABLED)
        #         self.video_title_entry.configure(state=NORMAL)
        #         self.output_entry.configure(state=NORMAL)
        #         self.output_entry.delete(0, END)
        #         self.output_entry.configure(state=DISABLED)
        #         self.output_entry.configure(state=NORMAL)
        #         self.output_entry.insert(0, str(autosave_file_dir))
        #         self.output_entry.configure(state=DISABLED)
        #         self.output_button.configure(state=NORMAL)
        #         self.audio_input_button.configure(state=NORMAL)
        #         self.subtitle_input_button.configure(state=NORMAL)
        #         self.chapter_input_button.configure(state=NORMAL)
        #         self.output_button.configure(state=NORMAL)
        #         self.start_button.configure(state=NORMAL)
        #         self.show_command.configure(state=NORMAL)
        #         media_info = MediaInfo.parse(filename)
        #         for track in media_info.tracks:  # Use mediainfo module to parse video section to collect frame rate
        #             if track.track_type == "Video":
        #                 detect_video_fps = track.frame_rate
        #                 self.fps_entry.configure(state=NORMAL)
        #                 self.fps_entry.delete(0, END)
        #                 self.fps_entry.insert(0, detect_video_fps)
        #                 self.fps_entry.configure(state=DISABLED)
        #                 try:  # Code to detect the position of the language code, for 3 digit, and set it to a variable
        #                     detect_index = [len(i) for i in track.other_language].index(3)
        #                     language_index = list(iso_639_2_codes_dictionary.values()).index(
        #                         track.other_language[detect_index])
        #                     self.video_combo_language.current(language_index)
        #                     self.video_title_entry.delete(0, END)
        #                     self.video_title_entry.insert(0, track.title)
        #                 except(Exception,):
        #                     pass
        #             if config['auto_chapter_import']['option'] == 'on':  # If checkbox to auto import chapter is checked
        #                 if track.track_type == 'General':
        #                     if track.count_of_menu_streams is not None:  # If source has chapters continue code
        #                         finalcommand = '"' + mp4box + ' ' + f'"{filename}"' + ' -dump-chap-ogg -out ' + \
        #                                        f'"{pathlib.Path(filename).with_suffix(".txt")}"' + '"'
        #                         # Use subprocess.run to execute, then wait to finish executing before code moves to next
        #                         subprocess.run('cmd /c ' + finalcommand, universal_newlines=True,
        #                                        creationflags=subprocess.CREATE_NO_WINDOW)
        #                         if pathlib.Path(filename).with_suffix(".txt").is_file():
        #                             self.chapter_input_entry.configure(state=NORMAL)
        #                             self.chapter_input_entry.delete(0, END)
        #                             self.chapter_input_entry.insert(0, f'Imported chapters from: "{filename.name}"')
        #                             self.chapter_input_entry.configure(state=DISABLED)
        #                             chapter_input = str(pathlib.Path(filename).with_suffix(".txt"))
        #     else:
        #         messagebox.showinfo(title='Input Not Supported',  # Error message if input is not a supported file type
        #                             message="Try Again With a Supported File Type!\n\nIf this is a "
        #                                     "file that should be supported, please let me know.\n\n"
        #                                     + 'Unsupported file extension "' + str(
        #                                 pathlib.Path(VideoInput).suffix) + '"')
        #         self.video_combo_language.current(0)
        #         self.video_title_entry.delete(0, END)
        #         self.fps_entry.configure(state=NORMAL)
        #         self.fps_entry.delete(0, END)
        #         self.fps_entry.configure(state=DISABLED)
        #         del detect_video_fps
        #         del VideoInput

    def clear_video_input(self):  # When user selects 'X' to clear input box
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

    # Drag and Drop Functions ---------------------------------------------------------------------------------------------
    # def video_drop_input(event):  # Drag and drop function
    #     return
    #     self.input_dnd.set(event.data)
    #
    # def update_file_input(*args):  # Drag and drop block of code
    #     return
    #     # global VideoInput, autofilesave_dir_path, VideoInputQuoted, output, autosavefilename, detect_video_fps, \
    #     #     self.fps_entry, output_quoted, chapter_input
    #     self.input_entry.configure(state=NORMAL)
    #     self.input_entry.delete(0, END)
    #     VideoInput = str(self.input_dnd.get()).replace("{", "").replace("}", "")
    #     video_extensions = ('.avi', '.mp4', '.m1v', '.m2v', '.m4v', '.264', '.h264', '.hevc', '.h265')
    #     if VideoInput.endswith(video_extensions):
    #         autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
    #         autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
    #         VideoInputQuoted = '"' + str(pathlib.Path(VideoInput)) + '"'
    #         self.input_entry.insert(0, str(self.input_dnd.get()).replace("{", "").replace("}", ""))
    #         filename = pathlib.Path(VideoInput)
    #         VideoOut = filename.with_suffix('')
    #         autosavefilename = str(VideoOut.name) + '.muxed_output'
    #         autosave_file_dir = pathlib.Path(str(f'{autofilesave_dir_path}\\') + str(autosavefilename + '.mp4'))
    #         output = str(autosave_file_dir)
    #         output_quoted = '"' + output + '"'
    #         self.input_entry.configure(state=DISABLED)
    #         self.video_title_entry.configure(state=NORMAL)
    #         self.output_entry.configure(state=NORMAL)
    #         self.output_entry.delete(0, END)
    #         self.output_entry.configure(state=DISABLED)
    #         self.output_entry.configure(state=NORMAL)
    #         self.output_entry.insert(0, str(autosave_file_dir))
    #         self.output_entry.configure(state=DISABLED)
    #         self.output_button.configure(state=NORMAL)
    #         self.audio_input_button.configure(state=NORMAL)
    #         self.subtitle_input_button.configure(state=NORMAL)
    #         self.chapter_input_button.configure(state=NORMAL)
    #         self.output_button.configure(state=NORMAL)
    #         self.start_button.configure(state=NORMAL)
    #         self.show_command.configure(state=NORMAL)
    #         media_info = MediaInfo.parse(filename)
    #         for track in media_info.tracks:
    #             if track.track_type == "Video":
    #                 detect_video_fps = track.frame_rate
    #                 self.fps_entry.configure(state=NORMAL)
    #                 self.fps_entry.delete(0, END)
    #                 self.fps_entry.insert(0, detect_video_fps)
    #                 self.fps_entry.configure(state=DISABLED)
    #                 try:
    #                     detect_index = [len(i) for i in track.other_language].index(3)
    #                     language_index = list(iso_639_2_codes_dictionary.values()).index(
    #                         track.other_language[detect_index])
    #                     self.video_combo_language.current(language_index)
    #                     self.video_title_entry.delete(0, END)
    #                     self.video_title_entry.insert(0, track.title)
    #                 except(Exception,):
    #                     pass
    #             if config['auto_chapter_import']['option'] == 'on':  # If checkbox to auto import chapter is checked
    #                 if track.track_type == 'General':
    #                     if track.count_of_menu_streams is not None:  # If source has chapters continue code
    #                         finalcommand = '"' + mp4box + ' ' + f'"{filename}"' + ' -dump-chap-ogg -out ' + \
    #                                        f'"{pathlib.Path(filename).with_suffix(".txt")}"' + '"'
    #                         # Use subprocess.run to execute, then wait to finish executing before code moves to next
    #                         subprocess.run('cmd /c ' + finalcommand, universal_newlines=True,
    #                                        creationflags=subprocess.CREATE_NO_WINDOW)
    #                         if pathlib.Path(filename).with_suffix(".txt").is_file():
    #                             self.chapter_input_entry.configure(state=NORMAL)
    #                             self.chapter_input_entry.delete(0, END)
    #                             self.chapter_input_entry.insert(0, f'Imported chapters from: "{filename.name}"')
    #                             self.chapter_input_entry.configure(state=DISABLED)
    #                             chapter_input = str(pathlib.Path(filename).with_suffix(".txt"))
    #     else:
    #         messagebox.showinfo(title='Input Not Supported',
    #                             message="Try Again With a Supported File Type!\n\nIf this is a "
    #                                     "file that should be supported, please let me know.\n\n"
    #                                     + 'Unsupported file extension "' + str(pathlib.Path(VideoInput).suffix) + '"')
    #         self.video_combo_language.current(0)
    #         self.video_title_entry.delete(0, END)
    #         self.fps_entry.configure(state=NORMAL)
    #         self.fps_entry.delete(0, END)
    #         self.fps_entry.configure(state=DISABLED)
    #         del detect_video_fps
    #         del VideoInput
