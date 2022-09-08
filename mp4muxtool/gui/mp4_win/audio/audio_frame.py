from tkinter import Label, E, W, N, S, LabelFrame, ttk, Frame, StringVar, DISABLED, Entry, filedialog, messagebox, NORMAL, END
import pathlib
from mp4muxtool.gui.mp4_win.audio.audio_track_selection import AudioTrackSelection
from mp4muxtool.theme.hoverbutton import HoverButton
from mp4muxtool.misc.iso_639_2 import iso_639_2_codes_dictionary


class AudioSection:
    """handles the audio section of the program"""

    def __init__(self, main_gui):
        # define window to place widgets in
        self.mp4_win = main_gui.mp4_win

        # audio frame
        self.audio_frame = LabelFrame(self.mp4_win, text=' Audio ')
        self.audio_frame.grid(row=1, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
        self.audio_frame.configure(fg="white", bg="#434547", bd=4)
        self.audio_frame.grid_columnconfigure(0, weight=1)
        self.audio_frame.grid_rowconfigure(0, weight=1)

        # audio tabs
        self.tabs = ttk.Notebook(self.audio_frame, height=110)
        self.tabs.grid(row=0, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=5)
        self.audio_tab = Frame(self.tabs, background="#434547")
        self.tabs.add(self.audio_tab, text=f" Track #1 ")
        for n in range(4):
            self.audio_tab.grid_columnconfigure(n, weight=1)
        for n in range(3):
            self.audio_tab.grid_rowconfigure(n, weight=1)

        # # bind drag and drop to audio tab
        # self.audio_frame.drop_target_register(DND_FILES)
        # self.audio_frame.dnd_bind('<<Drop>>', lambda drop_event: self.open_audio_source(
        #     [x for x in self.mp4_win.splitlist(drop_event.data)][0]))

        #
        self.audio_input_dnd = StringVar()
        self.audio_input_button = HoverButton(self.audio_tab, text='Audio', command=self.manual_open_audio_source,
                                              foreground='white', background='#23272A', borderwidth='3',
                                              activebackground='grey', state=DISABLED)
        self.audio_input_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)

        self.audio_input_entry = Entry(self.audio_tab, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
        self.audio_input_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)

        self.delete_audio_input_button = HoverButton(self.audio_tab, text='X', command=self.delete_audio_frame,
                                                     foreground='white',
                                                     background='#23272A', borderwidth='3', activebackground='grey',
                                                     width=2)
        self.delete_audio_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)

        self.audio_title = StringVar()
        self.audio_title_entry_label = Label(self.audio_tab, text='Title:', anchor=W, background='#434547',
                                             foreground='white')
        self.audio_title_entry_label.grid(row=1, column=1, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        self.audio_title_entry = Entry(self.audio_tab, textvariable=self.audio_title, borderwidth=4,
                                       background='#CACACA')
        self.audio_title_entry.grid(row=2, column=1, columnspan=1, padx=10, pady=(0, 15), sticky=W + E)

        self.audio_delay = StringVar()
        self.audio_delay_label = Label(self.audio_tab, text="Delay (ms):", background="#434547", foreground="white")
        self.audio_delay_label.grid(row=1, column=3, columnspan=1, padx=10, pady=1, sticky=W)
        self.audio_delay_entry = Entry(self.audio_tab, borderwidth=4, background='#CACACA',
                                       textvariable=self.audio_delay)
        self.audio_delay_entry.grid(row=2, column=3, columnspan=1, padx=10, pady=(0, 15), sticky=W + E)
        self.audio_delay.set("0")

        self.audio_language = StringVar()
        self.audio_language_menu_label = Label(self.audio_tab, text='Language:', background="#434547",
                                               foreground="white")
        self.audio_language_menu_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=W)
        self.audio_language = ttk.Combobox(self.audio_tab, values=list(iso_639_2_codes_dictionary.keys()),
                                           justify="center",
                                           textvariable=self.audio_language)
        self.audio_language.grid(row=2, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
        self.audio_language['state'] = 'readonly'
        self.audio_language.current(0)

    def manual_open_audio_source(self):
        """gui dialog function for audio input when the button is clicked"""
        aud_input = filedialog.askopenfilename(parent=self.mp4_win, initialdir="/", title="Select Audio File")

        if aud_input:
            self.open_audio_source(aud_input)

    def open_audio_source(self, audio_input):
        """ """
        supported_audio_extensions = ('.ac3', '.aac', '.mp4', '.m4a', '.mp2', '.mp3', '.opus', '.ogg', '.mkv', '.mka')
        # StreamOrder is needed to extract stream from mkv

        if not pathlib.Path(audio_input).suffix in supported_audio_extensions:
            messagebox.showerror(parent=self.mp4_win, title="Error",
                                 message=f"{str(pathlib.Path(audio_input).suffix)} is not supported")
        else:
            get_audio_info = AudioTrackSelection(self.mp4_win, audio_input)
            get_info = get_audio_info.get()

            if not get_info:
                messagebox.showerror(parent=self.mp4_win, title="Error",
                                     message=f"'{str(pathlib.Path(audio_input).name)}' does not contain any audio tracks")
                self.delete_audio_frame()
                return

            elif get_info:
                self.update_audio_frame(audio_input, get_info)

    def update_audio_frame(self, audio_input, audio_info):
        """updates the gui for the audio"""
        self.audio_delay.set(audio_info["detected_delay"])
        self.audio_title.set(audio_info["detected_title"])
        # print(audio_info["detected_language"])
        self.audio_language.current(int(audio_info["detected_language"]))
        self.audio_input_entry.configure(state=NORMAL)
        self.audio_input_entry.delete(0, END)
        self.audio_input_entry.insert(0, str(pathlib.Path(audio_input)))
        self.audio_input_entry.configure(state=DISABLED)

    def delete_audio_frame(self):
        """clear the gui for the audio"""
        self.audio_delay.set("0")
        self.audio_language.current(0)
        self.audio_title_entry.delete(0, END)
        self.audio_input_entry.configure(state=NORMAL)
        self.audio_input_entry.delete(0, END)
        self.audio_input_entry.configure(state=DISABLED)
