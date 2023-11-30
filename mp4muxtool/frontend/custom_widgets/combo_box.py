from PySide6.QtWidgets import QComboBox, QCompleter

# from PySide6.QtGui import QPalette, QColor
# from mp4muxtool.frontend.theme_utils import hex_to_rgb


class CustomComboBox(QComboBox):
    def __init__(
        self, theme: dict, completer: bool = False, max_items: int = 10, parent=None
    ):
        super().__init__(parent)

        combo_box_theme = theme.get("combo-box")
        # text_color = hex_to_rgb(combo_box_theme.get("text"))
        # background_color = hex_to_rgb(combo_box_theme.get("background"))

        self.setStyleSheet(
            f"""
            CustomComboBox {{
                background-color: {combo_box_theme.get("background")};
                color: {combo_box_theme.get("text")};
                border: 1px solid {combo_box_theme.get("border")};
                border-top-left-radius: 2px;
                border-bottom-left-radius: 2px;
            }}
            CustomComboBox:hover {{
                border-color: {combo_box_theme.get("border-hover")};
            }}
            CustomComboBox QAbstractItemView {{
                color: {combo_box_theme.get("text")};  
            }}
        """
        )
        self.setEditable(True)
        self.setMaxVisibleItems(max_items)
        if not completer:
            self.lineEdit().setFrame(False)
            self.lineEdit().setReadOnly(True)
        else:
            self.setInsertPolicy(QComboBox.NoInsert)
            self.completer().setCompletionMode(QCompleter.PopupCompletion)

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
