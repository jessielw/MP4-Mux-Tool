# Imports--------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog, StringVar, ttk, messagebox
import subprocess, pathlib, webbrowser, threading
import tkinter as tk
from TkinterDnD2 import *
from ISO_639_2 import *
from configparser import ConfigParser
from Packages.about import openaboutwindow


# Main Gui & Windows --------------------------------------------------------
def mp4_root_exit_function():
    confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
                                                               "     Note: This will end all current tasks!",
                                       parent=mp4_root)
    if confirm_exit:
        try:
            subprocess.Popen(f"TASKKILL /F /im MP4-Mux-Tool.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
            mp4_root.destroy()
        except (Exception,):
            mp4_root.destroy()


mp4_root = TkinterDnD.Tk()
mp4_root.title("MP4-Mux-Tool Beta v1.0")
# mp4_root.iconphoto(True, PhotoImage(file="Runtime/Images/topbar.png"))
mp4_root.configure(background="#434547")
window_height = 764
window_width = 605
screen_width = mp4_root.winfo_screenwidth()
screen_height = mp4_root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
mp4_root.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')
mp4_root.protocol('WM_DELETE_WINDOW', mp4_root_exit_function)

# Config Parser -------------------------------------------------------------------------------------------------------
config_file = 'Runtime/config.ini'  # Creates (if it doesn't exist) and defines location of config.ini
config = ConfigParser()
config.read(config_file)
# ------------------------------------------------------------------------------------------------------- Config Parser


# Menu Items and Sub-Bars ---------------------------------------------------------------------------------------------
my_menu_bar = Menu(mp4_root, tearoff=0)
mp4_root.config(menu=my_menu_bar)

file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='File', menu=file_menu)
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
options_submenu.add_radiobutton(label='Progress Bars', variable=shell_options,
                                value="Default", command=update_shell_option)
options_submenu.add_radiobutton(label='CMD Shell (Debug)', variable=shell_options,
                                value="Debug", command=update_shell_option)
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
        except (Exception,):
            pass
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
for n in range(0):
    mp4_root.grid_rowconfigure(n, weight=1)

# --------------------------------------------------------------------------------------- mp4_root Row/Column Configure

# Bundled Apps --------------------------------------------------------------------------------------------------------
if not config.has_section('mp4box_path'):
    config.add_section('mp4box_path')
if not config.has_option('mp4box_path', 'path'):
    config.set('mp4box_path', 'path', '')

if not config.has_section('debug_option'):
    config.add_section('debug_option')
if not config.has_option('debug_option', 'option'):
    config.set('debug_option', 'option', '')

try:
    with open(config_file, 'w') as configfile:
        config.write(configfile)
except (Exception,):
    messagebox.showinfo(title='Error', message='Could Not Write to config.ini file, delete and try again')

mp4box = config['mp4box_path']['path']

if not pathlib.Path(mp4box.replace('"', '')).is_file():  # Checks config for bundled app paths path
    # mp4box -----------------------------------------------------------------------
    if pathlib.Path('Apps/mp4box/MP4Box.exe').is_file():
        messagebox.showinfo(title='Info', message='Program will use the included '
                                                  '"mp4box.exe" located in the "Apps" folder')
        mp4box = '"' + str(pathlib.Path('Apps/mp4box/MP4Box.exe')) + '"'
        try:
            config.set('mp4box_path', 'path', mp4box)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass
    elif not pathlib.Path('Apps/mp4box/MP4Box.exe').is_file():
        messagebox.showerror(title='Error!', message='Please download mp4box.exe and set path to '
                                                     'mp4box.exe in the Options menu')
        webbrowser.open('https://github.com/gpac/gpac/wiki/MP4Box')
    # mp4box ------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------- Bundled Apps
# Video Frame ---------------------------------------------------------------------------------------------------------
video_frame = LabelFrame(mp4_root, text=' Video ')
video_frame.grid(row=0, columnspan=3, sticky=E + W + N + S, padx=20, pady=(5, 0))
video_frame.configure(fg="white", bg="#434547", bd=4)

for n in range(3):
    video_frame.grid_columnconfigure(n, weight=1)
