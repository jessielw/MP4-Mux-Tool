


class ProgressWindow:

    def __init__(self):
        pass

# def start_job():
#     global output_quoted
#     total_progress_segments = 2  # Progress segments starts at 2 because video+output has to be defined in order for
#
#     # the program to work, they equal 2 progress segments
#
#     def error_msg_box():  # Generic error box that shows the error via the 'error_name' variable
#         messagebox.showerror(title='Error!', message='Please input or clear the ' + error_name + ' input box')
#
#     if 'output' not in globals():  # If the variable 'output' doesn't exist in globals
#         output_error = 1  # Set output error to 1 (error)
#         messagebox.showinfo(title='Information', message='You must select an output for the program to continue')
#     if 'output' in globals():  # If the variable exist in globals
#         output_error = 0  # Set output error to 0 (no error)
#
#     try:  # Video is differently checked because it HAS to exist for the program to work, the other
#         # variables audio, subs, etc. check for globals to see if they exist at all
#         if detect_video_fps != '':  # If video fps equals anything other than '' (empty string/nothing)
#             fps_input = ':fps=' + detect_video_fps  # Set fps_input to string + detect_video_fps
#
#         # Build video_options for the final command line with all the variables
#         video_options = ' -add "' + VideoInput + '#1' + video_title_cmd_input + \
#                         ':lang=' + iso_639_2_codes_dictionary[self.video_language.get()] + fps_input + \
#                         self.dolby_profiles[self.dolby_v_profile.get()] + ':ID=1"'
#         video_errors = 0  # Set's video_errors to 0 as long as all variables are found correctly
#     except (Exception,):
#         video_errors = 1  # Set's errors to 1 if the above try block cannot execute
#         error_name = 'video'  # Provides generic error name for the above error box
#         error_msg_box()  # Runs the error_msg_box function with the error name above
#
#     try:
#         if 'audio_input' in globals():  # If the variable 'audio_input' does exist in globals
#             total_progress_segments += 1  # Add +1 to total_progress_segments, for final summed count of segments
#             # Build audio_options for the final command line with all the variables
#             audio_options = ' -add "' + audio_input + acodec_stream_choices[acodec_stream.get()] + \
#                             audio_title_cmd_input + ':delay=' + self.audio_delay.get() + ':lang=' + \
#                             iso_639_2_codes_dictionary[self.audio_language.get()] + ':ID=2"'
#         elif 'audio_input' not in globals():  # If the variable 'audio_input' doesn't exist in globals
#             audio_options = ''  # Set's audio_options to '' (nothing/empty string)
#         audio_one_errors = 0  # Set output error to 0 (no error)
#     except (Exception,):
#         audio_one_errors = 1  # Set's errors to 1 if the above try block cannot execute
#         error_name = 'audio #1'  # Provides generic error name for the above error box
#         error_msg_box()  # Runs the error_msg_box function with the error name above
#
#     try:
#         if 'subtitle_input' in globals():  # If the variable 'subtitle_input' does exist in globals
#             total_progress_segments += 1  # Add +1 to total_progress_segments, for final summed count of segments
#             # Build subtitle_options for the final command line with all the variables
#             subtitle_options = ' -add "' + subtitle_input + '#1' + subtitle_title_cmd_input + ':lang=' + \
#                                iso_639_2_codes_dictionary[self.subtitle_language.get()] + ':ID=3"'
#         elif 'subtitle_input' not in globals():
#             subtitle_options = ''  # Set's subtitle_options to '' (nothing/empty string)
#         subtitle_errors = 0  # Set output error to 0 (no error)
#     except (Exception,):
#         subtitle_errors = 1  # Set's errors to 1 if the above try block cannot execute
#         error_name = 'subtitle'  # Provides generic error name for the above error box
#         error_msg_box()  # Runs the error_msg_box function with the error name above
#
#     try:
#         if 'chapter_input' in globals():  # If the variable 'chapter_input' does exist in globals
#             # Build subtitle_options for the final command line with all the variables
#             chapter_options = ' -add "' + chapter_input + fps_input + '"'
#         elif 'chapter_input' not in globals():  # If the variable 'chapter_input' doesn't exist in globals
#             chapter_options = ''  # Set's chapter_options to '' (nothing/empty string)
#         chapter_errors = 0  # Set output error to 0 (no error)
#     except (Exception,):
#         chapter_errors = 1  # Set's errors to 1 if the above try block cannot execute
#         error_name = 'chapter'  # Provides generic error name for the above error box
#         error_msg_box()  # Runs the error_msg_box function with the error name above
#
#     # Combine all above errors, if exists and adds them to a sum (which should be 0), places them into var total_errors
#     total_errors = video_errors + audio_one_errors + subtitle_errors + chapter_errors + output_error
#
#     if self.shell_options.get() == "Default" and total_errors == 0:  # Run block if self.shell_options = Default and errors = 0
#         def close_encode():  # Block of code to close muxing window progress and terminate all sub-processes
#             if step_label.cget('text') == 'Job Completed':  # If muxing windows label says 'Job Completed'
#                 window.destroy()  # Close muxing window only
#             else:  # If muxing windows label says anything other than 'Job Completed'
#                 confirm_exit = messagebox.askyesno(title='Prompt',  # Prompt message box
#                                                    message="Are you sure you want to stop the mux?", parent=window)
#                 if confirm_exit:  # If user selects yes on the message box
#                     try:  # Use subprocess.popen/cmd.exe to send a kill order to the job via job.pid
#                         subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T",
#                                          creationflags=subprocess.CREATE_NO_WINDOW)
#                         window.destroy()  # Once the job is destroyed close muxing window
#                     except (Exception,):
#                         window.destroy()  # If job already completes or cannot be closed, still close muxing window
#
#         def close_window():  # Function to make 'close_encode' multi-threaded, so it can be done while the program runs
#             threading.Thread(target=close_encode).start()
#
#         window = tk.Toplevel(self.mp4_win)  # Define muxing window
#         window.title(
#             str(pathlib.Path(VideoInput).stem))  # Set's muxing window title to VideoInput (no path no ext.)
#         window.configure(background="#434547")  # Set's muxing window background color
#         encode_label = Label(window, text='- ' * 20 + 'Progress' + ' -' * 20,  # Progress Label
#                              font=("Times New Roman", 14), background='#434547', foreground="white")
#         encode_label.grid(column=0, row=0)
#         window.grid_columnconfigure(0, weight=1)
#         window.grid_rowconfigure(0, weight=1)
#         window.grid_rowconfigure(1, weight=1)
#         window.protocol('WM_DELETE_WINDOW', close_window)
#         window.geometry("600x450")
#         encode_window_progress = scrolledtextwidget.ScrolledText(window, width=60, height=15,
#                                                                  self.tabs = 10, spacing2 = 3,
#                                                                                             spacing1 = 2, spacing3 = 3)
#         encode_window_progress.grid(row=1, column=0, pady=(10, 6), padx=10, sticky=E + W)
#         # Set's 0 out of 'total_progres_segments', the sum of all the progress segments from above
#         step_label = Label(window, text='Step ' + str(0) + ' out of ' + str(total_progress_segments),
#                            font=("Times New Roman", 12), background='#434547', foreground="white")
#         step_label.grid(column=0, row=2, sticky=E, padx=(0, 10))
#         updated_number = 0  # Set's a var with 0, so it can bne updated from 0 to +1 with every completed segment
#
#         def auto_close_window_toggle():  # Function to save input from the checkbox below to config.ini
#             try:
#                 config.set('auto_close_progress_window', 'option', self.auto_close_window.get())
#                 with open(config_file, 'w') as configfile:
#                     config.write(configfile)
#             except (Exception,):
#                 pass
#
#         auto_close_window_checkbox = Checkbutton(window, text='Automatically Close',
#                                                  variable=self.auto_close_window,
#                                                  onvalue='on', offvalue='off', command=auto_close_window_toggle,
#                                                  takefocus=False)
#         auto_close_window_checkbox.grid(row=2, column=0, columnspan=1, rowspan=1, padx=10, pady=(10, 0), sticky=W)
#         auto_close_window_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
#                                              activeforeground="white", selectcolor="#434547",
#                                              font=("Helvetica", 12))
#         self.auto_close_window.set(config['auto_close_progress_window']['option'])
#         app_progress_bar = ttk.Progressbar(window, style="purple.Horizontal.TProgressbar", orient=HORIZONTAL,
#                                            mode='determinate')
#         app_progress_bar.grid(row=3, pady=(10, 10), padx=15, sticky=E + W)
#
#     if self.shell_options.get() == "Default" and total_errors == 0:
#         finalcommand = '"' + mp4box + video_options + audio_options + subtitle_options + chapter_options + ' -new ' \
#                        + output_quoted + '"'
#         job = subprocess.Popen('cmd /c ' + finalcommand, universal_newlines=True,
#                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
#                                creationflags=subprocess.CREATE_NO_WINDOW)
#         if config['reset_program_on_start_job']['option'] == 'on':  # If program is set to reset gui upon successful
#             # start job command clear all inputs
#             clear_inputs()
#         for line in job.stdout:  # Code to put the muxing progress text line by line from stdout into muxing window
#             encode_window_progress.configure(state=NORMAL)
#             encode_window_progress.insert(END, line)
#             encode_window_progress.see(END)
#             encode_window_progress.configure(state=DISABLED)
#             try:  # Code to break down stdout information
#                 strip = line.split()[-1].replace('(', '').replace(')', '').split('/')[0]
#                 if strip == '00':  # Each time the code 'strip' says '00' add 1 to var update_number
#                     updated_number = updated_number + 1
#                     if updated_number == total_progress_segments:  # For final step change label to below
#                         step_label.configure(text='Muxing imports to .Mp4')
#                     else:  # If updated number does not equal total_progress_setgments update step by 1 each time
#                         step_label.configure(text='Step ' + str(updated_number) + ' out of '
#                                                   + str(total_progress_segments))
#                 app_progress_bar['value'] = int(strip)  # Code to update the progress bar percentage
#             except (Exception,):
#                 pass
#         encode_window_progress.configure(state=NORMAL)
#         encode_window_progress.insert(END, 'Job Completed!!')  # Once job is done insert into scroll box
#         encode_window_progress.see(END)
#         encode_window_progress.configure(state=DISABLED)
#         step_label.configure(text='Job Completed')  # Update label to say 'Job Completed' (needed for above code)
#         if config['auto_close_progress_window']['option'] == 'on':
#             window.destroy()  # If program is set to auto close muxing window when complete, close the window
#     if self.shell_options.get() == "Debug" and total_errors == 0:  # Command to muxing process in cmd.exe window
#         finalcommand = '"' + mp4box + video_options + audio_options + subtitle_options + chapter_options + ' -new ' \
#                        + output_quoted + '"'
#         subprocess.Popen('cmd /k ' + finalcommand)
#         if config['reset_program_on_start_job']['option'] == 'on':
#             clear_inputs()  # Clear gui after success job start in "Debug Mode"
#
# # ------------------------------------------------------------------------------------------------------------- Command