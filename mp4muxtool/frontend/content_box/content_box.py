from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QToolButton,
    QFrame,
    QSpacerItem,
    QStackedWidget,
)
from PySide6.QtGui import QIcon

from mp4muxtool.frontend.button_box import ButtonBox
from mp4muxtool.frontend.content_box.video_content import VideoContent
from mp4muxtool.frontend.content_box.audio_content import AudioContent
from mp4muxtool.frontend.content_box.subtitle_content import SubtitleContent
from mp4muxtool.frontend.content_box.chapter_content import ChapterContent
from mp4muxtool.frontend.content_box.output_content import OutputContent
from mp4muxtool.frontend.content_box.settings_content import SettingsContent

content_box_stylesheet = """
QFrame {
    background-color: #434547;
}
"""


class ContentBox(QFrame):
    def __init__(self, button_box: ButtonBox):
        super().__init__()

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(content_box_stylesheet)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)

        self.stacked_content = QStackedWidget(self)

        self.video_content = VideoContent()
        self.audio_content = AudioContent()
        self.subtitle_content = SubtitleContent()
        self.chapter_content = ChapterContent()
        self.output_content = OutputContent()
        self.settings_content = SettingsContent()

        self.stacked_content.addWidget(self.video_content)
        self.stacked_content.addWidget(self.audio_content)
        self.stacked_content.addWidget(self.subtitle_content)
        self.stacked_content.addWidget(self.chapter_content)
        self.stacked_content.addWidget(self.output_content)
        self.stacked_content.addWidget(self.settings_content)

        layout.addWidget(self.stacked_content)

        # Connect signals from ButtonBox to slots in ContentBox
        button_box.video_button_clicked.connect(self.show_video_content)
        button_box.audio_button_clicked.connect(self.show_audio_content)
        button_box.chapter_button_clicked.connect(self.show_subtile_content)
        button_box.subtitle_button_clicked.connect(self.show_chapter_content)
        button_box.output_button_clicked.connect(self.show_output_content)
        button_box.settings_button_clicked.connect(self.show_settings_content)

    # TODO: alternative solution to define signals AFTER widget creation
    # def setup_signals(self, button_box):
    #     button_box.video_button_clicked.connect(self.show_video_content)
    #     button_box.audio_button_clicked.connect(self.show_audio_content)

    def show_video_content(self):
        self.stacked_content.setCurrentWidget(self.video_content)

    def show_audio_content(self):
        self.stacked_content.setCurrentWidget(self.audio_content)

    def show_subtile_content(self):
        self.stacked_content.setCurrentWidget(self.subtitle_content)

    def show_chapter_content(self):
        self.stacked_content.setCurrentWidget(self.chapter_content)

    def show_output_content(self):
        self.stacked_content.setCurrentWidget(self.output_content)
        
    def show_settings_content(self):
        self.stacked_content.setCurrentWidget(self.settings_content)        
