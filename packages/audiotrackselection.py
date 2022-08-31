import pathlib
import re
from tkinter import Toplevel, LabelFrame, messagebox, OptionMenu, StringVar, N, S, W, E

from pymediainfo import MediaInfo

from packages.hoverbutton import HoverButton


class AudioTrackSelection:
    """used to get the track ID and return it for mp4box"""

    def __init__(self, mp4_root, audio_input):
        """determine how many audio tracks are in opened file"""

        # main window
        self.mp4_win = mp4_root

        # audio input
        self.audio_input = pathlib.Path(audio_input)

        # track id
        self.track_id = None

        # use media info to parse input file
        self.media_info = MediaInfo.parse(self.audio_input)

        # get audio track count
        self.track_count = self.media_info.general_tracks[0].count_of_audio_streams

        # do different things depending on total audio track count
        if not self.track_count or self.track_count == "0":
            self.track_id = None
        elif self.track_count and self.track_count == "1":
            self.track_id = int(self.media_info.audio_tracks[0].track_id)
        elif self.track_count and self.track_count >= "2":
            self.__multi_audio_track()

    def __multi_audio_track(self):
        """window that will open above main window for the user to select which audio track they want from input"""
        audio_track_win = Toplevel()
        audio_track_win.configure(background="#191a1a")
        audio_track_win.geometry(
            f'{500}x{180}+{str(int(self.mp4_win.geometry().split("+")[1]) + 148)}+'
            f'{str(int(self.mp4_win.geometry().split("+")[2]) + 230)}'
        )
        audio_track_win.resizable(False, False)
        audio_track_win.overrideredirect(True)
        audio_track_win.grab_set()
        self.mp4_win.attributes("-alpha", 0.92)
        audio_track_win.grid_rowconfigure(0, weight=1)
        audio_track_win.grid_columnconfigure(0, weight=1)

        # track frame
        track_frame = LabelFrame(
            audio_track_win, text=" Track Selection ", fg="white", bg="#636669", bd=3
        )
        track_frame.grid(
            row=0, column=0, columnspan=5, sticky=E + W, padx=6, pady=(8, 0)
        )
        track_frame.rowconfigure(0, weight=1)
        track_frame.grid_columnconfigure(0, weight=1)

        # generate audio track information
        audio_stream_info_output = self.__loop_audio_tracks()

        # if __loop_audio_tracks returned None show error
        if not audio_stream_info_output:
            messagebox.showerror(
                parent=self.mp4_win, title="Error", message="Could not detect track ID"
            )
            return

        # Code uses the above dictionary to create a drop-down menu of audio tracks to display/select included track --
        audio_id = StringVar()
        audio_id.set(list(audio_stream_info_output)[0])
        audio_id_menu = OptionMenu(
            track_frame, audio_id, *audio_stream_info_output.keys()
        )
        audio_id_menu.config(
            background="#23272A",
            foreground="white",
            highlightthickness=1,
            width=48,
            anchor="w",
        )
        audio_id_menu.grid(
            row=0, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E
        )
        audio_id_menu["menu"].configure(activebackground="dim grey")

        def confirm_selection(audio_dict, audio_stream):
            """get selected track ID to send to mp4box, restore transparency and close track window"""
            self.track_id = int(audio_dict[audio_stream.get()])
            self.mp4_win.attributes("-alpha", 1.0)
            audio_track_win.destroy()

        select_track = HoverButton(
            track_frame,
            text="Choose Track",
            foreground="white",
            command=lambda: confirm_selection(audio_stream_info_output, audio_id),
            background="#23272A",
            borderwidth="3",
            activebackground="grey",
        )
        select_track.grid(
            row=1, column=0, columnspan=1, padx=5, pady=(60, 5), sticky=N + S + E + W
        )

        audio_track_win.wait_window()

    def __loop_audio_tracks(self):
        """generate a dictionary for multi-track input to be displayed in the track selection menu"""
        result = []

        # loop through all audio tracks and append the needed information to the results list
        for track in self.media_info.audio_tracks:

            # get format string of tracks (aac, ac3 etc...)
            if track.format:
                audio_format = "|  " + str(track.format) + "  |"
            else:
                audio_format = ""

            # get audio channels of input tracks
            if track.channel_s:
                audio_channels = "|  " + "Channels: " + str(track.channel_s) + "  |"
            else:
                audio_channels = ""

            # get audio bitrate of input tracks
            if track.other_bit_rate:
                audio_bitrate = (
                    "|  "
                    + str(track.other_bit_rate)
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                    + "  |"
                )
            else:
                audio_bitrate = ""

            # get audio language of input tracks
            if track.other_language:
                self.audio_language = "|  " + str(track.other_language[0]) + "  |"
            else:
                self.audio_language = ""

            # get audio title of input tracks
            if track.title:

                # if title > 50 characters
                if len(str(track.title)) > 50:
                    audio_title = "|  Title: " + str(track.title)[:50] + "...  |"

                # if title is < 50 characters
                else:
                    audio_title = "|  Title: " + str(track.title) + "  |"
            else:
                audio_title = ""

            # get audio sampling rate of input tracks
            if track.other_sampling_rate:
                audio_sampling_rate = (
                    "|  "
                    + str(track.other_sampling_rate)
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                    + "  |"
                )
            else:
                audio_sampling_rate = ""

            # get audio duration of input tracks
            if track.other_duration:
                audio_duration = "|  " + str(track.other_duration[0]) + "  |"
            else:
                audio_duration = ""

            # get audio delay of input tracks
            if track.delay:
                if str(track.delay) == "0":
                    audio_delay = ""
                else:
                    audio_delay = "|  Delay: " + str(track.delay) + "  |"
            else:
                audio_delay = ""

            # get track ID of audio input (this is needed for mp4box input)
            if track.track_id:
                audio_track_id = (
                    "|  ID: " + str(track.track_id) + "  |"
                )  # Code for viewing in drop down
            else:
                return None

            # combine output of all the information into a single string
            audio_track_info = (
                audio_format
                + audio_channels
                + audio_bitrate
                + audio_sampling_rate
                + audio_delay
                + audio_duration
                + self.audio_language
                + audio_title
                + audio_track_id
            )

            # add parsed string to result list
            for audio_info in [audio_track_info]:
                result.append(audio_info)

        # create a dictionary and loop results
        audio_stream_info_output = {}
        for i in range(int(self.track_count)):
            # use regex to extract track ID only
            id_num = re.search(r"ID:\s(\d+)\s", str(result[i])).group(1)

            # update dictionary with all the information
            audio_stream_info_output.update({f"Track #{i + 1}:   {result[i]}": id_num})

        # return dictionary for option menu
        return audio_stream_info_output

    def get(self):
        return self.track_id
