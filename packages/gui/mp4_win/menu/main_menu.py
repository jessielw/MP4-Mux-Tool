import pathlib
from tkinter import filedialog, StringVar, messagebox, Menu, DISABLED, NORMAL, END
from packages.config.config_params import *
from packages.config.config_writer import config_writer
from packages.gui.chapter_demuxer.chapterdemuxer import ChapterDemux
from packages.gui.about.about import openaboutwindow


class MainMenu:

    def __init__(self, main_gui):
        self.mp4_win = main_gui.mp4_win
        # create menu bar
        self.my_menu_bar = Menu(self.mp4_win, tearoff=0)
        self.mp4_win.config(menu=self.my_menu_bar)

        # file menu
        self.file_menu = Menu(self.my_menu_bar, tearoff=0, activebackground='dim grey')
        self.my_menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Clear Inputs', command=self.clear_inputs)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=main_gui.mp4_win_exit_function)

        # options menu
        self.options_menu = Menu(self.my_menu_bar, tearoff=0, activebackground='dim grey')
        self.my_menu_bar.add_cascade(label='Options', menu=self.options_menu)
        self.options_submenu = Menu(self.mp4_win, tearoff=0, activebackground='dim grey')
        self.options_menu.add_cascade(label='Shell Options', menu=self.options_submenu)

        # options menu - debug
        self.shell_options = StringVar()
        self.shell_options.set(config['debug_option']['option'])
        self.options_submenu.add_radiobutton(label='Progress Bars', variable=self.shell_options, value="Default",
                                             command=lambda: config_writer('debug_option', 'option',
                                                                           self.shell_options.get()))
        self.options_submenu.add_radiobutton(label='CMD Shell (Debug)', variable=self.shell_options, value="Debug",
                                             command=lambda: config_writer('debug_option', 'option',
                                                                           self.shell_options.get()))

        # options menu - auto close progress window
        self.auto_close_window = StringVar()
        self.auto_close_window.set(config['auto_close_progress_window']['option'])
        self.options_submenu2 = Menu(self.mp4_win, tearoff=0, activebackground='dim grey')
        self.options_menu.add_cascade(label='Auto-Close Progress Window On Completion', menu=self.options_submenu2)
        self.options_submenu2.add_radiobutton(label='On', variable=self.auto_close_window, value='on',
                                              command=lambda: config_writer('auto_close_progress_window',
                                                                            'option', self.auto_close_window.get()))
        self.options_submenu2.add_radiobutton(label='Off', variable=self.auto_close_window, value='off',
                                              command=lambda: config_writer('auto_close_progress_window',
                                                                            'option', self.auto_close_window.get()))

        # options menu - reset config
        self.reset_gui_on_start = StringVar()
        self.reset_gui_on_start.set(config['reset_program_on_start_job']['option'])
        self.options_submenu3 = Menu(self.mp4_win, tearoff=0, activebackground='dim grey')
        self.options_menu.add_cascade(label='Reset GUI When Start Job Is Selected', menu=self.options_submenu3)
        self.options_submenu3.add_radiobutton(label='On', variable=self.reset_gui_on_start, value='on',
                                              command=lambda: config_writer('reset_program_on_start_job',
                                                                            'option', self.reset_gui_on_start.get()))
        self.options_submenu3.add_radiobutton(label='Off', variable=self.reset_gui_on_start, value='off',
                                              command=lambda: config_writer('reset_program_on_start_job',
                                                                            'option', self.reset_gui_on_start.get()))
        self.options_menu.add_separator()

        # options menu - define tool paths
        self.options_menu.add_command(label='Set path to MP4Box', command=self.set_mp4box_path)
        self.options_menu.add_command(label='Set path to mkvextract', command=self.set_mkvextract_path)
        self.options_menu.add_separator()

        # options menu - reset config file
        self.options_menu.add_command(label='Reset Configuration File', command=self.reset_config)

        # tools menu
        self.tools_menu = Menu(self.my_menu_bar, tearoff=0, activebackground="dim grey")
        self.my_menu_bar.add_cascade(label="Tools", menu=self.tools_menu)

        # tools menu - Chapter Demuxer
        self.tools_menu.add_command(label='Chapter Demuxer',
                                    command=lambda: ChapterDemux(master=self.mp4_win, standalone=False))

        # help menu
        self.help_menu = Menu(self.my_menu_bar, tearoff=0, activebackground="dim grey")
        self.my_menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # help menu - About
        self.help_menu.add_command(label="About", command=openaboutwindow)


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

    def set_mp4box_path(self):
        """dialog to set the path to mp4box"""
        path = filedialog.askopenfilename(parent=self.mp4_win, title='Select Location to "mp4box.exe"',
                                          filetypes=[('MP4Box', 'mp4box.exe')])
        if pathlib.Path(path).is_file():
            config_writer('mp4box_path', 'path', str(pathlib.Path(path)))

    def set_mkvextract_path(self):
        """dialog to set the path to mkvextract"""
        path = filedialog.askopenfilename(parent=self.mp4_win, title='Select Location to "mkvextract.exe"',
                                          filetypes=[('mkvextract', 'mkvextract.exe')])
        if pathlib.Path(path).is_file():
            config_writer('mkvextract_path', 'path', str(pathlib.Path(path)))

    def reset_config(self):
        """dialog for user to confirm config reset"""
        msg = messagebox.askyesno(parent=self.mp4_win, title='Warning',
                                  message='Are you sure you want to reset the config.ini file settings?')
        if msg:
            config_writer('mp4box_path', 'path', '')
            config_writer('mkvextract_path', 'path', '')
            config_writer('debug_option', 'option', '')
            config_writer('auto_close_progress_window', 'option', '')
            config_writer('reset_program_on_start_job', 'option', '')
            self.mp4_win_exit_function()