for n in range(3):
    video_frame.grid_rowconfigure(n, weight=1)


# Entry Box for Video Title -------------------------------------------------------------------------------------------
def video_title(*args):
    global video_title_cmd_input
    if video_title_cmd.get().strip() == '':
        video_title_cmd_input = ''
    else:
        video_title_cmd_input = ':name=' + video_title_cmd.get().strip()


video_title_cmd = StringVar()
video_title_entrybox_label = Label(video_frame, text='Video Title:', anchor=W, background='#434547', foreground='white')
video_title_entrybox_label.grid(row=1, column=1, columnspan=1, padx=10, pady=(0, 0), sticky=W)
video_title_entrybox = Entry(video_frame, textvariable=video_title_cmd, borderwidth=4, background='#CACACA',
                             state=DISABLED)
video_title_entrybox.grid(row=2, column=1, columnspan=3, padx=(5, 20), pady=(0, 15), sticky=W + E)
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
# video_fps_menu_label = Label(video_frame, text='Framerate (FPS):', background="#434547", foreground="white")
# video_fps_menu_label.grid(row=1, column=3, columnspan=1, padx=10, pady=(0, 0), sticky=W)
# combo_fps = ttk.Combobox(video_frame, values=list(video_fps_choices.keys()), justify="center",
#                          textvariable=video_fps, width=10)
# combo_fps.grid(row=2, column=3, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
# combo_fps['state'] = 'readonly'
# combo_fps.current(0)
#
# # --------------------------------------------------------------------------------------------------------- Video FPS

# Video Language Selection --------------------------------------------------------------------------------------------
video_language = StringVar()
video_language_menu_label = Label(video_frame, text='Language:', background="#434547", foreground="white")
video_language_menu_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=W)
video_combo_language = ttk.Combobox(video_frame, values=list(iso_639_2_codes_dictionary.keys()), justify="center",
                                    textvariable=video_language, width=15)
video_combo_language.grid(row=2, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=W + E + N + S)
video_combo_language['state'] = 'readonly'
video_combo_language.current(0)


# ------------------------------------------------------------------------------------------------------ Video Language

def input_button_commands():
    global VideoInput, autosavefilename, autofilesave_dir_path, VideoInputQuoted, output
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
        else:
            messagebox.showinfo(title='Input Not Supported',
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.\n\n"
                                        + 'Unsupported file extension "' + str(pathlib.Path(VideoInput).suffix) + '"')


# ---------------------------------------------------------------------------------------------- Input Functions Button

# Drag and Drop Functions ---------------------------------------------------------------------------------------------
def video_drop_input(event):
    input_dnd.set(event.data)


def update_file_input(*args):
    global VideoInput, autofilesave_dir_path, VideoInputQuoted, output, autosavefilename
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
    else:
        messagebox.showinfo(title='Input Not Supported',
                            message="Try Again With a Supported File Type!\n\nIf this is a "
                                    "file that should be supported, please let me know.\n\n"
                                    + 'Unsupported file extension "' + str(pathlib.Path(VideoInput).suffix) + '"')


# --------------------------------------------------------------------------------------------- Drag and Drop Functions


# Buttons -------------------------------------------------------------------------------------------------------------
input_dnd = StringVar()
input_dnd.trace('w', update_file_input)
input_button = HoverButton(video_frame, text='Open File', command=input_button_commands, foreground='white',
                           background='#23272A', borderwidth='3', activebackground='grey', width=15)
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=W + E)
input_button.drop_target_register(DND_FILES)
input_button.dnd_bind('<<Drop>>', video_drop_input)

input_entry = Entry(video_frame, borderwidth=4, background='#CACACA', state=DISABLED, width=40)
input_entry.grid(row=0, column=1, columnspan=3, padx=(5, 50), pady=5, sticky=W + E)
input_entry.drop_target_register(DND_FILES)
input_entry.dnd_bind('<<Drop>>', video_drop_input)


