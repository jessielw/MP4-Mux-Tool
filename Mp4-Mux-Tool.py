# Imports--------------------------------------------------------------------------------------------------------------
import pathlib
import pyperclip
import subprocess
import threading
import tkinter as tk
import tkinter.scrolledtext as scrolledtextwidget
import webbrowser
from configparser import ConfigParser
from ctypes import windll
from tkinter import filedialog, StringVar, ttk, messagebox, PhotoImage, Menu, LabelFrame, E, N, S, W, Label, \
    Entry, DISABLED, NORMAL, END, Frame, Spinbox, CENTER, Checkbutton, HORIZONTAL, Toplevel, SUNKEN, OptionMenu

from TkinterDnD2 import *
from pymediainfo import MediaInfo

from ISO_639_2 import *
from Packages.about import openaboutwindow


# ------------------------------------------------------------------------------------------------------------- Imports


# Main Gui & Windows --------------------------------------------------------------------------------------------------
def mp4_root_exit_function():  # Pop up window when you file + exit or press 'X' to close the program
    confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
                                                               "     Note: This will end all current tasks!",
                                       parent=mp4_root)
    if confirm_exit:  # If user selects 'Yes', program attempts to kill all tasks then closes GUI
        try:
            subprocess.Popen(f"TASKKILL /F /im MP4-Mux-Tool.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
            mp4_root.destroy()
        except (Exception,):
            mp4_root.destroy()


mp4_root = TkinterDnD.Tk()  # Main loop with DnD.Tk() module (for drag and drop)
mp4_root.title("MP4-Mux-Tool v1.0")  # Sets the version of the program
mp4_root.iconphoto(True, PhotoImage(file='Runtime/Images/mp4mux.png'))  # Sets icon for all windows
mp4_root.configure(background="#434547")  # Sets gui background color
window_height = 760  # Gui window height
window_width = 605  # Gui window width
screen_width = mp4_root.winfo_screenwidth()  # down
screen_height = mp4_root.winfo_screenheight()  # down
x_coordinate = int((screen_width / 2) - (window_width / 2))  # down
y_coordinate = int((screen_height / 2) - (window_height / 2))  # down
mp4_root.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')  # does the math for center open
mp4_root.protocol('WM_DELETE_WINDOW', mp4_root_exit_function)  # Code to use exit function when selecting 'X'

# Block of code to fix DPI awareness issues on Windows 7 or higher
try:
    windll.shcore.SetProcessDpiAwareness(1)  # if your Windows version >= 8.1
except(Exception,):
    windll.user32.SetProcessDPIAware()  # Windows 8.0 or less
# Block of code to fix DPI awareness issues on Windows 7 or higher

# Config Parser -------------------------------------------------------------------------------------------------------
config_file = 'Runtime/config.ini'  # Creates (if it doesn't exist) and defines location of config.ini
config = ConfigParser()
config.read(config_file)

if not config.has_section('mp4box_path'):  # Creates mp4box.exe config info
    config.add_section('mp4box_path')
if not config.has_option('mp4box_path', 'path'):
    config.set('mp4box_path', 'path', '')

if not config.has_section('debug_option'):  # Creates debug config info
    config.add_section('debug_option')
if not config.has_option('debug_option', 'option'):
    config.set('debug_option', 'option', '')

if not config.has_section('auto_close_progress_window'):  # Creates auto close progress on complete config info
    config.add_section('auto_close_progress_window')
if not config.has_option('auto_close_progress_window', 'option'):
    config.set('auto_close_progress_window', 'option', '')

if not config.has_section('reset_program_on_start_job'):  # Creates reset main gui on start job config info
    config.add_section('reset_program_on_start_job')
if not config.has_option('reset_program_on_start_job', 'option'):
    config.set('reset_program_on_start_job', 'option', '')

try:  # writes all the above config information to config.ini file
    with open(config_file, 'w') as configfile:
        config.write(configfile)
except (Exception,):  # If for some reason there is an error writing the file, this pop up window will let you know
    messagebox.showinfo(title='Error', message='Could Not Write to config.ini file, delete and try again')
# ------------------------------------------------------------------------------------------------------- Config Parser

# Menu Items and Sub-Bars ---------------------------------------------------------------------------------------------
my_menu_bar = Menu(mp4_root, tearoff=0)
mp4_root.config(menu=my_menu_bar)

file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='File', menu=file_menu)


def clear_inputs():  # Clears/Resets the entire GUI/variables to "default" or None

    global VideoInput, video_title_cmd_input, video_title_entrybox, video_combo_language, dolby_v_profile_combo, \
        input_entry, detect_video_fps, audio_input, audio_title_cmd, audio_title_entrybox, audio_delay, \
        audio_input_entry, subtitle_input, subtitle_input_entry, subtitle_language, subtitle_title_cmd_input, \
        subtitle_title_entrybox, chapter_input, chapter_input_entry, chapter_title_cmd_input, output, output_entry
    try:  # Video Reset
        video_title_cmd_input = ''
        video_title_entrybox.configure(state=NORMAL)
        video_title_entrybox.delete(0, END)
        video_title_entrybox.configure(state=DISABLED)
        video_combo_language.current(0)
        input_entry.configure(state=NORMAL)
        input_entry.delete(0, END)
        input_entry.configure(state=DISABLED)
        fps_entry.configure(state=NORMAL)
        fps_entry.delete(0, END)
        fps_entry.configure(state=DISABLED)
        dolby_v_profile_combo.current(0)
        status_label.configure(text='Select "Open File" or drag and drop a video file to begin')
        show_command.configure(state=DISABLED)
        start_button.configure(state=DISABLED)
        del VideoInput
        del detect_video_fps
    except NameError as v:
        v_error = str(v)

    try:  # Audio Reset
        audio_title_cmd = ''
        audio_title_entrybox.delete(0, END)
        audio_title_entrybox.configure(state=DISABLED)
        audio_input_entry.configure(state=NORMAL)
        audio_input_entry.delete(0, END)
        audio_input_entry.configure(state=DISABLED)
        audio_language.current(0)
        audio_delay.set(0)
        audio_input_button.configure(state=DISABLED)
        del audio_input
    except NameError as a1:
        a1_error = str(a1)

    try:  # Subtitle Reset
        subtitle_title_cmd_input = ''
        subtitle_input_entry.configure(state=NORMAL)
        subtitle_input_entry.delete(0, END)
        subtitle_input_entry.configure(state=DISABLED)
        subtitle_title_entrybox.configure(state=NORMAL)
        subtitle_title_entrybox.delete(0, END)
        subtitle_title_entrybox.configure(state=DISABLED)
        subtitle_language.current(0)
        subtitle_input_button.configure(state=DISABLED)
        del subtitle_input
    except NameError as s1:
        s1_error = str(s1)

    try:  # Chapter Reset
        chapter_title_cmd_input = ''
        chapter_input_entry.configure(state=NORMAL)
        chapter_input_entry.delete(0, END)
        chapter_input_entry.configure(state=DISABLED)
        chapter_input_button.configure(state=DISABLED)
        del chapter_input
    except NameError as c:
        c_error = str(c)

    try:  # Output Reset
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.configure(state=DISABLED)
        output_button.configure(state=DISABLED)
        del output
    except NameError as o:
        o_error = str(o)


file_menu.add_command(label='Clear Inputs', command=clear_inputs)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=mp4_root_exit_function)

options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='Options', menu=options_menu)

options_submenu = Menu(mp4_root, tearoff=0, activebackground='dim grey')
options_menu.add_cascade(label='Shell Options', menu=options_submenu)
shell_options = StringVar()
shell_options.set(config['debug_option']['option'])
if shell_options.get() == '':
    shell_options.set('Default')
elif shell_options.get() != '':
    shell_options.set(config['debug_option']['option'])


def update_shell_option():
    try:
        config.set('debug_option', 'option', shell_options.get())
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    except (Exception,):
        pass


update_shell_option()
options_submenu.add_radiobutton(label='Progress Bars', variable=shell_options, value="Default",
                                command=update_shell_option)
options_submenu.add_radiobutton(label='CMD Shell (Debug)', variable=shell_options, value="Debug",
                                command=update_shell_option)

auto_close_window = StringVar()
auto_close_window.set(config['auto_close_progress_window']['option'])
if auto_close_window.get() == '':
    auto_close_window.set('on')
elif auto_close_window.get() != '':
    auto_close_window.set(config['auto_close_progress_window']['option'])


def update_auto_close():
    try:
        config.set('auto_close_progress_window', 'option', auto_close_window.get())
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    except (Exception,):
        pass


update_auto_close()
options_submenu2 = Menu(mp4_root, tearoff=0, activebackground='dim grey')
options_menu.add_cascade(label='Auto-Close Progress Window On Completion', menu=options_submenu2)
options_submenu2.add_radiobutton(label='On', variable=auto_close_window, value='on', command=update_auto_close)
options_submenu2.add_radiobutton(label='Off', variable=auto_close_window, value='off', command=update_auto_close)

reset_gui_on_start = StringVar()
reset_gui_on_start.set(config['reset_program_on_start_job']['option'])
if reset_gui_on_start.get() == '':
    reset_gui_on_start.set('on')
