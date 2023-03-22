from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import NORMAL
from typing import Type


class MainGUIFlowControl:
    """used to enable/disable the MainGUI elements to control the flow of the program"""

    def __init__(self, main_gui):
        """
        use Tk() after method to loop and control the mp4_win window
        """

        self.main_gui = main_gui
        # self.loop()

    def loop(self):
        """enable and disable MainGUI elements depending on rather or not video input is loaded"""
        print(self.main_gui.video_loaded)
        if not self.main_gui.video_loaded:
            # disable all elements other than video
            self.main_gui.audio_section_instance.audio_frame.unbind('<<Drop>>')
            pass
        else:
            # enable all other elements
            self.main_gui.audio_section_instance.audio_input_button.config(state=NORMAL)
            # bind drag and drop to audio tab
            self.main_gui.audio_section_instance.audio_frame.drop_target_register(DND_FILES)
            self.main_gui.audio_section_instance.audio_frame.dnd_bind('<<Drop>>', lambda drop_event: self.main_gui.audio_section_instance.open_audio_source(
                [x for x in self.main_gui.splitlist(drop_event.data)][0]))
            pass

        self.main_gui.mp4_win.after(50, self.loop)
