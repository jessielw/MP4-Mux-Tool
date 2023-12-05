def theme_nav_panel(theme: dict):
    nav_panel_theme = theme.get("navigation-panel")
    navigational_panel = f"""
QFrame {{
    background-color: {nav_panel_theme.get("base")};
}}
QToolButton {{
	color: {nav_panel_theme.get("button").get("text")};
	border-radius: 0;
	text-align: center;
}}
QToolButton:hover {{
	background-color: {nav_panel_theme.get("button").get("background-hover")};
    color: #3498db;
}}
QToolButton:checked {{
    color: #3498db;
	background-color: {nav_panel_theme.get("button").get("background-toggle")};
}}
QFrame#buttonSeparator {{
    background-color: {nav_panel_theme.get("panel-separator")};
}}
QToolButton#closeButton:hover {{
    background-color: transparent;
}}
QToolButton#closeButton:pressed {{
    background-color: {nav_panel_theme.get("button").get("close-button-click")};
}}
"""
    return navigational_panel