elif reset_gui_on_start.get() != '':
    reset_gui_on_start.set(config['reset_program_on_start_job']['option'])


def update_reset_on_job():
    try:
        config.set('reset_program_on_start_job', 'option', reset_gui_on_start.get())
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    except (Exception,):
        pass


update_reset_on_job()
options_submenu3 = Menu(mp4_root, tearoff=0, activebackground='dim grey')
options_menu.add_cascade(label='Reset GUI When Start Job Is Selected', menu=options_submenu3)
options_submenu3.add_radiobutton(label='On', variable=reset_gui_on_start, value='on', command=update_reset_on_job)
options_submenu3.add_radiobutton(label='Off', variable=reset_gui_on_start, value='off', command=update_reset_on_job)

options_menu.add_separator()


def set_mp4box_path():
    global mp4box
    path = filedialog.askopenfilename(title='Select Location to "mp4box.exe"', initialdir='/',
                                      filetypes=[('MP4Box', 'mp4box.exe')])
    if path != '':
        mp4box = '"' + str(pathlib.Path(path)) + '"'
        config.set('mp4box_path', 'path', mp4box)
        with open(config_file, 'w') as configfile:
            config.write(configfile)


options_menu.add_command(label='Set path to MP4Box', command=set_mp4box_path)
options_menu.add_separator()


def reset_config():
    msg = messagebox.askyesno(title='Warning', message='Are you sure you want to reset the config.ini file settings?')
    if msg:
        try:
            config.set('mp4box_path', 'path', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            messagebox.showinfo(title='Prompt', message='Please restart the program')
            subprocess.Popen(f"TASKKILL /F /im MP4-Mux-Tool.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
        except (Exception,):
            mp4_root.destroy()
        mp4_root.destroy()


options_menu.add_command(label='Reset Configuration File', command=reset_config)

help_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
my_menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=openaboutwindow)

# --------------------------------------------------------------------------------------------- Menu Items and Sub-Bars


# Themes --------------------------------------------------------------------------------------------------------------
# Custom Tkinter Theme-----------------------------------------
custom_style = ttk.Style()
custom_style.theme_create('jlw_style', parent='alt', settings={
    # Notebook Theme Settings -------------------
    "TNotebook": {"configure": {"tabmargins": [5, 5, 5, 0]}},
    "TNotebook.Tab": {"configure": {"padding": [5, 1], "background": 'grey', 'foreground': 'white', 'focuscolor': ''},
                      "map": {"background": [("selected", '#434547')], "expand": [("selected", [1, 1, 1, 0])]}},
    # Notebook Theme Settings -------------------
    # ComboBox Theme Settings -------------------
    'TCombobox': {'configure': {'selectbackground': '#23272A', 'fieldbackground': '#23272A',
                                'background': 'white', 'foreground': 'white'}}}
                          # ComboBox Theme Settings -------------------
                          )
custom_style.theme_use('jlw_style')  # Enable the use of the custom theme
# ComboBox Mouse Hover Code ----------------------------------
mp4_root.option_add('*TCombobox*Listbox*Background', '#404040')
mp4_root.option_add('*TCombobox*Listbox*Foreground', '#FFFFFF')
mp4_root.option_add('*TCombobox*Listbox*selectBackground', '#FFFFFF')
mp4_root.option_add('*TCombobox*Listbox*selectForeground', '#404040')
custom_style.map('TCombobox', foreground=[('hover', 'white')], background=[('hover', 'grey')])
custom_style.configure("purple.Horizontal.TProgressbar", background='purple')


# ----------------------------------- ComboBox Mouse Hover Code
# ------------------------------------------ Custom Tkinter Theme

# Hover over button theme ---------------------------------------
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


# --------------------------------------- Hover over button theme
# -------------------------------------------------------------------------------------------------------------- Themes

# mp4_root Row/Column Configure ---------------------------------------------------------------------------------------
for n in range(3):
    mp4_root.grid_columnconfigure(n, weight=1)
for n in range(6):
    mp4_root.grid_rowconfigure(n, weight=1)

# --------------------------------------------------------------------------------------- mp4_root Row/Column Configure

# Bundled Apps --------------------------------------------------------------------------------------------------------
mp4box = config['mp4box_path']['path']

if not pathlib.Path(mp4box.replace('"', '')).is_file():  # Checks config for bundled app paths path
    # mp4box -----------------------------------------------------------------------
    if pathlib.Path('Apps/mp4box/MP4Box.exe').is_file():  # If mp4box.exe is located in the apps folder
        messagebox.showinfo(title='Info', message='Program will use the included '
                                                  '"mp4box.exe" located in the "Apps" folder')
        mp4box = '"' + str(pathlib.Path('Apps/mp4box/MP4Box.exe')) + '"'  # sets variable to mp4box.exe
        try:  # Write path location to config.ini file
            config.set('mp4box_path', 'path', mp4box)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):  # If unable to write path to mp4box.exe present error message
            messagebox.showerror(title='Error!', message=f'Could not save path to mp4box at '
                                                         f'\n{mp4box}\n please try again')
    elif not pathlib.Path('Apps/mp4box/MP4Box.exe').is_file():  # If mp4box.exe does not exist
        messagebox.showerror(title='Error!', message='Please download mp4box.exe and set path to '
                                                     'mp4box.exe in the Options menu')  # Error message
        webbrowser.open('https://github.com/gpac/gpac/wiki/MP4Box')  # Opens default web-browser to mp4box github
    # mp4box ------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------- Bundled Apps
# Video Frame ---------------------------------------------------------------------------------------------------------
video_frame = LabelFrame(mp4_root, text=' Video ')
video_frame.grid(row=0, columnspan=3, sticky=E + W + N + S, padx=20, pady=(5, 0))
video_frame.configure(fg="white", bg="#434547", bd=4)

video_frame.grid_columnconfigure(0, weight=1)
video_frame.grid_rowconfigure(0, weight=1)

# Video Notebook Frame ------------------------------------------------------------------------------------------------
tabs = ttk.Notebook(video_frame, height=110)
tabs.grid(row=0, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)
video_tab = Frame(tabs, background="#434547")
video_tab2 = Frame(tabs, background="#434547")
tabs.add(video_tab, text=' Input ')
tabs.add(video_tab2, text=' Options ')

for n in range(4):
    video_tab.grid_columnconfigure(n, weight=1)
for n in range(3):
    video_tab.grid_rowconfigure(n, weight=1)


# ------------------------------------------------------------------------------------------------ Video Notebook Frame


# Entry Box for Video Title -------------------------------------------------------------------------------------------
def video_title(*args):
    global video_title_cmd_input
    if video_title_cmd.get().strip() == '':  # If title box string is empty or only white space
        video_title_cmd_input = ':name='  # .strip() is used to remove all white space from left or right of a string
    else:  # If title box string has characters
        video_title_cmd_input = ':name=' + video_title_cmd.get().strip()


video_title_cmd = StringVar()
video_title_entrybox_label = Label(video_tab, text='Video Title:', anchor=W, background='#434547', foreground='white')
video_title_entrybox_label.grid(row=1, column=1, columnspan=1, padx=10, pady=(0, 0), sticky=W)
video_title_entrybox = Entry(video_tab, textvariable=video_title_cmd, borderwidth=4, background='#CACACA',
                             state=DISABLED)
video_title_entrybox.grid(row=2, column=1, columnspan=1, padx=(5, 15), pady=(0, 15), sticky=W + E)
video_title_cmd.trace('w', video_title)
video_title_cmd.set('')
# ---------------------------------------------------------------------------------------------------- Video Title Line

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
# video_fps_menu_label = Label(video_tab, text='Framerate (FPS):', background="#434547", foreground="white")
# video_fps_menu_label.grid(row=1, column=3, columnspan=1, padx=10, pady=(0, 0), sticky=W)
# combo_fps = ttk.Combobox(video_tab, values=list(video_fps_choices.keys()), justify="center",
#                          textvariable=video_fps, width=10)
# combo_fps.grid(row=2, column=3, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
# combo_fps['state'] = 'readonly'
# combo_fps.current(0)

# Video FPS Label is only for viewing purposes, you need input FPS for program to know what fps to output
video_fps_menu_label = Label(video_tab, text='Framerate (FPS):', background="#434547", foreground="white")
video_fps_menu_label.grid(row=1, column=2, columnspan=1, padx=(3, 0), pady=(0, 0), sticky=W)
fps_entry = Entry(video_tab, borderwidth=4, background='#CACACA', state=DISABLED, width=10)
fps_entry.grid(row=2, column=2, columnspan=2, padx=(5, 10), pady=(0, 15), sticky=W + E)

#
# # --------------------------------------------------------------------------------------------------------- Video FPS

# Video Language Selection --------------------------------------------------------------------------------------------
video_language = StringVar()
video_language_menu_label = Label(video_tab, text='Language:', background="#434547", foreground="white")
video_language_menu_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=W)
video_combo_language = ttk.Combobox(video_tab, values=list(iso_639_2_codes_dictionary.keys()), justify="center",
                                    textvariable=video_language, width=15)
