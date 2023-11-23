from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QToolButton, QFrame, QSpacerItem
from PySide6.QtGui import QIcon

content_box_stylesheet = """
QFrame {
    background-color: #434547;
}
"""

class ContentBox(QFrame):
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet(content_box_stylesheet)
        
        
        # video_button = QToolButton()
        # video_button.setText("Video")
    
        # audio_button = QToolButton()
        # audio_button.setText("Audio")
        
        # # vertical_spacer = QSpacerItem()
        
        # layout = QVBoxLayout()    
        