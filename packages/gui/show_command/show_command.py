

class ShowCommand:

    def __init__(self):
        pass

        # Show Command --
        # def view_command():  # This function is to show the full command line output into a window, the code is the same as
        #     # the command code above with a few minor changes
        #     global cmd_line_window, encode_window_progress, output, output_quoted
        #     if detect_video_fps != '':
        #         fps_input = ':fps=' + detect_video_fps
        #
        #     video_options = ' -add "' + VideoInput + '#1' + video_title_cmd_input + \
        #                     ':lang=' + iso_639_2_codes_dictionary[self.video_language.get()] + fps_input + \
        #                     self.dolby_profiles[self.dolby_v_profile.get()] + ':ID=1"'
        #
        #     if 'audio_input' in globals():
        #         audio_options = ' -add "' + audio_input + acodec_stream_choices[acodec_stream.get()] + \
        #                         audio_title_cmd_input + ':delay=' + self.audio_delay.get() + ':lang=' + \
        #                         iso_639_2_codes_dictionary[self.audio_language.get()] + ':ID=2"'
        #     elif 'audio_input' not in globals():
        #         audio_options = ''
        #
        #     if 'subtitle_input' in globals():
        #         subtitle_options = ' -add "' + subtitle_input + '#1' + subtitle_title_cmd_input + ':lang=' + \
        #                            iso_639_2_codes_dictionary[self.subtitle_language.get()] + ':ID=3"'
        #     elif 'subtitle_input' not in globals():
        #         subtitle_options = ''
        #
        #     if 'chapter_input' in globals():
        #         chapter_options = ' -add "' + chapter_input + fps_input + '"'
        #     elif 'chapter_input' not in globals():
        #         chapter_options = ''
        #
        #     finalcommand = mp4box + video_options + audio_options + subtitle_options + chapter_options + ' -new ' + \
        #                    output_quoted
        #     try:  # Attempt to update already opened window, this prevents spawning a new command window if it already exsists
        #         encode_window_progress.configure(state=NORMAL)
        #         encode_window_progress.delete(1.0, END)
        #         encode_window_progress.insert(END, finalcommand)
        #         encode_window_progress.configure(state=DISABLED)
        #         cmd_line_window.deiconify()
        #     except (AttributeError, NameError):  # If no window exists then spawn a new window with all the commands
        #         cmd_line_window = Toplevel()
        #         cmd_line_window.title('Command Line')
        #         cmd_line_window.configure(background="#434547")
        #         encode_window_progress = scrolledtextwidget.ScrolledText(cmd_line_window, width=60, height=15,
        #                                                                  self.tabs = 10,
        #                                                                              spacing2 = 3, spacing1 = 2, spacing3 = 3)
        #         encode_window_progress.grid(row=0, column=0, pady=(10, 6), padx=10, sticky=E + W)
        #         encode_window_progress.insert(END, finalcommand)
        #         encode_window_progress.configure(state=DISABLED)
        #
        #         def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
        #             pyperclip.copy(encode_window_progress.get(1.0, END))
        #
        #         copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
        #                                 foreground='white', background='#23272A', borderwidth='3',
        #                                 activebackground='grey')
        #         copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 10), pady=(15, 2), sticky=W + E)
        #
        #         def hide_instead():  # This hides the command window instead of fully destroying it/it's variables, it allows
        #             # us to update the window instead of openeing a new one each time
        #             cmd_line_window.withdraw()
        #
        #         cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)