video_combo_language.grid(row=2, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=W + E + N + S)
video_combo_language['state'] = 'readonly'
video_combo_language.current(0)  # Sets language to index 0 (UND) by default

# ------------------------------------------------------------------------------------------------------ Video Language

# Dolby Vision --------------------------------------------------------------------------------------------------------
dolby_profiles = {'None': '', 'Profile 5': ':dv-profile=5:hdr=none', 'Profile 8.1': ':dv-profile=8.hdr10:hdr=none',
                  'Profile 8.2': ':dv-profile=8.bt709:hdr=none'}
dolby_v_profile = StringVar()
dolby_v_profile_menu_label = Label(video_tab2, text='Dolby Vision:', background="#434547", foreground="white")
dolby_v_profile_menu_label.grid(row=0, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=W)
dolby_v_profile_combo = ttk.Combobox(video_tab2, values=list(dolby_profiles.keys()), justify="center",
                                     textvariable=dolby_v_profile, width=15)
dolby_v_profile_combo.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=W + E + N + S)
dolby_v_profile_combo['state'] = 'readonly'
dolby_v_profile_combo.current(0)  # Sets profile to index 0 ('') by default


# -------------------------------------------------------------------------------------------------------- Dolby Vision

def input_button_commands():  # Open file block of code (non drag and drop)
    global VideoInput, autosavefilename, autofilesave_dir_path, VideoInputQuoted, output, detect_video_fps, \
        fps_entry, output_quoted
    video_extensions = ('.avi', '.mp4', '.m1v', '.m2v', '.m4v', '.264', '.h264', '.hevc', '.h265')
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=[("Supported Formats", video_extensions)])
    if VideoInput:
        input_entry.configure(state=NORMAL)
        input_entry.delete(0, END)
        if VideoInput.endswith(video_extensions):
            autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
            autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
            VideoInputQuoted = '"' + str(pathlib.Path(VideoInput)) + '"'
            input_entry.insert(0, str(pathlib.Path(VideoInput)))
            filename = pathlib.Path(VideoInput)
            VideoOut = filename.with_suffix('')
            autosavefilename = str(VideoOut.name) + '.muxed_output'
            autosave_file_dir = pathlib.Path(str(f'{autofilesave_dir_path}\\') + str(autosavefilename + '.mp4'))
            output = str(autosave_file_dir)
            output_quoted = '"' + output + '"'
            input_entry.configure(state=DISABLED)
            video_title_entrybox.configure(state=NORMAL)
            output_entry.configure(state=NORMAL)
            output_entry.delete(0, END)
            output_entry.configure(state=DISABLED)
            output_entry.configure(state=NORMAL)
            output_entry.insert(0, str(autosave_file_dir))
            output_entry.configure(state=DISABLED)
            output_button.configure(state=NORMAL)
            audio_input_button.configure(state=NORMAL)
            subtitle_input_button.configure(state=NORMAL)
            chapter_input_button.configure(state=NORMAL)
            output_button.configure(state=NORMAL)
            start_button.configure(state=NORMAL)
            show_command.configure(state=NORMAL)
            media_info = MediaInfo.parse(filename)
            for track in media_info.tracks:  # Use mediainfo module to parse video section to collect frame rate
                if track.track_type == "Video":
                    detect_video_fps = track.frame_rate
                    fps_entry.configure(state=NORMAL)
                    fps_entry.delete(0, END)
                    fps_entry.insert(0, detect_video_fps)
                    fps_entry.configure(state=DISABLED)
                    try:  # Code to detect the position of the language code, for 3 digit, and set it to a variable
                        detect_index = [len(i) for i in track.other_language].index(3)
                        language_index = list(iso_639_2_codes_dictionary.values()).index(
                            track.other_language[detect_index])
                        video_combo_language.current(language_index)
                        video_title_entrybox.delete(0, END)
                        video_title_entrybox.insert(0, track.title)
                    except(Exception,):
                        pass
        else:
            messagebox.showinfo(title='Input Not Supported',  # Error message if input is not a supported file type
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.\n\n"
                                        + 'Unsupported file extension "' + str(pathlib.Path(VideoInput).suffix) + '"')
            video_combo_language.current(0)
            video_title_entrybox.delete(0, END)
            fps_entry.configure(state=NORMAL)
            fps_entry.delete(0, END)
            fps_entry.configure(state=DISABLED)
            del detect_video_fps
            del VideoInput


# ---------------------------------------------------------------------------------------------- Input Functions Button

# Drag and Drop Functions ---------------------------------------------------------------------------------------------
def video_drop_input(event):  # Drag and drop function
    input_dnd.set(event.data)


def update_file_input(*args):  # Drag and drop block of code
    global VideoInput, autofilesave_dir_path, VideoInputQuoted, output, autosavefilename, detect_video_fps, \
        fps_entry, output_quoted
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    VideoInput = str(input_dnd.get()).replace("{", "").replace("}", "")
    video_extensions = ('.avi', '.mp4', '.m1v', '.m2v', '.m4v', '.264', '.h264', '.hevc', '.h265')
    if VideoInput.endswith(video_extensions):
        autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
        autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
        VideoInputQuoted = '"' + str(pathlib.Path(VideoInput)) + '"'
        input_entry.insert(0, str(input_dnd.get()).replace("{", "").replace("}", ""))
        filename = pathlib.Path(VideoInput)
        VideoOut = filename.with_suffix('')
        autosavefilename = str(VideoOut.name) + '.muxed_output'
        autosave_file_dir = pathlib.Path(str(f'{autofilesave_dir_path}\\') + str(autosavefilename + '.mp4'))
        output = str(autosave_file_dir)
        output_quoted = '"' + output + '"'
        input_entry.configure(state=DISABLED)
        video_title_entrybox.configure(state=NORMAL)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.configure(state=DISABLED)
        output_entry.configure(state=NORMAL)
        output_entry.insert(0, str(autosave_file_dir))
        output_entry.configure(state=DISABLED)
        output_button.configure(state=NORMAL)
        audio_input_button.configure(state=NORMAL)
        subtitle_input_button.configure(state=NORMAL)
        chapter_input_button.configure(state=NORMAL)
        output_button.configure(state=NORMAL)
        start_button.configure(state=NORMAL)
        show_command.configure(state=NORMAL)
        media_info = MediaInfo.parse(filename)
        for track in media_info.tracks:
            if track.track_type == "Video":
                detect_video_fps = track.frame_rate
                fps_entry.configure(state=NORMAL)
                fps_entry.delete(0, END)
                fps_entry.insert(0, detect_video_fps)
                fps_entry.configure(state=DISABLED)
                try:
                    detect_index = [len(i) for i in track.other_language].index(3)
                    language_index = list(iso_639_2_codes_dictionary.values()).index(
                        track.other_language[detect_index])
                    video_combo_language.current(language_index)
                    video_title_entrybox.delete(0, END)
                    video_title_entrybox.insert(0, track.title)
                except(Exception,):
                    pass
    else:
        messagebox.showinfo(title='Input Not Supported',
                            message="Try Again With a Supported File Type!\n\nIf this is a "
                                    "file that should be supported, please let me know.\n\n"
                                    + 'Unsupported file extension "' + str(pathlib.Path(VideoInput).suffix) + '"')
        video_combo_language.current(0)
        video_title_entrybox.delete(0, END)
        fps_entry.configure(state=NORMAL)
        fps_entry.delete(0, END)
        fps_entry.configure(state=DISABLED)
        del detect_video_fps
        del VideoInput


# --------------------------------------------------------------------------------------------- Drag and Drop Functions


# Buttons -------------------------------------------------------------------------------------------------------------
input_dnd = StringVar()
input_dnd.trace('w', update_file_input)
input_button = HoverButton(video_tab, text='Open File', command=input_button_commands, foreground='white',
                           background='#23272A', borderwidth='3', activebackground='grey', width=15)
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=W + E)
input_button.drop_target_register(DND_FILES)
input_button.dnd_bind('<<Drop>>', video_drop_input)

input_entry = Entry(video_tab, borderwidth=4, background='#CACACA', state=DISABLED, width=40)
input_entry.grid(row=0, column=1, columnspan=2, padx=(5, 0), pady=5, sticky=W + E)
input_entry.drop_target_register(DND_FILES)
input_entry.dnd_bind('<<Drop>>', video_drop_input)


def clear_video_input():  # When user selects 'X' to clear input box
    global VideoInput, video_title_cmd_input, video_title_entrybox, video_combo_language, input_entry, \
        detect_video_fps, dolby_v_profile_combo
    try:
        video_title_cmd_input = ''
        video_title_entrybox.configure(state=NORMAL)
        video_title_entrybox.delete(0, END)
        video_title_entrybox.configure(state=DISABLED)
        video_combo_language.current(0)
        input_entry.configure(state=NORMAL)
        input_entry.delete(0, END)
        input_entry.configure(state=DISABLED)
        fps_entry.configure(state=NORMAL)
        fps_entry.delete(0, END)
        fps_entry.configure(state=DISABLED)
        dolby_v_profile_combo.current(0)
        del VideoInput
        del detect_video_fps
    except (Exception,):
        pass


