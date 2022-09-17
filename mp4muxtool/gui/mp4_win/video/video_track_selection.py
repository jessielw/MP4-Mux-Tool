from __future__ import annotations

import pathlib
import re
from os import PathLike
from tkinter import (
    Toplevel,
    LabelFrame,
    messagebox,
    OptionMenu,
    StringVar,
    N,
    S,
    W,
    E,
    Tk,
)

from pymediainfo import MediaInfo

from mp4muxtool.misc.iso_639_2 import *
from mp4muxtool.theme.hoverbutton import HoverButton


class VideoTrackSelection:
    """use to get track information for use within the program"""

    def __init__(self, mp4_root: Tk | Toplevel, video_input: str | PathLike):
        """
        Determine how many video tracks are in opened file.

        :param mp4_root: Object ID of parent window
        :param video_input: String or PathLike path to video file
        """

        # mp4_win window
        self.mp4_win = mp4_root

        # video input
        self.video_input = pathlib.Path(video_input)

        # track id
        self.track_id = None

        # use media info to parse input file
        self.media_info = MediaInfo.parse(self.video_input)

        # get video track count
        self.track_count = self.media_info.general_tracks[0].count_of_video_streams

        # do different things depending on total video track count
        if not self.track_count or self.track_count == "0":
            self.track_id = None
        elif self.track_count and self.track_count == "1":
            if self.media_info.video_tracks[0].track_id:
                self.track_id = self.media_info.video_tracks[0].track_id
            else:
                self.track_id = "0"
        elif self.track_count and self.track_count >= "2":
            self._multi_video_track()

    def _multi_video_track(self):
        """window that will open above mp4_win window for the user to select which video track they want from input"""
        video_track_win = Toplevel()
        video_track_win.configure(background="#191a1a")
        video_track_win.geometry(
            f'{500}x{180}+{str(int(self.mp4_win.geometry().split("+")[1]) + 148)}+'
            f'{str(int(self.mp4_win.geometry().split("+")[2]) + 230)}'
        )
        video_track_win.resizable(False, False)
        video_track_win.overrideredirect(True)
        video_track_win.grab_set()
        self.mp4_win.attributes("-alpha", 0.92)
        video_track_win.grid_rowconfigure(0, weight=1)
        video_track_win.grid_columnconfigure(0, weight=1)

        # track frame
        track_frame = LabelFrame(
            video_track_win, text=" Track Selection ", fg="white", bg="#636669", bd=3
        )
        track_frame.grid(
            row=0, column=0, columnspan=5, sticky=E + W, padx=6, pady=(8, 0)
        )
        track_frame.rowconfigure(0, weight=1)
        track_frame.grid_columnconfigure(0, weight=1)

        # generate video track information
        video_stream_info_output = self._loop_video_tracks()

        # if _loop_video_tracks returned None show error
        if not video_stream_info_output:
            messagebox.showerror(
                parent=self.mp4_win, title="Error", message="Could not detect track ID"
            )
            return

        # Code uses the above dictionary to create a drop-down menu of video tracks to display/select included track
        video_id = StringVar()
        video_id.set(list(video_stream_info_output)[0])
        video_id_menu = OptionMenu(
            track_frame, video_id, *video_stream_info_output.keys()
        )
        video_id_menu.config(
            background="#23272A",
            foreground="white",
            highlightthickness=1,
            width=48,
            anchor="w",
        )
        video_id_menu.grid(
            row=0, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E
        )
        video_id_menu["menu"].configure(activebackground="dim grey")

        def confirm_selection(video_dict, video_stream):
            """get selected track ID to send to mp4box, restore transparency and close track window"""
            self.track_id = int(video_dict[video_stream.get()])
            self.mp4_win.attributes("-alpha", 1.0)
            video_track_win.destroy()

        select_track = HoverButton(
            track_frame,
            text="Choose Track",
            foreground="white",
            command=lambda: confirm_selection(video_stream_info_output, video_id),
            background="#23272A",
            borderwidth="3",
            activebackground="grey",
        )
        select_track.grid(
            row=1, column=0, columnspan=1, padx=5, pady=(60, 5), sticky=N + S + E + W
        )

        # wait for the window to be closed before continuing
        video_track_win.wait_window()

    def _loop_video_tracks(self):
        """generate a dictionary for multi-track input to be displayed in the track selection menu"""
        result = []

        # loop through all video tracks and append the needed information to the results list
        for track in self.media_info.video_tracks:

            # get format string of tracks (aac, ac3 etc...)
            if track.format:
                video_format = "|  " + str(track.format) + "  |"
            else:
                video_format = ""

            # get video channels of input tracks
            if track.channel_s:
                video_channels = "|  " + "Channels: " + str(track.channel_s) + "  |"
            else:
                video_channels = ""

            # get video bitrate of input tracks
            if track.other_bit_rate:
                video_bitrate = (
                    "|  "
                    + str(track.other_bit_rate)
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                    + "  |"
                )
            else:
                video_bitrate = ""

            # get video language of input tracks
            if track.other_language:
                video_language = "|  " + str(track.other_language[0]) + "  |"
            else:
                video_language = ""

            # get video title of input tracks
            if track.title:

                # if title > 50 characters
                if len(str(track.title)) > 50:
                    video_title = "|  Title: " + str(track.title)[:50] + "...  |"

                # if title is < 50 characters
                else:
                    video_title = "|  Title: " + str(track.title) + "  |"
            else:
                video_title = ""

            # get video sampling rate of input tracks
            if track.other_sampling_rate:
                video_sampling_rate = (
                    "|  "
                    + str(track.other_sampling_rate)
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                    + "  |"
                )
            else:
                video_sampling_rate = ""

            # get video duration of input tracks
            if track.other_duration:
                video_duration = "|  " + str(track.other_duration[0]) + "  |"
            else:
                video_duration = ""

            # get video delay of input tracks
            delay = self._video_delay(track.track_id)
            if delay:
                if str(delay) == "0":
                    video_delay = ""
                else:
                    video_delay = "|  Delay: " + str(delay) + "  |"
            else:
                video_delay = ""

            # get track ID of video input (this is needed for mp4box input)
            if track.track_id:
                video_track_id = (
                    "|  ID: " + str(track.track_id) + "  |"
                )  # Code for viewing in drop down
            else:
                return None

            # combine output of all the information into a single string
            video_track_info = (
                video_format
                + video_channels
                + video_bitrate
                + video_sampling_rate
                + video_delay
                + video_duration
                + video_language
                + video_title
                + video_track_id
            )

            result.append(video_track_info)

        # create a dictionary and loop results
        video_stream_info_output = {}
        for i in range(int(self.track_count)):
            # use regex to extract track ID only
            id_num = re.search(r"ID:\s(\d+)\s", str(result[i])).group(1)

            # update dictionary with all the information
            video_stream_info_output.update({f"Track #{i + 1}:   {result[i]}": id_num})

        # return dictionary for option menu
        return video_stream_info_output

    def _detect_title(self, video_id):
        """
        Check video track for embedded track title.

        :param video_id: Track selected ID
        :return: String of detected title
        """
        detected_title = self.media_info.tracks[video_id].title
        if detected_title:
            return detected_title
        else:
            return ""

    def _video_delay(self, video_id):
        """
        find video delay from selected track and return it to be used within the program.

        :param video_id: ID of selected track to properly get the delay from that track.
        :return: Video delay in the form of a string.
        """

        detected_delay = None

        # if input file is MP4 then use source_delay of the selected video track to obtain the delay
        if pathlib.Path(self.video_input).suffix == ".mp4":
            if self.media_info.tracks[video_id].source_delay:
                detected_delay = str(self.media_info.tracks[video_id].source_delay)
            elif not self.media_info.tracks[video_id].source_delay:
                detected_delay = "0"

            # check if filename has the delay string as a back-up
            if detected_delay == "0":
                detected_delay = self._video_delay_filename()

        # if input file is MKV then use delay of the selected video track to obtain the delay
        elif pathlib.Path(self.video_input).suffix == ".mkv":
            if self.media_info.tracks[video_id].delay:
                detected_delay = str(self.media_info.tracks[video_id].delay)
            elif not self.media_info.tracks[video_id].delay:
                detected_delay = "0"

            # check if filename has the delay string as a back-up
            if detected_delay == "0":
                detected_delay = self._video_delay_filename()

        # if the file is any other supported format, search for the delay string in the filename
        else:
            detected_delay = self._video_delay_filename()

        return detected_delay

    def _video_delay_filename(self):
        find_delay = re.search(
            r"delay\s?(-?\d*)\s?ms",
            str(pathlib.Path(self.video_input).name),
            re.IGNORECASE,
        )
        if find_delay:
            return str(find_delay.group(1))
        if not find_delay:
            return "0"

    def _language_detection(self, video_id):
        """returns the ISO_638_2 language code"""
        if self.media_info.tracks[video_id].other_language:
            detect_index = [
                len(i) for i in self.media_info.tracks[video_id].other_language
            ].index(3)
            language_index = list(iso_639_2_codes_dictionary.values()).index(
                self.media_info.tracks[video_id].other_language[detect_index]
            )
            return language_index
        else:
            return 0

    def get(self):
        """returns the media info of the selected video track in dictionary format"""
        if not self.track_id:
            return None
        else:
            delay = self._video_delay(video_id=int(self.track_id))
            language = self._language_detection(video_id=int(self.track_id))
            title = self._detect_title(video_id=int(self.track_id))
            return {
                "track_data": self.media_info.tracks[int(self.track_id)].to_data(),
                "detected_delay": delay,
                "detected_language": language,
                "detected_title": title,
            }
