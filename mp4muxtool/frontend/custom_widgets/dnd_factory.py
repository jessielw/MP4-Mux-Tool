from pathlib import Path
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal


def DNDFactory(base_class: QWidget):
    """Factory used to create drag and drop widgets as needed"""

    class DNDWidget(base_class):
        dropped = Signal(list)

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setAcceptDrops(True)
            self.supported_extensions = None

        def dragEnterEvent(self, event):
            drop = Path(event.mimeData().urls()[0].toLocalFile())
            if drop.is_file():
                if self.supported_extensions:
                    if drop.suffix in self.supported_extensions:
                        event.acceptProposedAction()

        def dropEvent(self, event):
            file_urls = [Path(url.toLocalFile()) for url in event.mimeData().urls()]
            self.dropped.emit(file_urls)

        def set_extensions(self, supported_extensions: list):
            self.supported_extensions = supported_extensions

    return DNDWidget
