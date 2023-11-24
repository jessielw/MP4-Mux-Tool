from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QStackedWidget,
    QFrame,
)


class OutputContent(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: brown")
        self.setFrameShape(QFrame.Shape.NoFrame)
