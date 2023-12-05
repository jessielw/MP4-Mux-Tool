def theme_loading_bar(theme: dict):
    loading_bar_theme = theme.get("loading-bar")
    loading_bar = f"""
QProgressBar {{
    border: 1px solid {loading_bar_theme.get('border')};
    border-radius: 5px;
    text-align: center;
    background-color: {loading_bar_theme.get('background')};
    color: {loading_bar_theme.get('color')};
}}
QProgressBar::chunk {{
    width: 4px;
    margin: 3px;
    background-color: {loading_bar_theme.get('chunk-color')};
}}"""
    return loading_bar
