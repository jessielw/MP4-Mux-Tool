from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow
)

from mp4muxtool.frontend.main_window.state import MainWindowState
from mp4muxtool.frontend.styles.styles import StyleFactory
from mp4muxtool.frontend.theme_utils import load_theme
from mp4muxtool.frontend.nav_panel import NavigationalPanel
from mp4muxtool.frontend.content_box.content_box import ContentBox
from mp4muxtool.frontend.status_box.status_box import StatusBox


class Mp4MuxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("Mp4MuxWindow")
        
        self.resize(600, 400)

        self.main_window_state = MainWindowState.get_instance()
        self.main_window_state.toggle_state.connect(self._toggle_state)

        theme = load_theme("themes/dark.json")
        theme_factory = StyleFactory.get_instance()
        theme_factory.update_theme(theme)
        self.setStyleSheet(theme_factory.get_global_theme())

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)    

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        nav_panel = NavigationalPanel()
        content_box = ContentBox(nav_panel)
        status_box = StatusBox()

        content_layout = QVBoxLayout()
        content_layout.addWidget(content_box, 10)
        content_layout.addWidget(status_box, 1)
        content_layout.setContentsMargins(2, 0, 0, 0)

        # TODO: alternative solution to define signals AFTER widget creation
        # content_box.setup_signals(button_box)

        main_layout.addWidget(nav_panel, stretch=1)
        main_layout.addLayout(content_layout, stretch=6)

    def _toggle_state(self, toggle: bool):
        self.setEnabled(toggle)
