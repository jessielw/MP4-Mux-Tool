def theme_content_box(theme: dict):
    content_box_theme = theme.get("content-box")
    # TODO: we need to double check if this is needed
    content_box = f"""
QFrame {{
    background-color: {content_box_theme.get("background")};
}}"""

    # return content_box
