from tkinter import *

def openaboutwindow():  # About Window Information
    about_window = Toplevel()
    about_window.title('About')
    about_window.configure(background="#434547")
    window_height = 100
    window_width = 470
    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    about_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    about_window_text = Text(about_window, background="#434547", foreground="white", relief=SUNKEN)
    about_window_text.pack()
    about_window_text.configure(state=NORMAL)
    about_window_text.insert(INSERT, "Mp4Box Muxer \n")
    about_window_text.insert(INSERT, "\n")
    about_window_text.insert(INSERT, "Development: jlw4049")
    about_window_text.insert(INSERT, "\n\n")
    about_window_text.insert(INSERT, "A GUI wrapper for Mp4Box")
    about_window_text.configure(state=DISABLED)