delete_input_button = HoverButton(video_tab, text='X', command=clear_video_input, foreground='white',
                                  background='#23272A', borderwidth='3', activebackground='grey', width=2)
delete_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=5, sticky=E)

# ------------------------------------------------------------------------------------------------------------- Buttons
# --------------------------------------------------------------------------------------------------------- Video Frame


# Audio  --------------------------------------------------------------------------------------------------------------
audio_frame = LabelFrame(mp4_root, text=' Audio ')
audio_frame.grid(row=1, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
audio_frame.configure(fg="white", bg="#434547", bd=4)

audio_frame.grid_columnconfigure(0, weight=1)
audio_frame.grid_rowconfigure(0, weight=1)

# Audio Notebook Frame ------------------------------------------------------------------------------------------------
tabs = ttk.Notebook(audio_frame, height=110)
tabs.grid(row=0, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)
audio_tab = Frame(tabs, background="#434547")
tabs.add(audio_tab, text=' Track #1 ')

for n in range(4):
    audio_tab.grid_columnconfigure(n, weight=1)
for n in range(3):
    audio_tab.grid_rowconfigure(n, weight=1)


# ------------------------------------------------------------------------------------------------ Audio Notebook Frame

# Entry Box for Audio Title -------------------------------------------------------------------------------------------
def audio_title(*args):
    global audio_title_cmd_input
    if audio_title_cmd.get().strip() == '':
        audio_title_cmd_input = ':name='
    else:
        audio_title_cmd_input = ':name=' + audio_title_cmd.get().strip()


audio_title_cmd = StringVar()
audio_title_entrybox_label = Label(audio_tab, text='Audio Title:', anchor=W, background='#434547', foreground='white')
audio_title_entrybox_label.grid(row=1, column=1, columnspan=1, padx=10, pady=(0, 0), sticky=W)
audio_title_entrybox = Entry(audio_tab, textvariable=audio_title_cmd, borderwidth=4, background='#CACACA',
                             state=DISABLED)
audio_title_entrybox.grid(row=2, column=1, columnspan=1, padx=10, pady=(0, 15), sticky=W + E)
audio_title_cmd.trace('w', audio_title)
audio_title_cmd.set('')
# ------------------------------------------------------------------------------------------- Entry Box for Audio Title

# Audio Delay Selection -----------------------------------------------------------------------------------------------
audio_delay = StringVar()
audio_delay_label = Label(audio_tab, text="Delay:", background="#434547", foreground="white")
audio_delay_label.grid(row=1, column=3, columnspan=1, padx=10, pady=1, sticky=W)
audio_delay_spinbox = Spinbox(audio_tab, from_=0, to=20000, increment=1.0, justify=CENTER,
                              wrap=True, textvariable=audio_delay, width=14)
audio_delay_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                              buttonbackground="black", readonlybackground="#23272A")
audio_delay_spinbox.grid(row=2, column=3, columnspan=1, padx=10, pady=(1, 8), sticky=W)
audio_delay.set(0)

# --------------------------------------------------------------------------------------------------------- Audio Delay

# Audio Language Selection --------------------------------------------------------------------------------------------
audio_language = StringVar()
audio_language_menu_label = Label(audio_tab, text='Language:', background="#434547", foreground="white")
audio_language_menu_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=W)
audio_language = ttk.Combobox(audio_tab, values=list(iso_639_2_codes_dictionary.keys()), justify="center",
                              textvariable=audio_language)
audio_language.grid(row=2, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
audio_language['state'] = 'readonly'
audio_language.current(0)


# ------------------------------------------------------------------------------------------------------ Audio Language


# Audio Stream Selection ----------------------------------------------------------------------------------
def check_audio_tracks_info():
    global audio_input

    def audio_track_choice():  # If audio input has only 1 audio track
        global acodec_stream, acodec_stream_choices
        acodec_stream = StringVar()  # Makes a new variable
        acodec_stream_choices = {'Only One Track': '#1'}  # Makes a new dictionary with #1 as the only option
        acodec_stream.set('Only One Track')  # Sets variable to select #1 for command line

    def audio_track_choices(*args):  # If audio input has more then 2 audio tracks, makes a new window to select track
        global acodec_stream, acodec_stream_choices
        audio_track_win = Toplevel()  # Toplevel window
        audio_track_win.configure(background='#191a1a')  # Set color of audio_track_win background
        window_height = 180  # win height
        window_width = 480  # win width
        screen_width = audio_track_win.winfo_screenwidth()  # down
        screen_height = audio_track_win.winfo_screenheight()  # down
        x_coordinate = int((screen_width / 2) - (window_width / 2))  # down
        y_coordinate = int((screen_height / 2) - (window_height / 2))  # down
        audio_track_win.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')  # code calculates
        # middle position of window
        audio_track_win.resizable(0, 0)  # makes window not resizable
        audio_track_win.overrideredirect(1)  # will remove the top badge of window
        audio_track_win.grab_set()  # forces audio_track_win to stay on top of root
        mp4_root.attributes('-alpha', 0.8)  # Lowers mp4root transparency to .8

        # Input Frame -------------------------------------------------------------------------------------------------
        track_frame = LabelFrame(audio_track_win, text=' Track Selection ')
        track_frame.grid(row=0, column=0, columnspan=5, sticky=E + W, padx=10, pady=(8, 0))
        track_frame.configure(fg="white", bg="#636669", bd=3)

        track_frame.rowconfigure(0, weight=1)
        track_frame.grid_columnconfigure(0, weight=1)
        # ------------------------------------------------------------------------------------------------- Input Frame

        # Code to gather multiple audio tracks information for use with the gui ---------------------------------------
        result = []  # Creates an empty list to be filled with the code below
        media_info = MediaInfo.parse(audio_input)  # Uses pymediainfo to get information for track selection
        for track in media_info.tracks:
            if track.track_type == 'Audio':
                if str(track.format) != 'None':  # Gets format string of tracks (aac, ac3 etc...)
                    audio_format = '|  ' + str(track.format) + '  |'
                else:
                    audio_format = ''
                if str(track.channel_s) != 'None':  # Gets audio channels of input tracks
                    audio_channels = '|  ' + 'Channels: ' + str(track.channel_s) + '  |'
                else:
                    audio_channels = ''
                if str(track.other_bit_rate) != 'None':  # Gets audio bitrate of input tracks
                    audio_bitrate = '|  ' + str(track.other_bit_rate).replace('[', '') \
                        .replace(']', '').replace("'", '') + '  |'
                else:
                    audio_bitrate = ''
                if str(track.other_language) != 'None':  # Gets audio language of input tracks
                    audio_language = '|  ' + str(track.other_language[0]) + '  |'
                else:
                    audio_language = ''
                if str(track.title) != 'None':  # Gets audio title of input tracks
                    if len(str(track.title)) > 50:  # Counts title character length
                        audio_title = '|  Title: ' + str(track.title)[:50] + '...  |'  # If title > 50 characters
                    else:
                        audio_title = '|  Title: ' + str(track.title) + '  |'  # If title is < 50 characters
                else:
                    audio_title = ''
                if str(track.other_sampling_rate) != 'None':  # Gets audio sampling rate of input tracks
                    audio_sampling_rate = '|  ' + str(track.other_sampling_rate) \
                        .replace('[', '').replace(']', '').replace("'", '') + '  |'
                else:
                    audio_sampling_rate = ''
                if str(track.other_duration) != 'None':  # Gets audio duration of input tracks
                    audio_duration = '|  ' + str(track.other_duration[0]) + '  |'
                else:
                    audio_duration = ''
                if str(track.delay) != 'None':  # Gets audio delay of input tracks
                    if str(track.delay) == '0':
                        audio_delay = ''
                    else:
                        audio_delay = '|  Delay: ' + str(track.delay) + '  |'
                else:
                    audio_delay = ''
                if str(track.track_id) != 'None':  # Gets track ID of audio inputs (this is needed for mp4box input)
                    audio_track_id = '|  ID: ' + str(track.track_id) + '  |'  # Code for viewing in drop down
                    audio_track_id_get = str(track.track_id)  # Code to save track # into a variable
                else:
                    messagebox.showerror(title='Error!', message='Cannot auto detect track ID')
                audio_track_info = audio_format + audio_channels + audio_bitrate + audio_sampling_rate + \
                                   audio_delay + audio_duration + audio_language + audio_title + audio_track_id
                for new_list in [audio_track_info]:  # Take all the pymedia input and adds it into a list
                    result.append(new_list)
        # ---------------------------------------- Code to gather all the audio tracks information for use with the gui

        # Code to take all the information from the newly created list(s) and put it into a dictionary ----------------
        audio_stream_info_output = {}
        for i in range(int(str(total_audio_tracks)[-1])):
            audio_stream_info_output[f'Track #{i + 1}:   {result[i]}'] = f'#{audio_track_id_get}'
        # ---------------- Code to take all the information from the newly created list(s) and put it into a dictionary

        # Code uses the above dictionary to create a drop-down menu of audio tracks to display/select included track --
        acodec_stream = StringVar()
        acodec_stream_choices = audio_stream_info_output
        acodec_stream.set(next(iter(audio_stream_info_output)))  # set the default option
        acodec_stream_menu = OptionMenu(track_frame, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=48, anchor='w')
        acodec_stream_menu.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")

        # -- Code uses the above dictionary to create a drop-down menu of audio tracks to display/select included track

        # Saves audio window and closes it while restoring transparency of main GUI -----------------------------------
        def close_audio_win():
            mp4_root.attributes('-alpha', 1.0)  # Restores mp4root transparency to default
            audio_track_win.grab_release()
            audio_track_win.destroy()  # Closes audio window

        select_track = HoverButton(track_frame, text="Choose Track", command=close_audio_win, foreground="white",
                                   background="#23272A", borderwidth="3", activebackground='grey')
        select_track.grid(row=1, column=0, columnspan=1, padx=5, pady=(60, 5), sticky=N + S + E + W)
        # ----------------------------------- Saves audio window and closes it while restoring transparency of main GUI

    media_info = MediaInfo.parse(audio_input)
    for track in media_info.tracks:
        if track.track_type == 'General':
            total_audio_tracks = track.count_of_audio_streams
    if total_audio_tracks is not None and int(total_audio_tracks) == 1:
        audio_track_choice()  # Starts single track function
    elif total_audio_tracks is not None and int(total_audio_tracks) >= 2:
        audio_track_choices()  # Starts function for more than 1 track
    else:  # If the input has 0 audio tracks it resets the audio frame gui back to default/none
        audio_delay.set(0)
        audio_language.current(0)
        audio_title_entrybox.delete(0, END)
        audio_input_entry.configure(state=NORMAL)
        audio_input_entry.delete(0, END)
        audio_input_entry.configure(state=DISABLED)
        # Error message explaining why file input failed
        messagebox.showinfo(title='Info', message=f'"{pathlib.Path(audio_input).name}"\n\nhas 0 audio streams, '
                                                  f'please open a file with at least 1 audio stream.')
        del audio_input


def audio_input_button_commands():  # Function for audio input button
    global audio_input, audio_input_quoted
    audio_extensions = ('.ac3', '.aac', '.mp4', '.m4a', '.mp2', '.mp3', '.opus', '.ogg')
    audio_input = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                             filetypes=[("Supported Formats", audio_extensions)])
    if audio_input:
        audio_input_entry.configure(state=NORMAL)
        audio_input_entry.delete(0, END)
        if audio_input.endswith(audio_extensions):
            audio_input_quoted = '"' + str(pathlib.Path(audio_input)) + '"'
            audio_input_entry.insert(0, audio_input)
            audio_input_entry.configure(state=DISABLED)
            audio_title_entrybox.configure(state=NORMAL)
            media_info = MediaInfo.parse(audio_input)
            for track in media_info.tracks:
                if track.track_type == 'Audio':
                    try:  # Uses mediainfo to detect the language of the file and converts it to 3-digit code
                        detect_index = [len(i) for i in track.other_language].index(3)
                        language_index = list(iso_639_2_codes_dictionary.values()).index(
                            track.other_language[detect_index])
                        audio_language.current(language_index)
                        audio_title_entrybox.delete(0, END)
                        audio_title_entrybox.insert(0, track.title)
                    except(Exception,):
                        pass
            check_audio_tracks_info()  # Function to get audio input from input file
        else:  # If file opened isn't a supported format
            messagebox.showinfo(title='Input Not Supported',
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.\n\n"
                                        + 'Unsupported file extension "' + str(pathlib.Path(audio_input).suffix) + '"')
            audio_delay.set(0)
            audio_language.current(0)
            audio_title_entrybox.delete(0, END)
            del audio_input


