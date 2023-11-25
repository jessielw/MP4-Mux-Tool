import json


def load_theme(file_path):
    """Loads theme from json file to dictionary"""
    with open(file_path, "r") as theme:
        theme_data = json.load(theme)
    return theme_data
