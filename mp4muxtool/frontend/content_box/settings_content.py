from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QStackedWidget,
    QFrame,
)


class SettingsContent(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: orange")
        self.setFrameShape(QFrame.Shape.NoFrame)