def update_audio_input(*args):  # Drag and drop function for audio input
    global audio_input, audio_input_quoted
    audio_input_entry.configure(state=NORMAL)
    audio_input_entry.delete(0, END)
    audio_input = str(audio_input_dnd.get()).replace("{", "").replace("}", "")
    audio_extensions = ('.ac3', '.aac', '.mp4', '.m4a', '.mp2', '.mp3', '.opus', '.ogg')
    if audio_input.endswith(audio_extensions):
        audio_input_quoted = '"' + str(pathlib.Path(audio_input)) + '"'
        audio_input_entry.insert(0, audio_input)
        audio_input_entry.configure(state=DISABLED)
        audio_title_entrybox.configure(state=NORMAL)
        media_info = MediaInfo.parse(audio_input)
        for track in media_info.tracks:
            if track.track_type == 'Audio':
                try:
                    detect_index = [len(i) for i in track.other_language].index(3)
                    language_index = list(iso_639_2_codes_dictionary.values()).index(track.other_language[detect_index])
                    audio_language.current(language_index)
                    audio_title_entrybox.delete(0, END)
                    audio_title_entrybox.insert(0, track.title)
                except(Exception,):
                    pass
        check_audio_tracks_info()  # Function to get audio input from input file
    else:  # If file opened isn't a supported format
        messagebox.showinfo(title='Input Not Supported',
                            message="Try Again With a Supported File Type!\n\nIf this is a "
                                    "file that should be supported, please let me know.\n\n"
                                    + 'Unsupported file extension "' + str(pathlib.Path(audio_input).suffix) + '"')
        audio_delay.set(0)
        audio_language.current(0)
        audio_title_entrybox.delete(0, END)
        del audio_input


# Buttons -------------------------------------------------------------------------------------------------------------
def audio_drop_input(event):  # Drag and drop function for audio input
    audio_input_dnd.set(event.data)


audio_input_dnd = StringVar()
audio_input_dnd.trace('w', update_audio_input)
audio_input_button = HoverButton(audio_tab, text='Open File', command=audio_input_button_commands, foreground='white',
                                 background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
audio_input_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)
audio_input_button.drop_target_register(DND_FILES)
audio_input_button.dnd_bind('<<Drop>>', audio_drop_input)

audio_input_entry = Entry(audio_tab, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
audio_input_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)
audio_input_entry.drop_target_register(DND_FILES)
audio_input_entry.dnd_bind('<<Drop>>', audio_drop_input)


def clear_audio_input():  # Deletes all inputs and sets defaults for audio box #1
    global audio_input, audio_title_cmd, audio_title_entrybox, audio_delay, audio_input_entry
    try:
        audio_title_cmd = ''
        audio_title_entrybox.delete(0, END)
        audio_title_entrybox.configure(state=DISABLED)
        audio_input_entry.configure(state=NORMAL)
        audio_input_entry.delete(0, END)
        audio_input_entry.configure(state=DISABLED)
        del audio_input
        audio_language.current(0)
        audio_delay.set(0)
    except (Exception,):
        pass


delete_audio_input_button = HoverButton(audio_tab, text='X', command=clear_audio_input, foreground='white',
                                        background='#23272A', borderwidth='3', activebackground='grey', width=2)
delete_audio_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)

# --------------------------------------------------------------------------------------------------------- Audio Frame


