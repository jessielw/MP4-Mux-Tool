def theme_layout_content(theme: dict):
    layout_panel_theme = theme.get("layout-content")
    layout = f"""    
QToolButton{{
	color: {layout_panel_theme.get("button").get("text")};
	border-radius: 5px;
}}
QToolButton#inputBtn:pressed,
QToolButton#clearBtn:pressed,
QToolButton#addNewTab:pressed,
QToolButton#resetDelay:pressed {{
    background-color: {layout_panel_theme.get("button").get("background-clicked")};
}}
QToolButton:hover {{
	background-color: {layout_panel_theme.get("button").get("background-hover")};
    color: {layout_panel_theme.get("button").get("text-hover")};
}}
QLineEdit {{
    border-radius: 2px;
    border: 1px solid {layout_panel_theme.get("entry-box").get("border")};
    background-color: {layout_panel_theme.get("entry-box").get("background")};
    color: {layout_panel_theme.get("entry-box").get("text")};
}}
QLineEdit:hover {{
    border: 1px solid {layout_panel_theme.get("entry-box").get("border-hover")};
}}
QLabel {{
    color: {layout_panel_theme.get("label").get("color")};
    background-color: {layout_panel_theme.get("label").get("background")};
}}
"""
    button_clear = f"""
QToolButton {{
    background-color: {theme.get("delete-color")};
}}    
"""

    return layout, button_clear
