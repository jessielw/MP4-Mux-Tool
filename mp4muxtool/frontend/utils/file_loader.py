from pathlib import Path

from PySide6.QtCore import QThread, Signal, QObject


class ThreadedFileLoader(QThread):
    file_loaded = Signal(object)

    def __init__(self, file_path: Path, payload_object: object, parent: QObject = None):
        """
        QThreaded file loader that returns a payload object.
        The payload_object must have a method called .get_payload().
        This method should return the payload object.

        Args:
            file_path (Path): Path to file that needs to be opened/processed.
            payload_object (object): This should be a class that can return a payload.
            parent (QObject, optional): Parent of the QObject calling it. Defaults to None.
        """
        super().__init__(parent)
        self.file_path = file_path
        self.payload_object = payload_object

    def run(self):
        payload = self.payload_object(self.file_path).get_payload()
        self.file_loaded.emit(payload)