# Subtitle-------------------------------------------------------------------------------------------------------------
subtitle_frame = LabelFrame(mp4_root, text=' Subtitle ')
subtitle_frame.grid(row=2, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
subtitle_frame.configure(fg="white", bg="#434547", bd=4)

subtitle_frame.grid_columnconfigure(0, weight=1)
subtitle_frame.grid_rowconfigure(0, weight=1)

# Subtitle Notebook Frame ---------------------------------------------------------------------------------------------
tabs = ttk.Notebook(subtitle_frame, height=110)
tabs.grid(row=0, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)
subtitle_tab = Frame(tabs, background="#434547")
tabs.add(subtitle_tab, text=' Track #1 ')

for n in range(4):
    subtitle_tab.grid_columnconfigure(n, weight=1)
for n in range(3):
    subtitle_tab.grid_rowconfigure(n, weight=1)


# --------------------------------------------------------------------------------------------- Subtitle Notebook Frame

# Entry Box for Subtitle Title ----------------------------------------------------------------------------------------
def subtitle_title(*args):
    global subtitle_title_cmd_input
    if subtitle_title_cmd.get().strip() == '':
        subtitle_title_cmd_input = ':name='
    else:
        subtitle_title_cmd_input = ':name=' + subtitle_title_cmd.get().strip()


subtitle_title_cmd = StringVar()
subtitle_title_entrybox_label = Label(subtitle_tab, text='Subtitle Title:', anchor=W, background='#434547',
                                      foreground='white')
subtitle_title_entrybox_label.grid(row=1, column=1, columnspan=1, padx=10, pady=(0, 0), sticky=W)
subtitle_title_entrybox = Entry(subtitle_tab, textvariable=subtitle_title_cmd, borderwidth=4, background='#CACACA',
                                state=DISABLED)
subtitle_title_entrybox.grid(row=2, column=1, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
subtitle_title_cmd.trace('w', subtitle_title)
subtitle_title_cmd.set('')
# ---------------------------------------------------------------------------------------- Entry Box for Subtitle Title

# Subtitle Language Selection -----------------------------------------------------------------------------------------
subtitle_language = StringVar()
subtitle_language_menu_label = Label(subtitle_tab, text='Language:', background="#434547", foreground="white")
subtitle_language_menu_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=W)
subtitle_language = ttk.Combobox(subtitle_tab, values=list(iso_639_2_codes_dictionary.keys()), justify="center",
                                 textvariable=subtitle_language)
subtitle_language.grid(row=2, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
subtitle_language['state'] = 'readonly'
subtitle_language.current(0)


# --------------------------------------------------------------------------------------------------- Subtitle Language


def subtitle_input_button_commands():
    global subtitle_input, subtitle_input_quoted
    subtitle_extensions = ('.srt', '.idx', '.ttxt')
    subtitle_input = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                filetypes=[("Supported Formats", subtitle_extensions)])
    if subtitle_input:
        subtitle_input_entry.configure(state=NORMAL)
        subtitle_input_entry.delete(0, END)
        if subtitle_input.endswith(subtitle_extensions):
            subtitle_input_quoted = '"' + str(pathlib.Path(subtitle_input)) + '"'
            subtitle_input_entry.insert(0, subtitle_input)
            subtitle_input_entry.configure(state=DISABLED)
            subtitle_title_entrybox.configure(state=NORMAL)
        else:
            messagebox.showinfo(title='Input Not Supported',
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.\n\n"
                                        + 'Unsupported file extension "'
                                        + str(pathlib.Path(subtitle_input).suffix) + '"')
            subtitle_language.current(0)
            subtitle_title_entrybox.delete(0, END)
            del subtitle_input


def update_subtitle_input(*args):
    global subtitle_input, subtitle_input_quoted
    subtitle_input_entry.configure(state=NORMAL)
    subtitle_input_entry.delete(0, END)
    subtitle_input = str(subtitle_input_dnd.get()).replace("{", "").replace("}", "")
    subtitle_extensions = ('.srt', '.idx', '.ttxt')
    if subtitle_input.endswith(subtitle_extensions):
        subtitle_input_quoted = '"' + str(pathlib.Path(subtitle_input)) + '"'
        subtitle_input_entry.insert(0, subtitle_input)
        subtitle_input_entry.configure(state=DISABLED)
        subtitle_title_entrybox.configure(state=NORMAL)
    else:
        messagebox.showinfo(title='Input Not Supported',
                            message="Try Again With a Supported File Type!\n\nIf this is a "
                                    "file that should be supported, please let me know.\n\n"
                                    + 'Unsupported file extension "' + str(pathlib.Path(subtitle_input).suffix) + '"')
        subtitle_language.current(0)
        subtitle_title_entrybox.delete(0, END)
        del subtitle_input


# Buttons -------------------------------------------------------------------------------------------------------------
def subtitle_drop_input(event):
    subtitle_input_dnd.set(event.data)


subtitle_input_dnd = StringVar()
subtitle_input_dnd.trace('w', update_subtitle_input)
subtitle_input_button = HoverButton(subtitle_tab, text='Open File', command=subtitle_input_button_commands,
                                    foreground='white', background='#23272A', borderwidth='3', activebackground='grey',
                                    state=DISABLED)
subtitle_input_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)
subtitle_input_button.drop_target_register(DND_FILES)
subtitle_input_button.dnd_bind('<<Drop>>', subtitle_drop_input)

subtitle_input_entry = Entry(subtitle_tab, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
subtitle_input_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)
subtitle_input_entry.drop_target_register(DND_FILES)
subtitle_input_entry.dnd_bind('<<Drop>>', subtitle_drop_input)


def clear_subtitle_input():  # Deletes all inputs and sets defaults for subtitle box #1
    global subtitle_input, subtitle_input_entry, subtitle_language, subtitle_title_cmd_input, subtitle_title_entrybox
    try:
        subtitle_title_cmd_input = ''
        subtitle_input_entry.configure(state=NORMAL)
        subtitle_input_entry.delete(0, END)
        subtitle_input_entry.configure(state=DISABLED)
        subtitle_title_entrybox.configure(state=NORMAL)
        subtitle_title_entrybox.delete(0, END)
        subtitle_title_entrybox.configure(state=DISABLED)
        del subtitle_input
        subtitle_language.current(0)

    except (Exception,):
        pass


delete_subtitle_input_button = HoverButton(subtitle_tab, text='X', command=clear_subtitle_input, foreground='white',
                                           background='#23272A', borderwidth='3', activebackground='grey', width=2)
delete_subtitle_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)

# ------------------------------------------------------------------------------------------------------ Subtitle Frame


# Chapter -------------------------------------------------------------------------------------------------------------
chapter_frame = LabelFrame(mp4_root, text=' Chapter ')
chapter_frame.grid(row=3, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
chapter_frame.configure(fg="white", bg="#434547", bd=4)

chapter_frame.grid_columnconfigure(0, weight=1)
chapter_frame.grid_rowconfigure(0, weight=1)


def chapter_input_button_commands():
    global chapter_input, chapter_input_quoted
    chapter_extensions = '.txt'
    chapter_input = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                               filetypes=[("OGG", chapter_extensions)])
    if chapter_input:
        chapter_input_entry.configure(state=NORMAL)
        chapter_input_entry.delete(0, END)
        if chapter_input.endswith(chapter_extensions):
            chapter_input_quoted = '"' + str(pathlib.Path(chapter_input)) + '"'
            chapter_input_entry.insert(0, chapter_input)
            chapter_input_entry.configure(state=DISABLED)
        else:
            messagebox.showinfo(title='Input Not Supported',
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.\n\n"
                                        + 'Unsupported file extension "'
                                        + str(pathlib.Path(chapter_input).suffix) + '"')
            del chapter_input


def update_chapter_input(*args):
    global chapter_input, chapter_input_quoted
    chapter_input_entry.configure(state=NORMAL)
    chapter_input_entry.delete(0, END)
    chapter_input = str(chapter_input_dnd.get()).replace("{", "").replace("}", "")
    chapter_extensions = '.txt'
    if chapter_input.endswith(chapter_extensions):
        chapter_input_quoted = '"' + str(pathlib.Path(chapter_input)) + '"'
        chapter_input_entry.insert(0, chapter_input)
        chapter_input_entry.configure(state=DISABLED)
    else:
        messagebox.showinfo(title='Input Not Supported',
                            message="Try Again With a Supported File Type!\n\nIf this is a "
                                    "file that should be supported, please let me know.\n\n"
                                    + 'Unsupported file extension "' + str(pathlib.Path(chapter_input).suffix) + '"')
        del chapter_input


# Buttons -------------------------------------------------------------------------------------------------------------
def chapter_drop_input(event):
    chapter_input_dnd.set(event.data)


chapter_input_dnd = StringVar()
chapter_input_dnd.trace('w', update_chapter_input)
chapter_input_button = HoverButton(chapter_frame, text='Open File', command=chapter_input_button_commands,
                                   foreground='white', background='#23272A', borderwidth='3', activebackground='grey',
                                   state=DISABLED)
chapter_input_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)
chapter_input_button.drop_target_register(DND_FILES)
chapter_input_button.dnd_bind('<<Drop>>', chapter_drop_input)

chapter_input_entry = Entry(chapter_frame, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
chapter_input_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)
chapter_input_entry.drop_target_register(DND_FILES)
chapter_input_entry.dnd_bind('<<Drop>>', chapter_drop_input)


def clear_chapter_input():  # Deletes all inputs and sets defaults for chapter box #1
    global chapter_input, chapter_input_entry, chapter_title_cmd_input
    try:
        chapter_title_cmd_input = ''
        chapter_input_entry.configure(state=NORMAL)
        chapter_input_entry.delete(0, END)
        chapter_input_entry.configure(state=DISABLED)
        del chapter_input
    except (Exception,):
        pass


delete_chapter_input_button = HoverButton(chapter_frame, text='X', command=clear_chapter_input, foreground='white',
                                          background='#23272A', borderwidth='3', activebackground='grey', width=2)
delete_chapter_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)

# ------------------------------------------------------------------------------------------------------------- Chapter


# Output --------------------------------------------------------------------------------------------------------------
output_frame = LabelFrame(mp4_root, text=' Output ')
output_frame.grid(row=4, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
output_frame.configure(fg="white", bg="#434547", bd=4)

output_frame.grid_columnconfigure(0, weight=1)
output_frame.grid_rowconfigure(0, weight=1)


def output_button_commands():
    global output, output_quoted
    output_window = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir=autofilesave_dir_path,
                                                 title="Select a Save Location", initialfile=autosavefilename,
                                                 filetypes=[("MP4", "*.mp4")])

    if output_window:
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_quoted = '"' + str(pathlib.Path(output_window)) + '"'
        output = output_window
        output_entry.insert(0, output)
        output_entry.configure(state=DISABLED)


output_button = HoverButton(output_frame, text='Output', command=output_button_commands, foreground='white',
                            background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
output_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)
output_entry = Entry(output_frame, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
output_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)


def clear_output():  # Deletes all inputs and sets defaults for output frame
    global output, output_entry
    try:
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.configure(state=DISABLED)
        del output
        messagebox.showinfo(title='Information', message='You must select an output for the program to continue')
    except (Exception,):
        pass


delete_output_button = HoverButton(output_frame, text='X', command=clear_output, foreground='white',
                                   background='#23272A', borderwidth='3', activebackground='grey', width=2)
delete_output_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)


# -------------------------------------------------------------------------------------------------------------- Output


