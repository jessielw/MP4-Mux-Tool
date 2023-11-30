from PySide6.QtWidgets import QComboBox, QCompleter
from PySide6.QtCore import QTimer

# from PySide6.QtGui import QPalette, QColor
# from mp4muxtool.frontend.theme_utils import hex_to_rgb


class CustomComboBox(QComboBox):
    def __init__(
        self, theme: dict, completer: bool = False, max_items: int = 10, parent=None
    ):
        super().__init__(parent)

        self.timer = None

        self.theme = theme
        self.combo_box_theme = self.theme.get("combo-box")
        # text_color = hex_to_rgb(combo_box_theme.get("text"))
        # background_color = hex_to_rgb(combo_box_theme.get("background"))

        self.original_style = f"""
            CustomComboBox {{
                background-color: {self.combo_box_theme.get("background")};
                color: {self.combo_box_theme.get("text")};
                border: 1px solid {self.combo_box_theme.get("border")};
                border-top-left-radius: 2px;
                border-bottom-left-radius: 2px;
            }}
            CustomComboBox:hover {{
                border-color: {self.combo_box_theme.get("border-hover")};
            }}
            CustomComboBox QAbstractItemView {{
                color: {self.combo_box_theme.get("text")};  
            }}           
        """

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
            modified_style = self.original_style.replace(
                f"border: 1px solid {self.combo_box_theme.get('border')};",
                f"border: 1px solid {self.theme.get('delete-color')};",
            )
            self.setStyleSheet(modified_style)
            if self.timer:
                self.timer.stop()
            self.timer = QTimer(self)
            self.timer.timeout.connect(lambda: self.setStyleSheet(self.original_style))
            self.timer.start(1000)
            self.setCurrentIndex(0)
