def theme_audio_content(theme: dict):
    # TODO: make an audio content
    audio_panel_theme = theme.get("video-content")
    audio_panel = f"""  
QToolButton{{
	color: {audio_panel_theme.get("button").get("text")};
	border-radius: 5px;
}}
QToolButton#inputBtn:pressed,
QToolButton#clearBtn:pressed,
QToolButton#addNewTab:pressed {{
    background-color: {audio_panel_theme.get("button").get("background-clicked")};
}}
QToolButton:hover {{
	background-color: {audio_panel_theme.get("button").get("background-hover")};
    color: {audio_panel_theme.get("button").get("text-hover")};
}}
QLineEdit {{
    border-radius: 2px;
    border: 1px solid {audio_panel_theme.get("entry-box").get("border")};
    background-color: {audio_panel_theme.get("entry-box").get("background")};
    color: {audio_panel_theme.get("entry-box").get("text")};
}}
QLineEdit:hover {{
    border: 1px solid {audio_panel_theme.get("entry-box").get("border-hover")};
}}
QLabel {{
    color: {audio_panel_theme.get("label").get("color")};
    background-color: {audio_panel_theme.get("label").get("background")};
}}
"""
    return audio_panel