# Start Job -----------------------------------------------------------------------------------------------------------
# Command -------------------------------------------------------------------------------------------------------------
def start_job():
    global output_quoted
    total_progress_segments = 2  # Progress segments starts at 2 because video+output has to be defined in order for
    # the program to work, they equal 2 progress segments

    def error_msg_box():  # Generic error box that shows the error via the 'error_name' variable
        messagebox.showerror(title='Error!', message='Please input or clear the ' + error_name + ' input box')

    if 'output' not in globals():  # If the variable 'output' doesn't exist in globals
        output_error = 1  # Set output error to 1 (error)
        messagebox.showinfo(title='Information', message='You must select an output for the program to continue')
    if 'output' in globals():  # If the variable exist in globals
        output_error = 0  # Set output error to 0 (no error)

    try:  # Video is differently checked because it HAS to exist for the program to work, the other
        # variables audio, subs, etc. check for globals to see if they exist at all
        if detect_video_fps != '':  # If video fps equals anything other than '' (empty string/nothing)
            fps_input = ':fps=' + detect_video_fps  # Set fps_input to string + detect_video_fps

        # Build video_options for the final command line with all the variables
        video_options = ' -add "' + VideoInput + '#1' + video_title_cmd_input + \
                        ':lang=' + iso_639_2_codes_dictionary[video_language.get()] + fps_input + \
                        dolby_profiles[dolby_v_profile.get()] + ':ID=1"'
        video_errors = 0  # Set's video_errors to 0 as long as all variables are found correctly
    except (Exception,):
        video_errors = 1  # Set's errors to 1 if the above try block cannot execute
        error_name = 'video'  # Provides generic error name for the above error box
        error_msg_box()  # Runs the error_msg_box function with the error name above

    try:
        if 'audio_input' in globals():  # If the variable 'audio_input' does exist in globals
            total_progress_segments += 1  # Add +1 to total_progress_segments, for final summed count of segments
            # Build audio_options for the final command line with all the variables
            audio_options = ' -add "' + audio_input + acodec_stream_choices[acodec_stream.get()] + \
                            audio_title_cmd_input + ':delay=' + audio_delay.get() + ':lang=' + \
                            iso_639_2_codes_dictionary[audio_language.get()] + ':ID=2"'
        elif 'audio_input' not in globals():  # If the variable 'audio_input' doesn't exist in globals
            audio_options = ''  # Set's audio_options to '' (nothing/empty string)
        audio_one_errors = 0  # Set output error to 0 (no error)
    except (Exception,):
        audio_one_errors = 1  # Set's errors to 1 if the above try block cannot execute
        error_name = 'audio #1'  # Provides generic error name for the above error box
        error_msg_box()  # Runs the error_msg_box function with the error name above

    try:
        if 'subtitle_input' in globals():   # If the variable 'subtitle_input' does exist in globals
            total_progress_segments += 1  # Add +1 to total_progress_segments, for final summed count of segments
            # Build subtitle_options for the final command line with all the variables
            subtitle_options = ' -add "' + subtitle_input + '#1' + subtitle_title_cmd_input + ':lang=' + \
                               iso_639_2_codes_dictionary[subtitle_language.get()] + ':ID=3"'
        elif 'subtitle_input' not in globals():
            subtitle_options = ''  # Set's subtitle_options to '' (nothing/empty string)
        subtitle_errors = 0  # Set output error to 0 (no error)
    except (Exception,):
        subtitle_errors = 1  # Set's errors to 1 if the above try block cannot execute
        error_name = 'subtitle'  # Provides generic error name for the above error box
        error_msg_box()  # Runs the error_msg_box function with the error name above

    try:
        if 'chapter_input' in globals():  # If the variable 'chapter_input' does exist in globals
            # Build subtitle_options for the final command line with all the variables
            chapter_options = ' -add "' + chapter_input + fps_input + '"'
        elif 'chapter_input' not in globals():  # If the variable 'chapter_input' doesn't exist in globals
            chapter_options = ''  # Set's chapter_options to '' (nothing/empty string)
        chapter_errors = 0  # Set output error to 0 (no error)
    except (Exception,):
        chapter_errors = 1  # Set's errors to 1 if the above try block cannot execute
        error_name = 'chapter'  # Provides generic error name for the above error box
        error_msg_box()  # Runs the error_msg_box function with the error name above

    # Combine all above errors, if exists and adds them to a sum (which should be 0), places them into var total_errors
    total_errors = video_errors + audio_one_errors + subtitle_errors + chapter_errors + output_error

    if shell_options.get() == "Default" and total_errors == 0:  # Run block if shell_options = Default and errors = 0
        def close_encode():  # Block of code to close muxing window progress and terminate all sub-processes
            if step_label.cget('text') == 'Job Completed':  # If muxing windows label says 'Job Completed'
                window.destroy()  # Close muxing window only
            else:  # If muxing windows label says anything other than 'Job Completed'
                confirm_exit = messagebox.askyesno(title='Prompt',  # Prompt message box
                                                   message="Are you sure you want to stop the mux?", parent=window)
                if confirm_exit:  # If user selects yes on the message box
                    try:  # Use subprocess.popen/cmd.exe to send a kill order to the job via job.pid
                        subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T", creationflags=subprocess.CREATE_NO_WINDOW)
                        window.destroy()  # Once the job is destroyed close muxing window
                    except (Exception,):
                        window.destroy()  # If job already completes or cannot be closed, still close muxing window

        def close_window():  # Function to make 'close_encode' multi-threaded, so it can be done while the program runs
            threading.Thread(target=close_encode).start()

        window = tk.Toplevel(mp4_root)  # Define muxing window
        window.title(str(pathlib.Path(VideoInput).stem))  # Set's muxing window title to VideoInput (no path no ext.)
        window.configure(background="#434547")  # Set's muxing window background color
        encode_label = Label(window, text='- ' * 20 + 'Progress' + ' -' * 20,  # Progress Label
                             font=("Times New Roman", 14), background='#434547', foreground="white")
        encode_label.grid(column=0, row=0)
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.protocol('WM_DELETE_WINDOW', close_window)
        window.geometry("600x450")
        encode_window_progress = scrolledtextwidget.ScrolledText(window, width=60, height=15, tabs=10, spacing2=3,
                                                                 spacing1=2, spacing3=3)
        encode_window_progress.grid(row=1, column=0, pady=(10, 6), padx=10, sticky=E + W)
        # Set's 0 out of 'total_progres_segments', the sum of all the progress segments from above
        step_label = Label(window, text='Step ' + str(0) + ' out of ' + str(total_progress_segments),
                           font=("Times New Roman", 12), background='#434547', foreground="white")
        step_label.grid(column=0, row=2, sticky=E, padx=(0, 10))
        updated_number = 0  # Set's a var with 0, so it can bne updated from 0 to +1 with every completed segment

        def auto_close_window_toggle():  # Function to save input from the checkbox below to config.ini
            try:
                config.set('auto_close_progress_window', 'option', auto_close_window.get())
                with open(config_file, 'w') as configfile:
                    config.write(configfile)
            except (Exception,):
                pass

        auto_close_window_checkbox = Checkbutton(window, text='Automatically Close', variable=auto_close_window,
                                                 onvalue='on', offvalue='off', command=auto_close_window_toggle,
                                                 takefocus=False)
        auto_close_window_checkbox.grid(row=2, column=0, columnspan=1, rowspan=1, padx=10, pady=(10, 0), sticky=W)
        auto_close_window_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                             activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        auto_close_window.set(config['auto_close_progress_window']['option'])
        app_progress_bar = ttk.Progressbar(window, style="purple.Horizontal.TProgressbar", orient=HORIZONTAL,
                                           mode='determinate')
        app_progress_bar.grid(row=3, pady=(10, 10), padx=15, sticky=E + W)

    if shell_options.get() == "Default" and total_errors == 0:
        finalcommand = '"' + mp4box + video_options + audio_options + subtitle_options + chapter_options + ' -new ' \
                       + output_quoted + '"'
        job = subprocess.Popen('cmd /c ' + finalcommand, universal_newlines=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        if config['reset_program_on_start_job']['option'] == 'on':  # If program is set to reset gui upon successful
            # start job command clear all inputs
            clear_inputs()
        for line in job.stdout:  # Code to put the muxing progress text line by line from stdout into muxing window
            encode_window_progress.configure(state=NORMAL)
            encode_window_progress.insert(END, line)
            encode_window_progress.see(END)
            encode_window_progress.configure(state=DISABLED)
            try:  # Code to break down stdout information
                strip = line.split()[-1].replace('(', '').replace(')', '').split('/')[0]
                if strip == '00':  # Each time the code 'strip' says '00' add 1 to var update_number
                    updated_number = updated_number + 1
                    if updated_number == total_progress_segments:  # For final step change label to below
                        step_label.configure(text='Muxing imports to .Mp4')
                    else:  # If updated number does not equal total_progress_setgments update step by 1 each time
                        step_label.configure(text='Step ' + str(updated_number) + ' out of '
                                                  + str(total_progress_segments))
                app_progress_bar['value'] = int(strip)  # Code to update the progress bar percentage
            except (Exception,):
                pass
        encode_window_progress.configure(state=NORMAL)
        encode_window_progress.insert(END, 'Job Completed!!')  # Once job is done insert into scroll box
        encode_window_progress.see(END)
        encode_window_progress.configure(state=DISABLED)
        step_label.configure(text='Job Completed')  # Update label to say 'Job Completed' (needed for above code)
        if config['auto_close_progress_window']['option'] == 'on':
            window.destroy()  # If program is set to auto close muxing window when complete, close the window
    if shell_options.get() == "Debug" and total_errors == 0:  # Command to muxing process in cmd.exe window
        finalcommand = '"' + mp4box + video_options + audio_options + subtitle_options + chapter_options + ' -new ' \
                       + output_quoted + '"'
        subprocess.Popen('cmd /k ' + finalcommand)
        if config['reset_program_on_start_job']['option'] == 'on':
            clear_inputs()  # Clear gui after success job start in "Debug Mode"


# ------------------------------------------------------------------------------------------------------------- Command

# Check to see if output file already exists and asks the user if they want to over-write it --------------------------
def check_for_existing_output():
    if pathlib.Path(output).is_file():  # Checks if 'output' variable/file already exists
        overwrite_output = messagebox.askyesno(title='Overwrite?',  # If exists would you like to over-write?
                                               message=f'Would you like to overwrite {str(output)}?')
        if overwrite_output:  # If "yes"
            threading.Thread(target=start_job).start()  # Run the start job command
        if not overwrite_output:  # If "no"
            output_button_commands()  # Open Output button function to set a new output file location
    else:  # If output doesn't exist go on and run the start job code
        threading.Thread(target=start_job).start()
# -------------------------- Check to see if output file already exists and asks the user if they want to over-write it


# Start Button Code ---------------------------------------------------------------------------------------------------
start_button = HoverButton(mp4_root, text='Start Job', command=check_for_existing_output, foreground='white',
                           background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
start_button.grid(row=5, column=2, columnspan=1, padx=(10, 20), pady=(15, 2), sticky=E)
# --------------------------------------------------------------------------------------------------- Start Button Code

# ----------------------------------------------------------------------------------------------------------- Start Job


# Show Command --------------------------------------------------------------------------------------------------------

def view_command():  # This function is to show the full command line output into a window, the code is the same as
    # the command code above with a few minor changes
    global cmd_line_window, encode_window_progress, output, output_quoted
    if detect_video_fps != '':
        fps_input = ':fps=' + detect_video_fps

    video_options = ' -add "' + VideoInput + '#1' + video_title_cmd_input + \
                    ':lang=' + iso_639_2_codes_dictionary[video_language.get()] + fps_input + \
                    dolby_profiles[dolby_v_profile.get()] + ':ID=1"'

    if 'audio_input' in globals():
        audio_options = ' -add "' + audio_input + acodec_stream_choices[acodec_stream.get()] + \
                        audio_title_cmd_input + ':delay=' + audio_delay.get() + ':lang=' + \
                        iso_639_2_codes_dictionary[audio_language.get()] + ':ID=2"'
    elif 'audio_input' not in globals():
        audio_options = ''

    if 'subtitle_input' in globals():
        subtitle_options = ' -add "' + subtitle_input + '#1' + subtitle_title_cmd_input + ':lang=' + \
                           iso_639_2_codes_dictionary[subtitle_language.get()] + ':ID=3"'
    elif 'subtitle_input' not in globals():
        subtitle_options = ''

    if 'chapter_input' in globals():
        chapter_options = ' -add "' + chapter_input + fps_input + '"'
    elif 'chapter_input' not in globals():
        chapter_options = ''

    finalcommand = mp4box + video_options + audio_options + subtitle_options + chapter_options + ' -new ' + \
                   output_quoted
    try:  # Attempt to update already opened window, this prevents spawning a new command window if it already exsists
        encode_window_progress.configure(state=NORMAL)
        encode_window_progress.delete(1.0, END)
        encode_window_progress.insert(END, finalcommand)
        encode_window_progress.configure(state=DISABLED)
        cmd_line_window.deiconify()
    except (AttributeError, NameError):  # If no window exists then spawn a new window with all the commands
        cmd_line_window = Toplevel()
        cmd_line_window.title('Command Line')
        cmd_line_window.configure(background="#434547")
        encode_window_progress = scrolledtextwidget.ScrolledText(cmd_line_window, width=60, height=15, tabs=10,
                                                                 spacing2=3, spacing1=2, spacing3=3)
        encode_window_progress.grid(row=0, column=0, pady=(10, 6), padx=10, sticky=E + W)
        encode_window_progress.insert(END, finalcommand)
        encode_window_progress.configure(state=DISABLED)

        def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
            pyperclip.copy(encode_window_progress.get(1.0, END))

        copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                foreground='white', background='#23272A', borderwidth='3', activebackground='grey')
        copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 10), pady=(15, 2), sticky=W + E)

        def hide_instead():  # This hides the command window instead of fully destroying it/it's variables, it allows
            # us to update the window instead of openeing a new one each time
            cmd_line_window.withdraw()

        cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)


