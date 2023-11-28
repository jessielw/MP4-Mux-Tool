from PySide6.QtWidgets import QProgressBar
from PySide6.QtCore import Signal, QObject


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
    def __init__(self, theme: dict, parent=None):
        super().__init__(parent)

        loading_theme = theme.get("loading-bar")
        self.setStyleSheet(
            f"""QProgressBar {{
            border: 1px solid {loading_theme.get('border')};
            border-radius: 5px;
            text-align: center;
            background-color: {loading_theme.get('background')};
            color: {loading_theme.get('color')};
        }}
        QProgressBar::chunk {{
            width: 4px;
            margin: 3px;
            background-color: {loading_theme.get('chunk-color')};
        }}"""
        )

        self.loading_bar_state = LoadingBarState.get_instance()
        self.loading_bar_state.toggle_state.connect(self._toggle_state)

    def _toggle_state(self, toggle: bool):
        if toggle:
            self.show()
        else:
            self.hide()
