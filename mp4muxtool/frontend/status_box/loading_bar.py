from PySide6.QtWidgets import QProgressBar
from PySide6.QtCore import Signal, QObject

from mp4muxtool.frontend.styles.styles import StyleFactory


class LoadingBarState(QObject):
    """Singleton class to be used throughout the program to activate the loading bar"""

    _instance = None
    toggle_state = Signal(bool)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoadingBarState, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LoadingBarState()
        return cls._instance


class LoadingBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(StyleFactory.get_instance().get_loading_bar_theme())

        self.loading_bar_state = LoadingBarState.get_instance()
        self.loading_bar_state.toggle_state.connect(self._toggle_state)

    def _toggle_state(self, toggle: bool):
        if toggle:
            self.show()
        else:
            self.hide()
