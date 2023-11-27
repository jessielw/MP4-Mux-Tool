from pathlib import Path

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QGridLayout,
    QFormLayout,
    QWidget,
    QFrame,
    QToolButton,
    QLineEdit,
    QLabel,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QCursor, QIcon

from mp4muxtool.exceptions import TrackError, VideoTrackError
from mp4muxtool.frontend.custom_widgets.combo_box import CustomComboBox
from mp4muxtool.frontend.custom_widgets.dnd_factory import DNDFactory
from mp4muxtool.backend.video_content import VideoContentBackEnd


video_panel_stylesheet = """
#VideoFrame {{
    background-color: {frame_bg_color};
}}
QToolButton {{
	color: {button_color};
	border-radius: 5px;
}}
QToolButton#inputBtn:clicked,
QToolButton#clearBtn:clicked {{
    background-color: {button_bg_clicked_color};
}}
QToolButton:hover {{
	background-color: {button_bg_hover_color};
    color: {button_text_hover_color};
}}
QLineEdit {{
    border-radius: 2px;
    border: 1px solid {entry_border_color};
    background-color: {entry_bg_color};
    color: {entry_text_color};
}}
QLineEdit:hover {{
    border: 1px solid {entry_border_hover_color};
}}
QLabel {{
    color: {label_color};
    background-color: {label_bg_color};
}}
"""


class VideoContent(QFrame):
    def __init__(self, theme: dict):
        super().__init__()

        self.payload = None

        self.setObjectName("VideoFrame")
        self.theme = self._set_theme(theme)

        layout = QGridLayout(self)

        dnd_input_button = DNDFactory(QToolButton)
        self.input_button = self._build_icon_buttons(
            dnd_input_button, "open.svg", "inputBtn"
        )
        self.input_button.setToolTip("Click/drag and drop a file to add a video file")
        self.input_button.set_extensions(self._get_supported_extensions())
        self.input_button.clicked.connect(self._open_filedialog)
        self.input_button.dropped.connect(self._handle_dnd)

        self.input_entry = DNDFactory(QLineEdit)()
        self.input_entry.setToolTip("Drag and drop a file to add a video file")
        self.input_entry.set_extensions(self._get_supported_extensions())
        self.input_entry.setFixedHeight(22)
        self.input_entry.setReadOnly(True)
        self.input_entry.dropped.connect(self._handle_dnd)

        self.clear_var = 0
        self.clear_timer = QTimer(self)
        self.clear_timer.timeout.connect(self._reset_clear)
        self.clear_button = self._build_icon_buttons(
            QToolButton, "delete.svg", "clearBtn"
        )
        self.clear_button.setToolTip("Clear input (click twice to confirm)")
        self.clear_button.clicked.connect(self._clear_input)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_button, 1)
        input_layout.addWidget(self.input_entry, 4)
        input_layout.addWidget(self.clear_button, 1)

        self.language_label = QLabel()
        self.language_label.setText("Language")

        self.language_combo_box = CustomComboBox(theme)
        self.language_combo_box.setFixedHeight(22)

        language_layout = QFormLayout()
        language_layout.setContentsMargins(0, 20, 0, 0)
        language_layout.addWidget(self.language_label)
        language_layout.addWidget(self.language_combo_box)

        self.track_title_label = QLabel()
        self.track_title_label.setText("Title")

        self.track_title_entry = QLineEdit()
        self.track_title_entry.setFixedHeight(22)

        title_layout = QFormLayout()
        title_layout.setContentsMargins(0, 20, 0, 0)
        title_layout.addWidget(self.track_title_label)
        title_layout.addWidget(self.track_title_entry)

        layout.addLayout(input_layout, 0, 0, 1, 4)
        layout.addLayout(language_layout, 1, 0, 1, 2)
        layout.addLayout(title_layout, 1, 2, 1, 2)

    def _clear_input(self):
        if self.input_entry.text():
            self.clear_var += 1
            if self.clear_var == 1:
                self.clear_timer.start(2000)
                self.clear_button.setStyleSheet(
                    f"QToolButton {{background-color: {self.theme.get('delete-color')}}};"
                )
            elif self.clear_var >= 2:
                self._reset_clear()

    def _reset_clear(self):
        self.clear_timer.stop()
        original_button_bg = (
            self.theme.get("video-content").get("button").get("background-base")
        )
        self.clear_button.setStyleSheet(
            f"QToolButton {{background-color: {original_button_bg}}}"
        )
        if self.clear_var >= 2:
            self._reset_panel()
        self.clear_var = 0

    def _reset_panel(self):
        self.language_combo_box.setCurrentIndex(0)
        self.input_entry.clear()
        self.track_title_entry.clear()

    def _handle_dnd(self, event):
        self._reset_panel()
        self._get_payload(Path(event[0]))
        self.input_entry.setText(str(event[0]))

    def _open_filedialog(self):
        supported_extensions = (
            "Video Files "
            f"({' '.join(['*' + ext for ext in self._get_supported_extensions()])})"
        )
        open_file, _ = QFileDialog.getOpenFileName(
            parent=self, caption="Open Video File", filter=supported_extensions
        )
        if open_file:
            self._reset_panel()
            self._get_payload(Path(open_file))
            self.input_entry.setText(str(Path(open_file)))

    def _get_payload(self, file_input: Path):
        try:
            self.payload = VideoContentBackEnd(file_input).get_payload()
        except TrackError as e:
            QMessageBox.warning(
                None,
                "Error",
                f"There was an error opening '{file_input.name}':\n\n{e}",
            )
            self._reset_panel()
        except VideoTrackError:
            QMessageBox.warning(
                None,
                "Error",
                f"Input file '{file_input.name}':\n\nDoes not have a video track",
            )
            self._reset_panel()

    def _build_icon_buttons(self, widget: QWidget, icon: str, object_name: str):
        button = widget()
        button.setObjectName(object_name)
        button.setIcon(QIcon(str(Path(f"mp4muxtool/frontend/svg/{icon}"))))
        button.setIconSize(QSize(26, 26))
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        return button

    def _set_theme(self, theme: dict):
        widget_theme = theme.get("video-content")
        format_style_sheet = video_panel_stylesheet.format(
            frame_bg_color=widget_theme.get("base"),
            button_color=widget_theme.get("button").get("text"),
            button_bg_clicked_color=widget_theme.get("button").get(
                "background-clicked"
            ),
            button_bg_hover_color=widget_theme.get("button").get("background-hover"),
            button_text_hover_color=widget_theme.get("button").get("text-hover"),
            entry_border_color=widget_theme.get("entry-box").get("border"),
            entry_bg_color=widget_theme.get("entry-box").get("background"),
            entry_text_color=widget_theme.get("entry-box").get("text"),
            entry_border_hover_color=widget_theme.get("entry-box").get("border-hover"),
            label_color=widget_theme.get("label").get("color"),
            label_bg_color=widget_theme.get("label").get("background"),
        )
        self.setStyleSheet(format_style_sheet)
        return theme

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
        )