def clear_video_input():
    global VideoInput, video_title_cmd_input, video_title_entrybox, video_combo_language, input_entry
    try:
        video_title_cmd_input = ''
        video_title_entrybox.configure(state=NORMAL)
        video_title_entrybox.delete(0, END)
        video_title_entrybox.configure(state=DISABLED)
        video_combo_language.current(0)
        input_entry.configure(state=NORMAL)
        input_entry.delete(0, END)
        input_entry.configure(state=DISABLED)
        VideoInput = ''
    except (Exception,):
        pass


delete_input_button = HoverButton(video_frame, text='X', command=clear_video_input, foreground='white',
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
tabs.grid(row=1, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)
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
        audio_title_cmd_input = ''
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


def audio_input_button_commands():
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
        else:
            messagebox.showinfo(title='Input Not Supported',
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.\n\n"
                                        + 'Unsupported file extension "' + str(pathlib.Path(audio_input).suffix) + '"')


def update_audio_input(*args):
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
    else:
        messagebox.showinfo(title='Input Not Supported',
                            message="Try Again With a Supported File Type!\n\nIf this is a "
                                    "file that should be supported, please let me know.\n\n"
                                    + 'Unsupported file extension "' + str(pathlib.Path(audio_input).suffix) + '"')


# Buttons -------------------------------------------------------------------------------------------------------------
def audio_drop_input(event):
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
        audio_input = ''
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
tabs.grid(row=1, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)
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
        subtitle_title_cmd_input = ''
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
        subtitle_input = ''
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
        chapter_input = ''
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
    output = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir=autofilesave_dir_path,
                                          title="Select a Save Location", initialfile=autosavefilename,
                                          filetypes=[("MP4", "*.mp4")])
    if output:
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        if output:
            output_quoted = '"' + str(pathlib.Path(output)) + '"'
            output_entry.insert(0, output)
            output_entry.configure(state=DISABLED)


output_button = HoverButton(output_frame, text='Output', command=output_button_commands, foreground='white',
                            background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
output_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)
output_entry = Entry(output_frame, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
output_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)


def clear_output():  # Deletes all inputs and sets defaults for chapter box #1
    global output, output_entry
    try:
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.configure(state=DISABLED)
        output = ''
    except (Exception,):
        pass


delete_output_button = HoverButton(output_frame, text='X', command=clear_output, foreground='white',
                                   background='#23272A', borderwidth='3', activebackground='grey', width=2)
delete_output_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)

# -------------------------------------------------------------------------------------------------------------- Output


