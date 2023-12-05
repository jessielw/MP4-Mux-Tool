from PySide6.QtWidgets import (
    QVBoxLayout,
    QFrame,
    QStackedWidget,
)

from mp4muxtool.frontend.styles.styles import StyleFactory
from mp4muxtool.frontend.nav_panel import NavigationalPanel
from mp4muxtool.frontend.content_box.video_content import VideoContent
from mp4muxtool.frontend.content_box.audio_content import AudioContentTabbed
from mp4muxtool.frontend.content_box.subtitle_content import SubtitleContent
from mp4muxtool.frontend.content_box.chapter_content import ChapterContent
from mp4muxtool.frontend.content_box.output_content import OutputContent
from mp4muxtool.frontend.content_box.settings_content import SettingsContent


class ContentBox(QFrame):
    def __init__(self, nav_panel: NavigationalPanel):
        super().__init__()

        self.setStyleSheet(StyleFactory.get_instance().get_content_box_theme())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 2)

        self.stacked_content = QStackedWidget(self)

        self.video_content = VideoContent()
        self.audio_content = AudioContentTabbed()
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
        nav_panel.video_button_clicked.connect(self.show_video_content)
        nav_panel.audio_button_clicked.connect(self.show_audio_content)
        nav_panel.chapter_button_clicked.connect(self.show_subtile_content)
        nav_panel.subtitle_button_clicked.connect(self.show_chapter_content)
        nav_panel.output_button_clicked.connect(self.show_output_content)
        nav_panel.settings_button_clicked.connect(self.show_settings_content)

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
