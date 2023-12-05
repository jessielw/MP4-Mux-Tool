def theme_video_content(theme: dict):
    video_panel_theme = theme.get("video-content")
    video_panel = f"""
#VideoContent {{
    background-color: {video_panel_theme.get("base")};
}}
QFrame#VideoLayout {{
    background-color: {video_panel_theme.get("base")};
}}
QToolButton {{
	color: {video_panel_theme.get("button").get("text")};
	border-radius: 5px;
}}
QToolButton#inputBtn:clicked,
QToolButton#clearBtn:clicked {{
    background-color: {video_panel_theme.get("button").get("background-clicked")};
}}
QToolButton:hover {{
	background-color: {video_panel_theme.get("button").get("background-hover")};
    color: {video_panel_theme.get("button").get("text-hover")};
}}
QLineEdit {{
    border-radius: 2px;
    border: 1px solid {video_panel_theme.get("entry-box").get("border")};
    background-color: {video_panel_theme.get("entry-box").get("background")};
    color: {video_panel_theme.get("entry-box").get("text")};
}}
QLineEdit:hover {{
    border: 1px solid {video_panel_theme.get("entry-box").get("border-hover")};
}}
QLabel {{
    color: {video_panel_theme.get("label").get("color")};
    background-color: {video_panel_theme.get("label").get("background")};
}}
"""
    return video_panel