# Show Command --------------------------------------------------------------------------------------------------------
show_command = HoverButton(mp4_root, text='View Command', command=NONE, foreground='white',
                           background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
show_command.grid(row=5, column=0, columnspan=1, padx=(20, 10), pady=(10, 5), sticky=W)
# -------------------------------------------------------------------------------------------------------- Show Command

# Start Job -----------------------------------------------------------------------------------------------------------
# Command -------------------------------------------------------------------------------------------------------------
def start_job():
    output_quoted = '"' + output + '"'

    video_options = ' -add "' + VideoInput + '#video' + video_title_cmd_input + \
                    ':lang=' + iso_639_2_codes_dictionary[video_language.get()] + '"'

    if audio_input:
        audio_options = ' -add "' + audio_input + '#audio' + audio_title_cmd_input + ':delay=' + \
                        audio_delay.get() + ':lang=' + iso_639_2_codes_dictionary[audio_language.get()] + '" '
    if not audio_input:
        audio_options = ''

    if subtitle_input:
        subtitle_options = ' -add "' + subtitle_input + subtitle_title_cmd_input + ':lang=' + \
                           iso_639_2_codes_dictionary[subtitle_language.get()] + '" '
    if not subtitle_input:
        subtitle_options = ''

    if chapter_input:
        chapter_options = ' -add "' + chapter_input + '" '
    if not chapter_input:
        chapter_options = ''

    if shell_options.get() == "Default":
        # try:
        #     mediainfo_file_size = MediaInfo.parse(VideoInputQuoted.replace('"', ''))
        #     for track in mediainfo_file_size.tracks:
        #         if track.track_type == "General":
        #             total_file_size = track.file_size
        #     total_duration = str(int(total_file_size) / 1000).rsplit('.', 1)[0]  # Compressed code for progress bars
        # except (Exception,):
        #     pass

        def close_encode():
            confirm_exit = messagebox.askyesno(title='Prompt',
                                               message="Are you sure you want to stop the parser?", parent=window)
            if confirm_exit:
                try:
                    subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T", creationflags=subprocess.CREATE_NO_WINDOW)
                    window.destroy()
                except (Exception,):
                    window.destroy()

        def close_window():
            threading.Thread(target=close_encode).start()

        window = tk.Toplevel(mp4_root)
        window.title(str(pathlib.Path(VideoInput).stem))
        window.configure(background="#434547")
        encode_label = Label(window, text='- ' * 20 + 'Progress' + ' -' * 20,
                             font=("Times New Roman", 14), background='#434547', foreground="white")
        encode_label.grid(column=0, row=0)
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.protocol('WM_DELETE_WINDOW', close_window)
        window.geometry("600x140")
        encode_window_progress = Text(window, height=2, relief=SUNKEN, bd=3)
        encode_window_progress.grid(row=1, column=0, pady=(10, 6), padx=10, sticky=E + W)
        encode_window_progress.insert(END, '')
        app_progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, mode='determinate')
        app_progress_bar.grid(row=2, pady=(10, 10), padx=15, sticky=E + W)
    # if shell_options.get() == "Default":
    #     finalcommand = '"' + ffmpeg + ' -analyzeduration 100M -probesize 50M -i ' + VideoInputQuoted \
    #                    + ' -map 0:v:0 -c:v:0 copy -vbsf hevc_mp4toannexb ' \
    #                      '-f hevc - -hide_banner -loglevel warning -stats|' \
    #                    + dolbyvision_tool + ' ' + dobly_vision_mode_choices[dobly_vision_mode.get()] \
    #                    + dolbyvision_crop.get() + ' extract-rpu - -o ' + str(VideoOutputQuoted) + '"'
    elif shell_options.get() == "Debug":
        finalcommand = '"' + mp4box + video_options + audio_options + subtitle_options + chapter_options + '-new ' \
                       + output_quoted + '"'
        print(finalcommand)
    # if shell_options.get() == "Default":
    #     job = subprocess.Popen('cmd /c ' + finalcommand, universal_newlines=True,
    #                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
    #                            creationflags=subprocess.CREATE_NO_WINDOW)
        # for line in job.stdout:
        #     try:
        #         encode_window_progress.delete('1.0', END)
        #         encode_window_progress.insert(END, 'Starting Job...')
        #         if line.split('=', 1)[0] == 'frame':
        #             encode_window_progress.delete('1.0', END)
        #             encode_window_progress.insert(END, line)
        #             size = line.split('size=', 1)[1].split()[0].rsplit('k', 1)[0]
        #             percent = '{:.1%}'.format(int(size) / int(total_duration)).split('.', 1)[0]
        #             app_progress_bar['value'] = percent
        #     except (Exception,):
        #         encode_window_progress.delete('1.0', END)
        #         encode_window_progress.insert(END, line)
    #     window.destroy()
    if shell_options.get() == "Debug":
        subprocess.Popen('cmd /k ' + finalcommand)


# ------------------------------------------------------------------------------------------------------------- Command






start_button = HoverButton(mp4_root, text='Start Job', command=lambda: threading.Thread(target=start_job).start(),
                           foreground='white', background='#23272A', borderwidth='3', activebackground='grey',
                           state=DISABLED)
start_button.grid(row=5, column=2, columnspan=1, padx=(10, 20), pady=(10, 5), sticky=E)
# ----------------------------------------------------------------------------------------------------------- Start Job


# Status Label at bottom of main GUI -----------------------------------------------------------------
status_label = Label(mp4_root, text='', bd=4, relief=SUNKEN, anchor=E, background='#717171', foreground="white")
status_label.grid(column=0, row=6, columnspan=4, sticky=W + E, pady=(0, 2), padx=3)
# ----------------------------------------------------------------- Status Label at bottom of main GUI

# End Loop ------------------------------------------------------------------------------------------------------------
mp4_root.mainloop()
