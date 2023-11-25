from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QToolButton, QFrame
from PySide6.QtGui import QIcon

from mp4muxtool.frontend.theme_loader import load_theme
from mp4muxtool.frontend.button_box import ButtonBox
from mp4muxtool.frontend.content_box.content_box import ContentBox

class Mp4MuxWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        
        theme = load_theme("themes/dark.json").get("theme")
        
        button_box = ButtonBox(theme)
        content_box = ContentBox(button_box)
        
        # TODO: alternative solution to define signals AFTER widget creation
        # content_box.setup_signals(button_box)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(button_box, stretch=1)
        layout.addWidget(content_box, stretch=6)