show_command = HoverButton(mp4_root, text='View Command', command=view_command, foreground='white',
                           background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
show_command.grid(row=5, column=0, columnspan=1, padx=(20, 10), pady=(15, 2), sticky=W)

# -------------------------------------------------------------------------------------------------------- Show Command


# Status Label at bottom of main GUI ----------------------------------------------------------------- The status
# label just updates based on the mouse cursor location, when you go over certain buttons it'll give you information
# based on that location
status_label = Label(mp4_root, text='Select "Open File" or drag and drop a video file to begin',
                     bd=4, relief=SUNKEN, anchor=E, background='#717171', foreground="white")
status_label.grid(column=0, row=6, columnspan=4, sticky=W + E, pady=(0, 2), padx=3)


def input_button_on_enter(e):
    status_label.configure(text='Video inputs supported (.avi, .mp4, .m1v/.m2v, .m4v, .264, .h264, .hevc, or .h265)')


def input_button_on_leave(e):
    status_label.configure(text='')


input_button.bind("<Enter>", input_button_on_enter)
input_button.bind("<Leave>", input_button_on_leave)


def audio_input_on_enter(e):
    status_label.configure(text='Audio inputs supported (.ac3, .aac, .mp4, .m4a, .mp2, .mp3, .opus, or .ogg)')


def audio_input_on_leave(e):
    status_label.configure(text='')


audio_input_button.bind("<Enter>", audio_input_on_enter)
audio_input_button.bind("<Leave>", audio_input_on_leave)


def subtitle_input_on_enter(e):
    status_label.configure(text='Subtitle inputs supported (.srt, .idx, .ttxt)')


def subtitle_input_on_leave(e):
    status_label.configure(text='')


subtitle_input_button.bind("<Enter>", subtitle_input_on_enter)
subtitle_input_button.bind("<Leave>", subtitle_input_on_leave)


def chapter_input_on_enter(e):
    status_label.configure(text='Chapter input supported OGG (.txt)')


def chapter_input_on_leave(e):
    status_label.configure(text='')


chapter_input_button.bind("<Enter>", chapter_input_on_enter)
chapter_input_button.bind("<Leave>", chapter_input_on_leave)


def file_output_on_enter(e):
    status_label.configure(text='Select File Save Location (*.mp4)')


def file_output_on_leave(e):
    status_label.configure(text='')


output_button.bind("<Enter>", file_output_on_enter)
output_button.bind("<Leave>", file_output_on_leave)


def reset_on_enter(e):
    status_label.configure(text='Remove input and settings')


def reset_on_leave(e):
    status_label.configure(text='')


output_button.bind("<Enter>", file_output_on_enter)
output_button.bind("<Leave>", file_output_on_leave)
delete_chapter_input_button.bind("<Enter>", reset_on_enter)
delete_chapter_input_button.bind("<Leave>", reset_on_leave)
delete_output_button.bind("<Enter>", reset_on_enter)
delete_output_button.bind("<Leave>", reset_on_leave)
delete_audio_input_button.bind("<Enter>", reset_on_enter)
delete_audio_input_button.bind("<Leave>", reset_on_leave)
delete_input_button.bind("<Enter>", reset_on_enter)
delete_input_button.bind("<Leave>", reset_on_leave)
delete_subtitle_input_button.bind("<Enter>", reset_on_enter)
delete_subtitle_input_button.bind("<Leave>", reset_on_leave)


def view_command_button_on_enter(e):
    status_label.configure(text='Select to show complete command line')


def view_command_button_on_leave(e):
    status_label.configure(text='')


show_command.bind("<Enter>", view_command_button_on_enter)
show_command.bind("<Leave>", view_command_button_on_leave)


def start_job_button_on_enter(e):
    status_label.configure(text='Select to begin muxing')


def start_job_button_on_leave(e):
    status_label.configure(text='')


start_button.bind("<Enter>", start_job_button_on_enter)
start_button.bind("<Leave>", start_job_button_on_leave)

# ----------------------------------------------------------------- Status Label at bottom of main GUI
# End Loop ------------------------------------------------------------------------------------------------------------
mp4_root.mainloop()
