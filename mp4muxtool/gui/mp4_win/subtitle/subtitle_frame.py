from tkinter import Label, E, W, N, S, LabelFrame, ttk, Frame, StringVar, DISABLED, Entry, filedialog, messagebox, NORMAL, END
import pathlib
from mp4muxtool.theme.hoverbutton import HoverButton
from tkinterdnd2 import DND_FILES
from mp4muxtool.misc.iso_639_2 import iso_639_2_codes_dictionary


class SubtitleSection:

    def __init__(self, main_gui):
        self.mp4_win = main_gui.mp4_win

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


        self.subtitle_input_dnd = StringVar()
        # self.subtitle_input_dnd.trace('w', update_subtitle_input)
        self.subtitle_input_button = HoverButton(self.subtitle_tab, text='Subtitle', command=self.subtitle_input_button_commands,
                                            foreground='white', background='#23272A', borderwidth='3',
                                            activebackground='grey',
                                            state=DISABLED)
        self.subtitle_input_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)
        self.subtitle_input_button.drop_target_register(DND_FILES)
        self.subtitle_input_button.dnd_bind('<<Drop>>', self.subtitle_drop_input)

        self.subtitle_input_entry = Entry(self.subtitle_tab, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
        self.subtitle_input_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)
        self.subtitle_input_entry.drop_target_register(DND_FILES)
        self.subtitle_input_entry.dnd_bind('<<Drop>>', self.subtitle_drop_input)


        self.delete_subtitle_input_button = HoverButton(self.subtitle_tab, text='X', command=self.clear_subtitle_input,
                                                   foreground='white',
                                                   background='#23272A', borderwidth='3', activebackground='grey',
                                                   width=2)
        self.delete_subtitle_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)

    def clear_subtitle_input(self):  # Deletes all inputs and sets defaults for subtitle box #1
        try:
            subtitle_title_cmd_input = ''
            self.subtitle_input_entry.configure(state=NORMAL)
            self.subtitle_input_entry.delete(0, END)
            self.subtitle_input_entry.configure(state=DISABLED)
            self.subtitle_title_entry.configure(state=NORMAL)
            self.subtitle_title_entry.delete(0, END)
            self.subtitle_title_entry.configure(state=DISABLED)
            del subtitle_input
            self.subtitle_language.current(0)

        except (Exception,):
            pass

    def subtitle_input_button_commands(self):
        global subtitle_input, subtitle_input_quoted
        subtitle_extensions = ('.srt', '.idx', '.ttxt')
        subtitle_input = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                    filetypes=[("Supported Formats", subtitle_extensions)])
        if subtitle_input:
            self.subtitle_input_entry.configure(state=NORMAL)
            self.subtitle_input_entry.delete(0, END)
            if subtitle_input.endswith(subtitle_extensions):
                subtitle_input_quoted = '"' + str(pathlib.Path(subtitle_input)) + '"'
                self.subtitle_input_entry.insert(0, subtitle_input)
                self.subtitle_input_entry.configure(state=DISABLED)
                self.subtitle_title_entry.configure(state=NORMAL)
            else:
                messagebox.showinfo(title='Input Not Supported',
                                    message="Try Again With a Supported File Type!\n\nIf this is a "
                                            "file that should be supported, please let me know.\n\n"
                                            + 'Unsupported file extension "'
                                            + str(pathlib.Path(subtitle_input).suffix) + '"')
                self.subtitle_language.current(0)
                self.subtitle_title_entry.delete(0, END)
                del subtitle_input

    def update_subtitle_input(self, *args):
        global subtitle_input, subtitle_input_quoted
        self.subtitle_input_entry.configure(state=NORMAL)
        self.subtitle_input_entry.delete(0, END)
        subtitle_input = str(self.subtitle_input_dnd.get()).replace("{", "").replace("}", "")
        subtitle_extensions = ('.srt', '.idx', '.ttxt')
        if subtitle_input.endswith(subtitle_extensions):
            subtitle_input_quoted = '"' + str(pathlib.Path(subtitle_input)) + '"'
            self.subtitle_input_entry.insert(0, subtitle_input)
            self.subtitle_input_entry.configure(state=DISABLED)
            self.subtitle_title_entry.configure(state=NORMAL)
        else:
            messagebox.showinfo(title='Input Not Supported',
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.\n\n"
                                        + 'Unsupported file extension "' + str(
                                    pathlib.Path(subtitle_input).suffix) + '"')
            self.subtitle_language.current(0)
            self.subtitle_title_entry.delete(0, END)
            del subtitle_input

    def subtitle_drop_input(self, event):
        self.subtitle_input_dnd.set(event.data)
