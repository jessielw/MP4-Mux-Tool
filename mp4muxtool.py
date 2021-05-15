# Imports--------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog, StringVar
import subprocess
import tkinter as tk
import pathlib
import tkinter.scrolledtext as scrolledtextwidget
from TkinterDnD2 import *
from tkinter import messagebox

# Main Gui & Windows --------------------------------------------------------
def mp4_root_exit_function():
    confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
                                                               "     Note: This will end all current tasks!",
                                       parent=mp4_root)
    if confirm_exit == False:
        pass
    elif confirm_exit == True:
        try:
            subprocess.Popen(f"TASKKILL /F /im MP4-Mux-Tool.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
            mp4_root.destroy()
        except:
            mp4_root.destroy()

mp4_root = TkinterDnD.Tk()
mp4_root.title("MP4-Mux-Tool Beta v1.0")
# mp4_root.iconphoto(True, PhotoImage(file="Runtime/Images/topbar.png"))
mp4_root.configure(background="#434547")
window_height = 640
window_width = 480
screen_width = mp4_root.winfo_screenwidth()
screen_height = mp4_root.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
mp4_root.geometry(f'{window_width}x{window_height}+{x_cordinate}+{y_cordinate}')
mp4_root.protocol('WM_DELETE_WINDOW', mp4_root_exit_function)

# root.grid_columnconfigure(0, weight=1)
# root.grid_columnconfigure(1, weight=1)
# root.grid_columnconfigure(2, weight=1)
# root.grid_columnconfigure(3, weight=1)
# root.grid_rowconfigure(0, weight=1)
# root.grid_rowconfigure(1, weight=1)
# root.grid_rowconfigure(2, weight=1)
# root.grid_rowconfigure(3, weight=1)

# Bundled Apps --------------------------------------------------------------------------------------------------------
mp4box = '"Apps/mp4box/MP4Box.exe"'

# -------------------------------------------------------------------------------------------------------- Bundled Apps

# Frames --------------------------------------------------------------------------------------------------------------
# Video Frame -------------------------------------------------------------------------------------------
video_frame = LabelFrame(mp4_root, text=' Video ')
video_frame.grid(row=0, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10,10))
video_frame.configure(fg="white", bg="#434547", bd=3)

video_frame.rowconfigure(1, weight=1)
video_frame.columnconfigure(0, weight=1)
video_frame.columnconfigure(1, weight=1)

# -------------------------------------------------------------------------------------------- Video Frame

# -------------------------------------------------------------------------------------------------------------- Frames

def input_button_commands():
    pass

# Entry Box for Video Title -----------------------------------------------------------------------------
def video_title(*args):
    global video_title_cmd_input
    if video_title_cmd.get() == (''):
        video_title_cmd_input = ('')
    else:
        cstmcmd = video_title_cmd.get()
        video_title_cmd_input = cstmcmd + ' '

video_title_cmd = StringVar()
video_title_entrybox_label = Label(video_frame, text='Video Title:', anchor=W, background='#434547',
                                   foreground='white')
video_title_entrybox_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=N + S + W + E)
video_title_entrybox = Entry(video_frame, textvariable=video_title_cmd, borderwidth=4, background='#CACACA')
video_title_entrybox.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 15), sticky=W + E)
video_title_cmd.trace('w', video_title)
video_title_cmd.set('')
# ------------------------------------------------------------------------------------- Video Title Line

# Audio Atempo Selection ----------------------------------------------------------------------------------
acodec_atempo = StringVar()
acodec_atempo_choices = {'Automatic': '',
                         '23.976': '-fps 23976',
                         '24': '-fps 24',
                         '25': '-fps 25',
                         '29.97': '-fps 2997',
                         '30': '-fps 30',
                         '50': '-fps 50',
                         '59.94': '-fps 5994',
                         '60': '-fps 60'}
acodec_atempo_menu_label = Label(video_frame, text='Frame Rate:', background="#434547", foreground="white")
acodec_atempo_menu_label.grid(row=1, column=2, columnspan=1, padx=10, pady=(0, 0), sticky=W)
acodec_atempo_menu = OptionMenu(video_frame, acodec_atempo, *acodec_atempo_choices.keys())
acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12)
acodec_atempo_menu.grid(row=2, column=2, columnspan=1, padx=10, pady=(0,10), sticky=N + S + W + E)
acodec_atempo.set('Automatic')
# acodec_atempo.set(config_profile['FFMPEG AC3 - SETTINGS']['tempo'])
acodec_atempo_menu["menu"].configure(activebackground="dim grey")
# acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
# acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
# ------------------------------------------------------------------------------------------------ Audio Atempo

def drop_input(event):
    input_dnd.set(event.data)

def update_file_input(*args):
    global VideoInput
    global track_count
    global autofilesave_dir_path
    global VideoInputQuoted
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    VideoInput = str(input_dnd.get()).replace("{", "").replace("}", "")
    # file_extension = pathlib.Path(VideoInput).suffix


# Buttons -------------------------------------------------------------------------------------------------------------
def input_button_hover(e):
    input_button["bg"] = "grey"

def input_button_hover_leave(e):
    input_button["bg"] = "#23272A"

input_dnd = StringVar()
input_dnd.trace('w', update_file_input)
input_button = tk.Button(video_frame, text='Open File', command=input_button_commands, foreground='white',
                         background='#23272A', borderwidth='3')
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
input_button.drop_target_register(DND_FILES)
input_button.dnd_bind('<<Drop>>', drop_input)
input_button.bind("<Enter>", input_button_hover)
input_button.bind("<Leave>", input_button_hover_leave)

input_entry = Entry(video_frame, width=40, borderwidth=4, background='#CACACA', state=DISABLED)
input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
input_entry.drop_target_register(DND_FILES)
input_entry.dnd_bind('<<Drop>>', drop_input)

# ------------------------------------------------------------------------------------------------------------- Buttons

# End Loop ------------------------------------------------------------------------------------------------------------
mp4_root.mainloop()
