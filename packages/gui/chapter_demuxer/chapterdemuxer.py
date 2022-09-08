from tkinter import (
    filedialog,
    messagebox,
    LabelFrame,
    E,
    N,
    S,
    W,
    Label,
    Entry,
    DISABLED,
    NORMAL,
    END,
    Toplevel,
    SUNKEN,
    Button,
)
import subprocess, pathlib, webbrowser
from pymediainfo import MediaInfo
from configparser import ConfigParser
from tkinterdnd2 import TkinterDnD, DND_FILES
from ctypes import windll

chapter_demuxer_version = "1.1"


class HoverButton(Button):
    """simple hoverbutton class"""

    def __init__(self, btn_master, **kw):
        Button.__init__(self, master=btn_master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["background"] = self["activebackground"]

    def on_leave(self, e):
        self["background"] = self.defaultBackground


class ChapterDemux:
    """gui window for de-muxing chapters"""

    def __init__(self, master, standalone=True, background="#434547"):
        # set variable for master window
        self.master = master

        # set some variables to manipulate
        self.extension_type = None
        self.video_input = None
        self.chapter_output = None

        # if standalone use provided Tk() instance
        if standalone:
            self.chap_extract_win = self.master

        # if not standalone run as a Toplevel()
        elif not standalone:
            self.chap_extract_win = Toplevel(self.master)

        # create chapter window
        self.chap_extract_win.title(f"Chapter Demuxer {chapter_demuxer_version}")
        self.chap_extract_win.configure(background=background)
        self.window_height = 270
        self.window_width = 500
        self.screen_width = self.chap_extract_win.winfo_screenwidth()
        self.screen_height = self.chap_extract_win.winfo_screenheight()
        self.x_coordinate = int((self.screen_width / 2) - (self.window_width / 2))
        self.y_coordinate = int((self.screen_height / 2) - (self.window_height / 2))
        self.chap_extract_win.geometry(
            f"{self.window_width}x{self.window_height}+"
            f"{self.x_coordinate}+{self.y_coordinate}"
        )
        self.chap_extract_win.grab_set()  # Keeps window above mp4_win root window
        self.chap_extract_win.protocol(
            "WM_DELETE_WINDOW", self.chap_exit_function
        )  # Code to use exit function for 'X'

        # bind window for drag and drop
        self.chap_extract_win.drop_target_register(DND_FILES)
        self.chap_extract_win.dnd_bind("<<Drop>>", self.dnd_video_drop_input)

        self.chap_extract_win.rowconfigure(3, weight=1)
        self.chap_extract_win.grid_columnconfigure(2, weight=1)

        # Block of code to fix DPI awareness issues on Windows 7 or higher
        try:
            windll.shcore.SetProcessDpiAwareness(2)  # if your Windows version >= 8.1
        except (Exception,):
            windll.user32.SetProcessDPIAware()  # Windows 8.0 or less
        # Block of code to fix DPI awareness issues on Windows 7 or higher

        self.chap_extract_win.rowconfigure(0, weight=1)
        self.chap_extract_win.grid_columnconfigure(0, weight=1)

        # if window is ran in standalone mode
        if standalone:
            self.mkvextract = r'"apps\mkvextract\mkvextract.exe"'
            self.mp4box = r'"apps\mp4box\mp4box.exe"'

            # if mkvextract is missing from defined path
            if not pathlib.Path(
                str(self.mkvextract).replace('"', "")
            ).is_file():  # If mkvextract isn't detected
                messagebox.showerror(
                    title="Error!",
                    message="Program is missing mkvextract.exe, please download and "
                    "place it in the Chapter-Demuxers /apps/mkvextract",
                )
                webbrowser.open("https://www.fosshub.com/MKVToolNix.html")
                self.chap_exit_function()
                return

            # if mp4box is missing from defined path
            if not pathlib.Path(
                str(self.mp4box).replace('"', "")
            ).is_file():  # If mp4box isn't detected
                messagebox.showerror(
                    title="Error!",
                    message="Program is missing mp4box.exe, please download and place "
                    "it in the Chapters-Demuxers /apps/mp4box",
                )
                webbrowser.open(
                    "https://www.mediafire.com/file/8pymy2869rmy5x5/mp4box.zip/file"
                )
                self.chap_exit_function()
                return

        # if program is not ran in standalone mode
        if not standalone:
            self.chapter_config_file = "runtime/config.ini"
            self.chapter_config = ConfigParser()
            self.chapter_config.read(self.chapter_config_file)
            self.mp4box = self.chapter_config["mp4box_path"]["path"]
            self.mkvextract = self.chapter_config["mkvextract_path"]["path"]

        # chapter label frame
        self.chapter_extract = LabelFrame(
            self.chap_extract_win, text=" Chapter Extraction "
        )
        self.chapter_extract.grid(
            row=0, columnspan=3, sticky=E + W + N + S, padx=20, pady=(5, 0)
        )
        self.chapter_extract.configure(fg="white", bg="#434547", bd=4)

        for c_x in range(3):
            self.chapter_extract.grid_columnconfigure(c_x, weight=1)
            self.chapter_extract.grid_rowconfigure(c_x, weight=1)
        self.chapter_extract.grid_columnconfigure(1, weight=100)

        # input button
        self.chap_input_button = HoverButton(
            self.chapter_extract,
            text="Input",
            command=self.input_button_command,
            foreground="white",
            background="#23272A",
            borderwidth="3",
            activebackground="grey",
            width=15,
        )
        self.chap_input_button.grid(
            row=0, column=0, columnspan=1, padx=(10, 5), pady=5, sticky=W
        )

        self.chap_input_entry = Entry(
            self.chapter_extract,
            borderwidth=4,
            background="#CACACA",
            state=DISABLED,
            width=30,
        )
        self.chap_input_entry.grid(
            row=0, column=1, columnspan=2, padx=(5, 10), pady=5, sticky=W + E
        )

        # output button
        self.chap_output_button = HoverButton(
            self.chapter_extract,
            text="Output",
            command=self.output_button_command,
            foreground="white",
            background="#23272A",
            borderwidth="3",
            activebackground="grey",
            width=15,
            state=DISABLED,
        )
        self.chap_output_button.grid(
            row=1, column=0, columnspan=1, padx=(10, 5), pady=(40, 5), sticky=W
        )
        self.chap_output_entry = Entry(
            self.chapter_extract,
            borderwidth=4,
            background="#CACACA",
            state=DISABLED,
            width=30,
        )
        self.chap_output_entry.grid(
            row=1, column=1, columnspan=2, padx=(5, 10), pady=(40, 5), sticky=W + E
        )

        # extract button
        self.extract_button = HoverButton(
            self.chap_extract_win,
            text="Extract",
            command=self.start_job,
            foreground="white",
            background="#23272A",
            borderwidth="3",
            activebackground="grey",
            width=15,
            state=DISABLED,
        )
        self.extract_button.grid(
            row=2, column=0, columnspan=3, padx=(20, 20), pady=(20, 5), sticky=W + E
        )

        # status label
        self.status_label = Label(
            self.chap_extract_win,
            text='Select "Input" or drag and drop a MKV or MP4 file to begin...',
            bd=4,
            relief=SUNKEN,
            anchor=E,
            background="#717171",
            foreground="white",
        )
        self.status_label.grid(
            column=0, row=3, columnspan=4, sticky=W + E, pady=(0, 2), padx=5
        )

    def start_job(self):
        """use subprocess to run a command based on the source input"""

        # if input file is mp4
        if self.extension_type == ".mp4":
            finalcommand = (
                '"'
                + self.mp4box
                + " "
                + f'"{self.video_input}"'
                + " -dump-chap-ogg -out "
                + f'"{self.chapter_output}"'
                + '"'
            )

        # if input file is mkv
        elif self.extension_type == ".mkv":
            finalcommand = (
                '"'
                + self.mkvextract
                + " "
                + f'"{self.video_input}"'
                + " "
                + "chapters -s "
                + f'"{self.chapter_output}"'
                + '"'
            )

        # use subprocess to execute the command
        subprocess.run(
            "cmd /c " + finalcommand, creationflags=subprocess.CREATE_NO_WINDOW
        )

        if pathlib.Path(
            self.chapter_output
        ).is_file():  # Once job is completed, update status label to say 'Completed'
            self.status_label.configure(text="Completed!")

    def output_button_command(self):
        """method for output button"""
        output_dialogue = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialdir=pathlib.Path(self.video_input).parent,
            title="Select a Save Location",
            initialfile=pathlib.Path(self.chapter_output).name,
            filetypes=[("ogg.txt", "*.txt")],
            parent=self.chap_extract_win,
        )

        if output_dialogue:
            self.chap_output_entry.configure(state=NORMAL)
            self.chap_output_entry.delete(0, END)
            self.chapter_output = pathlib.Path(output_dialogue)
            self.chap_output_entry.insert(0, str(self.chapter_output))
            self.chap_output_entry.configure(state=DISABLED)

    def dnd_video_drop_input(self, drop_event):
        """method to get dropped input and call open source method"""

        # use tkinter splitlist method to get dropped data
        get_dropped_input = [x for x in self.master.splitlist(drop_event.data)]

        # open source method
        self.open_source_file(get_dropped_input[0])

    def input_button_command(self):
        """manual file input"""
        source_input = filedialog.askopenfilename(
            title="Select A File",
            parent=self.chap_extract_win,
            filetypes=[("Supported Formats", (".mp4", ".mkv"))],
        )
        if source_input:
            self.open_source_file(source_file=pathlib.Path(source_input))

    def open_source_file(self, source_file):
        """open source file"""

        # create media info instance and check for menu streams
        media_info = MediaInfo.parse(pathlib.Path(source_file))
        detect_chapters = media_info.general_tracks[0].count_of_menu_streams

        # if there is no chapters in input file
        if detect_chapters is None:
            messagebox.showerror(
                title="Error",
                message="Input has no chapters",
                parent=self.chap_extract_win,
            )
            return

        # if chapters are detected
        elif detect_chapters:
            source_file_input = pathlib.Path(source_file)

            if source_file_input.suffix in (".mp4", ".mkv"):
                # update extension type variable
                if source_file_input.suffix == ".mp4":
                    self.extension_type = ".mp4"
                elif source_file_input.suffix == ".mkv":
                    self.extension_type = ".mkv"

                # manipulate the input entry box
                self.chap_input_entry.configure(state=NORMAL)
                self.chap_input_entry.delete(0, END)
                self.chap_input_entry.insert(0, pathlib.Path(str(source_file)))
                self.chap_input_entry.configure(state=DISABLED)

                # remove suffix and add string to filename
                chapter_input_filename = (
                    str(source_file_input.with_suffix("")) + ".extracted_chapters"
                )

                # create new autosave file path
                autosave_file_dir = pathlib.Path(
                    str(f"{source_file_input.parents[0]}\\")
                    + str(pathlib.Path(chapter_input_filename).name)
                ).with_suffix(".txt")

                # manipulate the output entry box
                self.chap_output_entry.configure(state=NORMAL)
                self.chap_output_entry.delete(0, END)
                self.chap_output_entry.insert(0, str(autosave_file_dir))
                self.chap_output_entry.configure(state=DISABLED)

                # enable extract button
                self.extract_button.configure(state=NORMAL)
                self.chap_output_button.configure(state=NORMAL)

                # update status label
                self.status_label.configure(text="Select Extract")

                # update variables
                self.video_input = source_file_input
                self.chapter_output = autosave_file_dir

            # if input file is not mp4 or mkv
            else:
                messagebox.showinfo(
                    title="Input Not Supported",
                    parent=self.chap_extract_win,
                    message="Try again with a supported file!\n\n"
                    + 'Unsupported file extension "'
                    + str(source_file_input.suffix)
                    + '"',
                )
                self.extract_button.configure(state=DISABLED)

    def chap_exit_function(self):
        self.chap_extract_win.grab_release()  # Release hold, so mp4_win gui can take focus again
        self.chap_extract_win.destroy()  # Close chap window


if __name__ == "__main__":
    chapter_root = TkinterDnD.Tk()
    ChapterDemux(master=chapter_root)
    chapter_root.mainloop()
