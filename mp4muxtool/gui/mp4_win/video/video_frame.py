from tkinter import Label, E, W, N, S, LabelFrame, ttk, Frame, DISABLED, Entry, filedialog, NORMAL, END, SUNKEN, \
    messagebox

from tkinterdnd2 import DND_FILES

from mp4muxtool.misc.iso_639_2 import iso_639_2_codes_dictionary
from mp4muxtool.theme.hoverbutton import HoverButton
from mp4muxtool.gui.mp4_win.video.video_track_selection import VideoTrackSelection
from mp4muxtool.gui.mp4_win.demuxer.demux_window import DemuxWindow

from configparser import ConfigParser
from mp4muxtool.config.config_writer import config_file

from pymediainfo import MediaInfo

import pathlib


class VideoSection:
    """creates the video portion of the GUI as well as the required methods"""

    def __init__(self, main_gui):
        """
        Creates all the widgets/variables used within the video frame.

        :param main_gui: Main Gui/Root object
        """

        # video input variable
        self.video_input = None

        # parent window
        self.mp4_win = main_gui.mp4_win

        # theme
        self.theme = main_gui.open_theme

        # config parser
        self.config_parser = ConfigParser()
        self.config_parser.read(config_file)

        # main video frame
        self.video_frame = LabelFrame(self.mp4_win, text=' Video ', bd=3,
                                      font=(self.theme.set_font, self.theme.set_font_size + 1, "bold"),
                                      fg=self.theme.custom_label_frame_colors["foreground"],
                                      bg=self.theme.custom_label_frame_colors["background"])
        self.video_frame.grid(row=0, columnspan=3, sticky=E + W + N + S, padx=5, pady=(5, 0))

        # main video frame grid
        self.video_frame.grid_columnconfigure(0, weight=1)
        self.video_frame.grid_rowconfigure(0, weight=1)

        # bind file drop for video input to video frame
        self.video_frame.drop_target_register(DND_FILES)
        self.video_frame.dnd_bind('<<Drop>>', lambda drop_event: self._open_video_source(
            [x for x in self.mp4_win.splitlist(drop_event.data)][0]))

        # video frame notebook tabs
        self.tabs = ttk.Notebook(self.video_frame, height=110)
        self.tabs.grid(row=0, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)

        # add input tab
        self.video_tab = Frame(self.tabs, background=self.theme.custom_frame_bg_colors["specialbg"])
        self.tabs.add(self.video_tab, text=' Input ')

        # add options tab
        self.video_tab2 = Frame(self.tabs, background=self.theme.custom_frame_bg_colors["specialbg"])
        self.tabs.add(self.video_tab2, text=' Options ')

        # video frame notebook tabs grid
        for vt_c in range(4):
            self.video_tab.grid_columnconfigure(vt_c, weight=1)
            self.video_tab2.grid_columnconfigure(vt_c, weight=1)
        for vt_r in range(3):
            self.video_tab.grid_rowconfigure(vt_r, weight=1)
            self.video_tab2.grid_rowconfigure(vt_r, weight=1)

        # input frame - to organize input section
        self.input_frame = Frame(
            self.video_tab,
            highlightbackground=self.theme.custom_frame_bg_colors["highlightcolor"],
            highlightthickness=0,
            bg=self.theme.custom_frame_bg_colors["specialbg"],
            highlightcolor=self.theme.custom_frame_bg_colors["highlightcolor"],
        )
        self.input_frame.grid(column=0, row=0, columnspan=4, sticky=N + S + E + W)

        # input frame grid control
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=200)
        self.input_frame.grid_columnconfigure(2, weight=1)
        self.input_frame.grid_columnconfigure(3, weight=1)
        self.input_frame.grid_rowconfigure(0, weight=1)

        # input button
        self.input_dnd_button = HoverButton(self.input_frame, text='Video', command=self._manual_video_input,
                                            width=15,
                                            borderwidth="3",
                                            foreground=self.theme.custom_button_colors["foreground"],
                                            background=self.theme.custom_button_colors["background"],
                                            activeforeground=self.theme.custom_button_colors["activeforeground"],
                                            activebackground=self.theme.custom_button_colors["activebackground"],
                                            disabledforeground=self.theme.custom_button_colors["disabledforeground"])
        self.input_dnd_button.grid(row=0, column=0, padx=10, pady=5, sticky=W + E)

        # input entry
        self.input_entry = Entry(self.input_frame, state=DISABLED, width=40, borderwidth=4,
                                 fg=self.theme.custom_entry_colors["foreground"],
                                 bg=self.theme.custom_entry_colors["background"],
                                 disabledforeground=self.theme.custom_entry_colors["disabledforeground"],
                                 disabledbackground=self.theme.custom_entry_colors["disabledbackground"])
        self.input_entry.grid(row=0, column=1, columnspan=2, pady=(3, 0), sticky=W + E)

        # input delete button
        self.delete_input_button = HoverButton(self.input_frame, text='X', command=self._clear_video_input,
                                               borderwidth="3", width=3,
                                               foreground=self.theme.custom_button_colors["foreground"],
                                               background=self.theme.custom_button_colors["background"],
                                               activeforeground=self.theme.custom_button_colors["activeforeground"],
                                               activebackground=self.theme.custom_button_colors["activebackground"],
                                               disabledforeground=self.theme.custom_button_colors["disabledforeground"])
        self.delete_input_button.grid(row=0, column=3, padx=10, pady=5, sticky=E + W)

        # video title label
        self.video_title_entry_label = Label(self.video_tab, text='Video Title:', anchor=W, bd=0,
                                             relief=SUNKEN,
                                             background=self.theme.custom_frame_bg_colors["specialbg"],
                                             fg=self.theme.custom_label_colors["foreground"],
                                             font=(self.theme.set_font, self.theme.set_font_size + 1))
        self.video_title_entry_label.grid(row=1, column=1, padx=10, pady=0, sticky=W)

        # video title entry box
        self.video_title_entry = Entry(self.video_tab, borderwidth=4,
                                       fg=self.theme.custom_entry_colors["foreground"],
                                       bg=self.theme.custom_entry_colors["background"],
                                       disabledforeground=self.theme.custom_entry_colors["disabledforeground"],
                                       disabledbackground=self.theme.custom_entry_colors["disabledbackground"])
        self.video_title_entry.grid(row=2, column=1, padx=10, pady=(0, 10), sticky=W + E)

        # video delay label
        self.video_delay_menu_label = Label(self.video_tab, text='Delay (MS):', bd=0,
                                          relief=SUNKEN,
                                          background=self.theme.custom_frame_bg_colors["specialbg"],
                                          fg=self.theme.custom_label_colors["foreground"],
                                          font=(self.theme.set_font, self.theme.set_font_size + 1))
        self.video_delay_menu_label.grid(row=1, column=2, padx=10, pady=0, sticky=W)

        # video delay entry box
        self.delay_entry = Entry(self.video_tab, width=10, borderwidth=4,
                               fg=self.theme.custom_entry_colors["foreground"],
                               bg=self.theme.custom_entry_colors["background"],
                               disabledforeground=self.theme.custom_entry_colors["disabledforeground"],
                               disabledbackground=self.theme.custom_entry_colors["disabledbackground"])
        self.delay_entry.grid(row=2, column=2, columnspan=2, padx=10, pady=(0, 10), sticky=W + E)

        # video language label
        self.video_language_menu_label = Label(self.video_tab, text='Language:', bd=0,
                                               relief=SUNKEN,
                                               background=self.theme.custom_frame_bg_colors["specialbg"],
                                               fg=self.theme.custom_label_colors["foreground"],
                                               font=(self.theme.set_font, self.theme.set_font_size + 1))
        self.video_language_menu_label.grid(row=1, column=0, padx=10, pady=0, sticky=W)

        # video language combobox
        self.video_combo_language = ttk.Combobox(self.video_tab, values=list(iso_639_2_codes_dictionary.keys()),
                                                 justify="center", width=15,
                                                 font=(self.theme.set_font, self.theme.set_font_size + 3))
        self.video_combo_language.grid(row=2, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=W + E)
        self.video_combo_language['state'] = 'readonly'

        # video FPS label - is only for viewing purposes, you need input FPS for mp4box to know what fps to output
        self.video_fps_menu_label = Label(self.video_tab2, text='Framerate (FPS):', bd=0,
                                          relief=SUNKEN,
                                          background=self.theme.custom_frame_bg_colors["specialbg"],
                                          fg=self.theme.custom_label_colors["foreground"],
                                          font=(self.theme.set_font, self.theme.set_font_size + 1))
        self.video_fps_menu_label.grid(row=0, column=0, padx=10, pady=0, sticky=W)

        # video FPS entry box
        self.fps_entry = Entry(self.video_tab2, state=DISABLED, width=10, borderwidth=4,
                               fg=self.theme.custom_entry_colors["foreground"],
                               bg=self.theme.custom_entry_colors["background"],
                               disabledforeground=self.theme.custom_entry_colors["disabledforeground"],
                               disabledbackground=self.theme.custom_entry_colors["disabledbackground"])
        self.fps_entry.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=W + E)

        # dolby vision
        self.dolby_profiles = {'None': '',
                               'Profile 5': ':dv-profile=5:hdr=none',
                               'Profile 8.1 (HDR10)': ':dv-profile=8.hdr10:hdr=none',
                               'Profile 8.2 (bt709)': ':dv-profile=8.bt709:hdr=none'}

        self.dolby_v_profile_menu_label = Label(self.video_tab2, text='Dolby Vision:', bd=0,
                                                relief=SUNKEN,
                                                background=self.theme.custom_frame_bg_colors["specialbg"],
                                                fg=self.theme.custom_label_colors["foreground"],
                                                font=(self.theme.set_font, self.theme.set_font_size + 1))
        self.dolby_v_profile_menu_label.grid(row=0, column=1, padx=10, pady=0, sticky=W)

        self.dolby_v_profile_combo = ttk.Combobox(self.video_tab2, values=list(self.dolby_profiles.keys()),
                                                  justify="center", width=20,
                                                  font=(self.theme.set_font, self.theme.set_font_size + 3))
        self.dolby_v_profile_combo.grid(row=1, column=1, padx=10, pady=(0, 10), sticky=W)
        self.dolby_v_profile_combo['state'] = 'readonly'

    def _manual_video_input(self):
        """
        GUI dialog function for video input when the video button is clicked
        If the user loads an input file run _open_video_source()
        """
        self.vid_input = filedialog.askopenfilename(parent=self.mp4_win, initialdir="/", title="Select Video File")

        if self.vid_input:
            self._open_video_source(video_input=self.vid_input)

    def _open_video_source(self, video_input):
        """
        Open input file with MediaInfo to check for and parse the video tracks
        If there is not a video track present clear the video input box and exit
        If there is a video track present run self._import_video()
        """
        self.video_track = MediaInfo.parse(pathlib.Path(video_input))

        if not self.video_track.video_tracks:
            messagebox.showerror(parent=self.mp4_win, title="Error",
                                 message=f"'{str(pathlib.Path(video_input).name)}':\n\nInput file does not contain "
                                         f"any video tracks")
            self._clear_video_input()

        elif self.video_track.video_tracks:
            # get video track id/information
            video_track_instance = VideoTrackSelection(self.mp4_win, video_input)
            get_video_track_info = video_track_instance.get()

            self._import_video(video_input, get_video_track_info)

    def _import_video(self, video_input, video_track_info):
        """
        RETYPE THIS UP:
        Work in here or build another module that allows extraction with progress via ffmpeg for known formats to
        be imported into mp4box
        """
        direct_import_extensions = (".263", ".263", ".264", ".265", ".26L", ".av1", ".avi", ".cmp", ".h264", ".h265",
                                    ".hevc", ".m1v", ".m2v", ".m4v", ".mov", ".mp4", ".mpeg", ".mpg", ".ogg", ".qcp",
                                    ".svcd", ".vcd", ".vob")

        if pathlib.Path(video_input).suffix in direct_import_extensions:
            self._update_video_input(video_input)

        elif pathlib.Path(video_input).suffix not in direct_import_extensions:
            extract_track = messagebox.askyesno(parent=self.mp4_win, title="Extract?",
                                message=f"'{str(pathlib.Path(video_input).suffix)}' cannot be directly imported.\n\n"
                                        f"Would you like to automatically extract the elementary stream from the "
                                        f"input file?")

            if extract_track:
                demux = DemuxWindow(self.mp4_win, video_input, video_track_info["track_data"]["stream_identifier"],
                                    "video")

                if demux.status["status"] == "Ok":
                    self._update_video_input(demux.status["output_filename"])

    def _update_video_input(self, video_input):
        video_track_instance = VideoTrackSelection(self.mp4_win, video_input)
        get_video_track_info = video_track_instance.get()
        print(get_video_track_info)

        # update video input entry box
        self.input_entry.config(state=NORMAL)
        self.input_entry.delete(0, END)
        self.input_entry.insert(END, str(pathlib.Path(video_input)))
        self.input_entry.config(state=DISABLED)

        # update language
        self.video_combo_language.set(int(get_video_track_info["detected_language"]))

        # update title
        self.video_title_entry.delete(0, END)
        self.video_title_entry.insert(END, str(get_video_track_info["detected_title"]))

        # update delay
        self.delay_entry.delete(0, END)
        self.delay_entry.insert(END, str(get_video_track_info["detected_delay"]))

        # update framerate
        self.fps_entry.config(state=NORMAL)
        self.fps_entry.delete(0, END)
        self.fps_entry.insert(END, str(get_video_track_info["track_data"]["frame_rate"]))
        self.fps_entry.config(state=DISABLED)

        # detect dolby vision
        # FIX

        # update input variable
        self.video_input = pathlib.Path(video_input)

    def _clear_video_input(self):
        """When user selects 'X' to clear input box"""

        # update video input entry box
        self.input_entry.config(state=NORMAL)
        self.input_entry.delete(0, END)
        self.input_entry.config(state=DISABLED)

        # update language
        self.video_combo_language.set(0)

        # update title
        self.video_title_entry.delete(0, END)

        # update delay
        self.delay_entry.delete(0, END)

        # update framerate
        self.fps_entry.config(state=NORMAL)
        self.fps_entry.delete(0, END)
        self.fps_entry.config(state=DISABLED)

        # detect dolby vision
        # FIX

        # update input variable
        self.video_input = None

    def get_info(self):
        """return a dictionary of file input information"""
        return {"input_file": self.video_input,
                "language": self.video_combo_language.get(),
                "title": self.video_title_entry.get().strip(),
                "delay": self.delay_entry.get().strip(),
                "fps": self.fps_entry.get().strip(),
                # need to add dolby vision FIX
                }
