from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout

from mp4muxtool.frontend.status_box.loading_bar import LoadingBar


class StatusBox(QFrame):
    def __init__(self, theme: dict):
        super().__init__()

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMaximumHeight(20)

        status_box_theme = theme.get("status-bar")
        self.setStyleSheet(
            f"QFrame {{background-color: {status_box_theme.get('background')}}}"
        )

        loading_bar = LoadingBar(theme)
        loading_bar.setRange(0, 0)
        loading_bar.setFixedWidth(60)
        loading_bar.setFixedHeight(10)
        loading_bar.hide()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 1, 5, 1)
        layout.addWidget(loading_bar, 0, Qt.AlignmentFlag.AlignRight)
