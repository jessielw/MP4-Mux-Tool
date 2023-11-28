from PySide6.QtCore import Signal, QObject


class MainWindowState(QObject):
    """
    Singleton class to be used throughout the program to
    toggle enabled state the main window
    """

    _instance = None
    toggle_state = Signal(bool)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MainWindowState, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MainWindowState()
        return cls._instance
