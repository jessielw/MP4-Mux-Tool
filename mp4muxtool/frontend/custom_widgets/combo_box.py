from PySide6.QtWidgets import QComboBox
from PySide6.QtGui import QPalette, QColor

from mp4muxtool.frontend.theme_utils import hex_to_rgb


class CustomComboBox(QComboBox):
    def __init__(self, theme: dict, parent=None):
        super().__init__(parent)

        text_color = hex_to_rgb(theme.get("combo-box").get("text"))
        background_color = hex_to_rgb(theme.get("combo-box").get("background"))

        self.setStyleSheet(
            f"""
            QComboBox QAbstractItemView {{
                color: {theme.get("combo-box").get("background")};  
            }}
        """
        )

        # Create a custom palette for the combo box
        combo_palette = QPalette()
        combo_palette.setColor(QPalette.Button, QColor(*text_color))
        combo_palette.setColor(QPalette.ButtonText, QColor(*background_color))

        # Apply the custom palette to the combo box
        self.setPalette(combo_palette)

        # Create a custom palette for the dropdown menu
        menu_palette = QPalette()
        menu_palette.setColor(QPalette.Window, QColor(*text_color))
        menu_palette.setColor(QPalette.HighlightedText, QColor(*background_color))

        # Apply the custom palette to the dropdown menu
        self.view().setPalette(menu_palette)
