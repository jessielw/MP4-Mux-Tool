from tkinter import Label, E, W, N, S, LabelFrame, ttk, Frame, StringVar, DISABLED, Entry, filedialog, messagebox, NORMAL, END, Checkbutton
import pathlib
from packages.hoverbutton import HoverButton
from tkinterdnd2 import DND_FILES
from packages.iso_639_2 import iso_639_2_codes_dictionary
from configparser import ConfigParser
from packages.config_writer import config_file


class ChapterSection:

    def __init__(self, main_gui):
        self.mp4_win = main_gui.mp4_win

        self.config = ConfigParser()
        self.config.read(config_file)

        self.chapter_frame = LabelFrame(self.mp4_win, text=' Chapter ')
        self.chapter_frame.grid(row=3, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
        self.chapter_frame.configure(fg="white", bg="#434547", bd=4)

        self.chapter_frame.grid_columnconfigure(0, weight=1)
        self.chapter_frame.grid_rowconfigure(0, weight=1)

        self.chapter_input_dnd = StringVar()
        # self.chapter_input_dnd.trace('w', update_chapter_input)
        self.chapter_input_button = HoverButton(self.chapter_frame, text='Chapter', command=self.chapter_input_button_commands,
                                           foreground='white', background='#23272A', borderwidth='3',
                                           activebackground='grey',
                                           state=DISABLED)
        self.chapter_input_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 0), sticky=W + E)
        self.chapter_input_button.drop_target_register(DND_FILES)
        self.chapter_input_button.dnd_bind('<<Drop>>', self.chapter_drop_input)

        self.chapter_input_entry = Entry(self.chapter_frame, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
        self.chapter_input_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 0), sticky=W + E)
        self.chapter_input_entry.drop_target_register(DND_FILES)
        self.chapter_input_entry.dnd_bind('<<Drop>>', self.chapter_drop_input)


        self.delete_chapter_input_button = HoverButton(self.chapter_frame, text='X', command=self.clear_chapter_input,
                                                  foreground='white',
                                                  background='#23272A', borderwidth='3', activebackground='grey',
                                                  width=2)
        self.delete_chapter_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 0), sticky=E)


        self.auto_chap_import = StringVar()
        self.auto_chap_import_checkbox = Checkbutton(self.chapter_frame, text='Import chapters from video input',
                                                variable=self.auto_chap_import, onvalue='on', offvalue='off',
                                                command=self.save_chap_import_option, takefocus=False)
        self.auto_chap_import_checkbox.grid(row=1, column=0, columnspan=2, rowspan=1, padx=10, pady=(1, 1), sticky=W)
        self.auto_chap_import_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                            activeforeground="white", selectcolor="#434547", font=("Helvetica", 10))
        self.auto_chap_import.set(str(self.config['auto_chapter_import']['option']))  # Set's button status from config.ini

        # ----- Auto Chapter Import Checkbutton

    def clear_chapter_input(self):  # Deletes all inputs and sets defaults for chapter box #1
        try:
            chapter_title_cmd_input = ''
            self.chapter_input_entry.configure(state=NORMAL)
            self.chapter_input_entry.delete(0, END)
            self.chapter_input_entry.configure(state=DISABLED)
            del chapter_input
        except (Exception,):
            pass

    # Auto Chapter Import Checkbutton
    def save_chap_import_option(self):  # Function to write variable to config.ini so program remembers user setting
        self.config.set('auto_chapter_import', 'option', self.auto_chap_import.get())
        try:
            with open(config_file, 'w') as configfile:
                self.config.write(configfile)
        except(Exception,):
            pass

    def chapter_input_button_commands(self):
        global chapter_input, chapter_input_quoted
        chapter_extensions = '.txt'
        chapter_input = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetypes=[("OGG", chapter_extensions)])
        if chapter_input:
            self.chapter_input_entry.configure(state=NORMAL)
            self.chapter_input_entry.delete(0, END)
            if chapter_input.endswith(chapter_extensions):
                chapter_input_quoted = '"' + str(pathlib.Path(chapter_input)) + '"'
                self.chapter_input_entry.insert(0, chapter_input)
                self.chapter_input_entry.configure(state=DISABLED)
            else:
                messagebox.showinfo(title='Input Not Supported',
                                    message="Try Again With a Supported File Type!\n\nIf this is a "
                                            "file that should be supported, please let me know.\n\n"
                                            + 'Unsupported file extension "'
                                            + str(pathlib.Path(chapter_input).suffix) + '"')
                del chapter_input

    def update_chapter_input(self, *args):
        global chapter_input, chapter_input_quoted
        self.chapter_input_entry.configure(state=NORMAL)
        self.chapter_input_entry.delete(0, END)
        chapter_input = str(self.chapter_input_dnd.get()).replace("{", "").replace("}", "")
        chapter_extensions = '.txt'
        if chapter_input.endswith(chapter_extensions):
            chapter_input_quoted = '"' + str(pathlib.Path(chapter_input)) + '"'
            self.chapter_input_entry.insert(0, chapter_input)
            self.chapter_input_entry.configure(state=DISABLED)
        else:
            messagebox.showinfo(title='Input Not Supported',
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.\n\n"
                                        + 'Unsupported file extension "' + str(
                                    pathlib.Path(chapter_input).suffix) + '"')
            del chapter_input

    def chapter_drop_input(self, event):
        self.chapter_input_dnd.set(event.data)