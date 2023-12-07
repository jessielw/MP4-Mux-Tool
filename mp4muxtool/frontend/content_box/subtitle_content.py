from PySide6.QtWidgets import QVBoxLayout, QWidget

from mp4muxtool.frontend.content_box.form_tabbed import ContentTabbed
from mp4muxtool.backend.video_content import VideoContentBackEnd


class SubtitleContentTabbed(QWidget):
    def __init__(self):
        super().__init__()
        object_name = "SubtitleContent"
        self.setObjectName(object_name)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # TODO: create a back end for subtitle
        self.tabbed_widget = ContentTabbed(object_name="SubtitleContentTabbed", 
                                           backend=VideoContentBackEnd, 
                                           name="subtitle", 
                                           layout_object_name=object_name + "Layout",
                                           extensions=self._get_supported_extensions(),
                                           enable_delay=False)
        
        layout.addWidget(self.tabbed_widget)
    
    # TODO: actually update the extensions for this
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
        