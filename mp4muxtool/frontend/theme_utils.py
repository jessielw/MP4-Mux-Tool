import json


def load_theme(file_path):
    """Loads theme from json file to dictionary"""
    with open(file_path, "r") as theme:
        theme_data = json.load(theme)
    return theme_data


def hex_to_rgb(hex_color):
    """Hex color codes to RGB"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
