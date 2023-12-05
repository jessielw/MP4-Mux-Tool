def theme_main_window(theme: dict):
    main_window_theme = theme.get("main-window")
    main_window = f"""
#Mp4MuxWindow {{
    background-color: {main_window_theme.get('background')};
}}"""
    return main_window
