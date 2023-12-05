def theme_status_box(theme: dict):
    status_box_theme = theme.get("status-bar")
    status_box = f"""
QFrame {{
    background-color: {status_box_theme.get("background")};
}}"""

    return status_box
