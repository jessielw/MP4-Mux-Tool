from PySide6.QtWidgets import QComboBox, QCompleter
from PySide6.QtCore import QTimer

# from PySide6.QtGui import QPalette, QColor
# from mp4muxtool.frontend.theme_utils import hex_to_rgb
from mp4muxtool.frontend.styles.styles import StyleFactory


class CustomComboBox(QComboBox):
    def __init__(self, completer: bool = False, max_items: int = 10, parent=None):
        super().__init__(parent)

        self.timer = None

        (
            self.original_style,
            self.delete_color,
        ) = StyleFactory.get_instance().get_custom_combo_box_theme()
        self.setStyleSheet(self.original_style)

        self.setEditable(True)
        self.setMaxVisibleItems(max_items)
        if not completer:
            self.lineEdit().setFrame(False)
            self.lineEdit().setReadOnly(True)
        else:
            self.setInsertPolicy(QComboBox.NoInsert)
            self.completer().setCompletionMode(QCompleter.PopupCompletion)
            self.lineEdit().editingFinished.connect(self.checkEnteredText)

        # Create a custom palette for the combo box
        # combo_palette = QPalette()
        # combo_palette.setColor(QPalette.Button, QColor(*text_color))
        # combo_palette.setColor(QPalette.ButtonText, QColor(*background_color))

        # Apply the custom palette to the combo box
        # self.setPalette(combo_palette)

        # Create a custom palette for the dropdown menu
        # menu_palette = QPalette()
        # menu_palette.setColor(QPalette.Window, QColor(*text_color))
        # menu_palette.setColor(QPalette.HighlightedText, QColor(*background_color))

        # Apply the custom palette to the dropdown menu
        # self.view().setPalette(menu_palette)

    def checkEnteredText(self):
        entered_text = self.currentText()
        if entered_text not in [self.itemText(i) for i in range(self.count())]:
            self.setStyleSheet(self.delete_color)
            if self.timer:
                self.timer.stop()
            self.timer = QTimer(self)
            self.timer.timeout.connect(lambda: self.setStyleSheet(self.original_style))
            self.timer.start(1000)
            self.setCurrentIndex(0)
