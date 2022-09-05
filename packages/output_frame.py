from tkinter import Label, E, W, N, S, LabelFrame, ttk, Frame, StringVar, DISABLED, Entry, filedialog, messagebox, NORMAL, END, Checkbutton
import pathlib
from packages.hoverbutton import HoverButton
from tkinterdnd2 import DND_FILES
from packages.iso_639_2 import iso_639_2_codes_dictionary
from configparser import ConfigParser
from packages.config_writer import config_file
import threading


class OutputSection:

    def __init__(self, main_gui):
        self.mp4_win = main_gui.mp4_win


        self.output_frame = LabelFrame(self.mp4_win, text=' Output ')
        self.output_frame.grid(row=4, columnspan=4, sticky=E + W + N + S, padx=20, pady=(5, 5))
        self.output_frame.configure(fg="white", bg="#434547", bd=4)

        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)



        self.output_button = HoverButton(self.output_frame, text='Output', command=self.output_button_commands, foreground='white',
                                    background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
        self.output_button.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 5), sticky=W + E)
        self.output_entry = Entry(self.output_frame, width=39, borderwidth=4, background='#CACACA', state=DISABLED)
        self.output_entry.grid(row=0, column=1, columnspan=3, padx=(0, 50), pady=(10, 5), sticky=W + E)



        self.delete_output_button = HoverButton(self.output_frame, text='X', command=self.clear_output, foreground='white',
                                           background='#23272A', borderwidth='3', activebackground='grey', width=2)
        self.delete_output_button.grid(row=0, column=3, columnspan=1, padx=10, pady=(10, 5), sticky=E)


        #
        self.start_button = HoverButton(self.mp4_win, text='Mux', command=self.check_for_existing_output, foreground='white',
                                   background='#23272A', borderwidth='3', activebackground='grey', state=DISABLED)
        self.start_button.grid(row=5, column=2, columnspan=1, padx=(10, 20), pady=(15, 2), sticky=E)

    def output_button_commands(self):
        global output, output_quoted
        output_window = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir=self.autofilesave_dir_path,
                                                     title="Select a Save Location", initialfile=self.autosavefilename,
                                                     filetypes=[("MP4", "*.mp4")])

        if output_window:
            self.output_entry.configure(state=NORMAL)
            self.output_entry.delete(0, END)
            output_quoted = '"' + str(pathlib.Path(output_window)) + '"'
            output = output_window
            self.output_entry.insert(0, output)
            self.output_entry.configure(state=DISABLED)

    def clear_output(self):  # Deletes all inputs and sets defaults for output frame
        try:
            self.output_entry.configure(state=NORMAL)
            self.output_entry.delete(0, END)
            self.output_entry.configure(state=DISABLED)
            del output
            messagebox.showinfo(title='Information',
                                message='You must select an output for the program to continue')
        except (Exception,):
            pass

    # Check to see if output file already exists and asks the user if they want to over-write it --------------------------
    def check_for_existing_output(self):
        pass
        # if pathlib.Path(output).is_file():  # Checks if 'output' variable/file already exists
        #     overwrite_output = messagebox.askyesno(title='Overwrite?',  # If exists would you like to over-write?
        #                                            message=f'Would you like to overwrite {str(output)}?')
        #     if overwrite_output:  # If "yes"
        #         threading.Thread(target=start_job).start()  # Run the start job command
        #     if not overwrite_output:  # If "no"
        #         output_button_commands()  # Open Output button function to set a new output file location
        # else:  # If output doesn't exist go on and run the start job code
        #     threading.Thread(target=start_job).start()

    # -------------------------- Check to see if output file already exists and asks the user if they want to over-write it