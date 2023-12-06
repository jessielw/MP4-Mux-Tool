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
    QSizePolicy,
    QSpinBox,
)
from PySide6.QtGui import QCursor, QIcon

from mp4muxtool.frontend.styles.styles import StyleFactory
from mp4muxtool.exceptions import TrackError, MissingTrackError
from mp4muxtool.frontend.custom_widgets.combo_box import CustomComboBox
from mp4muxtool.frontend.custom_widgets.dnd_factory import DNDFactory
from mp4muxtool.frontend.status_box.loading_bar import LoadingBarState
from mp4muxtool.frontend.main_window.state import MainWindowState
from mp4muxtool.frontend.utils.file_loader import ThreadedFileLoader


class LayoutContent(QFrame):
    def __init__(self, backend: object, name: str, object_name: str, extensions: list, top_margin: int, enable_delay: bool):
        super().__init__()

        self.payload = None

        self.setObjectName(object_name)
        self.original_stylesheet, self.delete_theme = StyleFactory.get_instance().get_layout_theme()
        self.setStyleSheet(self.original_stylesheet)

        self.backend = backend
        self.backend_instance = backend()
        self.name = name
        self.extensions = extensions
        
        self.delay_spinbox = None

        self.main_ui_toggle = MainWindowState.get_instance()
        self.loading_bar_toggle = LoadingBarState.get_instance()

        layout = QGridLayout(self)

        self.input_button = self._build_icon_buttons(
            DNDFactory(QToolButton), "open.svg", "inputBtn"
        )
        self.input_button.setToolTip(
            f"Click/drag and drop a file to add a {self.name} file"
        )
        self.input_button.set_extensions(self.extensions)
        self.input_button.clicked.connect(self._open_filedialog)
        self.input_button.dropped.connect(self._handle_dnd)

        self.input_entry = DNDFactory(QLineEdit)()
        self.input_entry.setToolTip(f"Drag and drop a file to add a {self.name} file")
        self.input_entry.set_extensions(self.extensions)
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

        row_1_layout = QHBoxLayout()
        row_1_layout.addWidget(self.input_button, 1)
        row_1_layout.addWidget(self.input_entry, 4)
        row_1_layout.addWidget(self.clear_button, 1)
        row_1_layout.setContentsMargins(0, top_margin, 0, 0)

        self.language_label = QLabel()
        self.language_label.setText("Language")

        self.language_combo_box = CustomComboBox(True, 10)
        self.language_combo_box.setFixedHeight(22)
        self.language_combo_box.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self._update_languages()

        language_layout = QFormLayout()
        language_layout.setContentsMargins(0, 0, 0, 0)
        language_layout.addWidget(self.language_label)
        language_layout.addWidget(self.language_combo_box)

        self.track_title_label = QLabel()
        self.track_title_label.setText("Title")

        self.track_title_entry = QLineEdit()
        self.track_title_entry.setFixedHeight(22)

        title_layout = QFormLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.addWidget(self.track_title_label)
        title_layout.addWidget(self.track_title_entry)

        row_2_layout = QHBoxLayout()
        row_2_layout.setContentsMargins(0, 10, 0, 0)
        row_2_layout.addLayout(language_layout, stretch=1)
        row_2_layout.addLayout(title_layout, stretch=1)
        
        layout.addLayout(row_1_layout, 0, 0, 1, 4)
        layout.addLayout(row_2_layout, 1, 0, 1, 4)
        
        if enable_delay:
            row_3_layout = self._build_delay_area()
            row_3_layout.setContentsMargins(0, 10, 0, 0)
            layout.addLayout(row_3_layout, 2, 0, 1, 2)     
        
        layout.setRowStretch(3, 8)           

    def _clear_input(self):
        if self.input_entry.text():
            self.clear_var += 1
            if self.clear_var == 1:
                self.clear_timer.start(2000)
                self.clear_button.setStyleSheet(self.delete_theme)
            elif self.clear_var >= 2:
                self._reset_clear()

    def _reset_clear(self):
        self.clear_timer.stop()
        self.clear_button.setStyleSheet(self.original_stylesheet)
        if self.clear_var >= 2:
            self._reset_panel()
        self.clear_var = 0

    def _reset_panel(self):
        self.language_combo_box.setCurrentIndex(0)
        self.input_entry.clear()
        self.track_title_entry.clear()
        if self.delay_spinbox:
            self.delay_spinbox.setValue(0)

    def _handle_dnd(self, event):
        self._reset_panel()
        self._get_payload(Path(event[0]))
        self.input_entry.setText(str(event[0]))

    def _open_filedialog(self):
        supported_extensions = (
            f"{self.name.title()} Files "
            f"({' '.join(['*' + ext for ext in self.extensions])})"
        )
        open_file, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption=f"Open {self.name.title()} File",
            filter=supported_extensions,
        )
        if open_file:
            self._reset_panel()
            self._get_payload(Path(open_file))
            self.input_entry.setText(str(Path(open_file)))

    def _get_payload(self, file_input: Path):
        self.loading_bar_toggle.toggle_state.emit(True)
        try:
            self.main_ui_toggle.toggle_state.emit(False)
            file_loader = ThreadedFileLoader(file_input, self.backend, self)
            file_loader.file_loaded.connect(self._receive_payload)
            file_loader.finished.connect(file_loader.deleteLater)
            file_loader.start()
        except TrackError as e:
            QMessageBox.warning(
                None,
                "Error",
                f"There was an error opening '{file_input.name}':\n\n{e}",
            )
            self._reset_panel()
            self.main_ui_toggle.toggle_state.emit(False)
        except MissingTrackError:
            QMessageBox.warning(
                None,
                "Error",
                f"Input file '{file_input.name}':\n\nDoes not have a {self.name} track",
            )
            self._reset_panel()
            self.main_ui_toggle.toggle_state.emit(False)

    def _receive_payload(self, payload):
        self.payload = payload
        self._update_ui()
        self.loading_bar_toggle.toggle_state.emit(True)
        self.main_ui_toggle.toggle_state.emit(True)
        self.loading_bar_toggle.toggle_state.emit(False)

    def _update_ui(self):
        self.track_title_entry.setText(
            self.payload.title.strip() if self.payload.title else ""
        )
        language = self.backend_instance.find_language(self.payload.language)
        self.language_combo_box.setCurrentText(language)

    def _update_languages(self):
        self.language_combo_box.addItems(self.backend_instance.get_language_list())
        
    def _build_delay_area(self):
        delay_label = QLabel("Delay")      
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(-999999, 999999)
        self.delay_spinbox.setFixedHeight(25)
        delay_reset = self._build_icon_buttons(QToolButton, "reset.svg", "resetDelay") 
        delay_reset.clicked.connect(lambda: self.delay_spinbox.setValue(0))   
        
        delay_form = QFormLayout()
        delay_form.addWidget(delay_label)
        delay_form.addWidget(self.delay_spinbox)
        
        row_3_layout = QHBoxLayout()
        row_3_layout.addLayout(delay_form)        
        row_3_layout.addWidget(delay_reset, 0, Qt.AlignmentFlag.AlignBottom)    

        return row_3_layout

    @staticmethod
    def _build_icon_buttons(widget: QWidget, icon: str, object_name: str):
        button = widget()
        button.setObjectName(object_name)
        button.setIcon(QIcon(str(Path(f"mp4muxtool/frontend/svg/{icon}"))))
        button.setIconSize(QSize(26, 26))
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        return button
