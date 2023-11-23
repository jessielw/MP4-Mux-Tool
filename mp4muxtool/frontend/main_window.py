from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QToolButton, QFrame
from PySide6.QtGui import QIcon

from mp4muxtool.frontend.custom_widgets.buttons import IconToolButton
from mp4muxtool.frontend.button_box import ButtonBox
from mp4muxtool.frontend.content_box import ContentBox

class Mp4MuxWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 450)
        
        button_box = ButtonBox()
        content_box = ContentBox()
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(button_box, stretch=1)
        layout.addWidget(content_box, stretch=6)