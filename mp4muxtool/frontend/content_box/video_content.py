from PySide6.QtWidgets import QVBoxLayout, QFrame

from mp4muxtool.frontend.styles.styles import StyleFactory
from mp4muxtool.backend.video_content import VideoContentBackEnd
from mp4muxtool.frontend.content_box.form_layout import LayoutContent


class VideoContent(QFrame):
    def __init__(self):
        super().__init__()

        self.payload = None

        self.setObjectName("VideoContent")
        self.setStyleSheet(StyleFactory.get_instance().get_video_content_theme())

        layout = QVBoxLayout(self)
        video_input = LayoutContent(
            VideoContentBackEnd,
            "video",
            "VideoLayout",
            self._get_supported_extensions(),
            0
        )
        layout.addWidget(video_input)

    @staticmethod
    def _get_supported_extensions():
        return (
            ".avi",
            ".mp4",
            ".m1v",
            ".m2v",
            ".m4v",
            ".264",
            ".h264",
            ".hevc",
            ".h265",
            ".avc",
            # TODO: remove this once we're done testing
            ".mkv",
        )
