from pathlib import Path
from typing import Union

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import (
    QVBoxLayout,
    QToolButton,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QApplication,
)
from PySide6.QtGui import QCursor, QIcon

from mp4muxtool.frontend.styles.styles import StyleFactory


class NavigationalPanel(QFrame):
    video_button_clicked = Signal()
    audio_button_clicked = Signal()
    subtitle_button_clicked = Signal()
    chapter_button_clicked = Signal()
    output_button_clicked = Signal()
    settings_button_clicked = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("navigationalPanel")
        self.setStyleSheet(StyleFactory.get_instance().get_nav_theme())

        self.video_button = self._build_nav_button("Video", "video.svg")
        self.audio_button = self._build_nav_button("Audio", "audio.svg")
        self.subtitle_button = self._build_nav_button("Subtitle", "subtitle.svg")
        self.chapter_button = self._build_nav_button("Chapter", "chapter.svg")
        self.output_button = self._build_nav_button("Output", "output.svg")
        self.settings_button = self._build_nav_button("Settings", "settings.svg")
        self.close_button = self._build_nav_button("Close", "close.svg", False)
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(QApplication.instance().quit)

        self._toggle_buttons = [
            self.video_button,
            self.audio_button,
            self.subtitle_button,
            self.chapter_button,
            self.output_button,
            self.settings_button,
        ]

        for button in self._toggle_buttons:
            button.clicked.connect(self._handle_button_clicked)

        vertical_spacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        button_separator = QFrame()
        button_separator.setObjectName("buttonSeparator")
        button_separator.setFrameShape(QFrame.Shape.NoFrame)
        button_separator.setFrameShadow(QFrame.Plain)
        button_separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button_separator.setFixedHeight(2)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.video_button)
        layout.addWidget(self.audio_button)
        layout.addWidget(self.subtitle_button)
        layout.addWidget(self.chapter_button)
        layout.addWidget(self.output_button)
        layout.addItem(vertical_spacer)
        layout.addWidget(button_separator)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.close_button)

        self.video_button.setChecked(True)

    def _handle_button_clicked(self):
        sender = self.sender()
        for button in self._toggle_buttons:
            if button is not sender:
                button.setChecked(False)

        if sender == self.video_button:
            self.video_button_clicked.emit()
        elif sender == self.audio_button:
            self.audio_button_clicked.emit()
        elif sender == self.subtitle_button:
            self.subtitle_button_clicked.emit()
        elif sender == self.chapter_button:
            self.chapter_button_clicked.emit()
        elif sender == self.output_button:
            self.output_button_clicked.emit()
        elif sender == self.settings_button:
            self.settings_button_clicked.emit()

    @staticmethod
    def _build_nav_button(
        name: Union[str, None] = None,
        icon: Union[str, None] = None,
        enable_toggle: bool = True,
    ):
        nav_btn = QToolButton()
        if name and icon:
            nav_btn.setText(name)
            nav_btn.setIcon(QIcon(str(Path(f"mp4muxtool/frontend/svg/{icon}"))))
            nav_btn.setIconSize(QSize(26, 26))
            nav_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        nav_btn.setMinimumSize(0, 50)
        nav_btn.setMaximumSize(16777215, 16777215)
        nav_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        nav_btn.setCursor(QCursor(Qt.PointingHandCursor))
        nav_btn.setCheckable(enable_toggle)
        return nav_btn