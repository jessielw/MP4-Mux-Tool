def theme_custom_combo_box(theme: dict):
    custom_combo_box_theme = theme.get("combo-box")

    base_template = """
CustomComboBox {{
    background-color: {background};
    color: {text};
    border: 1px solid {border};
    border-top-left-radius: 2px;
    border-bottom-left-radius: 2px;
}}
CustomComboBox:hover {{
    border-color: {border_hover};
}}
CustomComboBox QAbstractItemView {{
    color: {text};  
    background-color: {background};
}}
"""
    normal = base_template.format(
        background=custom_combo_box_theme.get("background"),
        text=custom_combo_box_theme.get("text"),
        border=custom_combo_box_theme.get("border"),
        border_hover=custom_combo_box_theme.get("border-hover"),
    )
    error = base_template.format(
        background=custom_combo_box_theme.get("background"),
        text=custom_combo_box_theme.get("text"),
        border=theme.get("delete-color"),
        border_hover=custom_combo_box_theme.get("border-hover"),
    )

    return normal, error
