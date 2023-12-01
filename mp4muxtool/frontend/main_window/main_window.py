from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

from mp4muxtool.frontend.main_window.state import MainWindowState
from mp4muxtool.frontend.main_window.global_style_sheet import generate_style_sheet
from mp4muxtool.frontend.theme_utils import load_theme
from mp4muxtool.frontend.button_box import ButtonBox
from mp4muxtool.frontend.content_box.content_box import ContentBox
from mp4muxtool.frontend.status_box.status_box import StatusBox


class Mp4MuxWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)

        self.main_window_state = MainWindowState.get_instance()
        self.main_window_state.toggle_state.connect(self._toggle_state)

        theme = load_theme("themes/dark.json")
        self.setStyleSheet(generate_style_sheet(theme))

        button_box = ButtonBox(theme)

        content_box = ContentBox(theme, button_box)
        status_box = StatusBox(theme)

        content_layout = QVBoxLayout()
        content_layout.addWidget(content_box, 10)
        content_layout.addWidget(status_box, 1)
        content_layout.setContentsMargins(2, 0, 0, 0)

        # TODO: alternative solution to define signals AFTER widget creation
        # content_box.setup_signals(button_box)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(button_box, stretch=1)
        layout.addLayout(content_layout, stretch=6)

    def _toggle_state(self, toggle: bool):
        self.setEnabled(toggle)
