def generate_style_sheet(theme: dict):
    main_window = theme.get("main-window")
    scroll_bar = theme.get("scroll-bar")
    style_sheet = f"""
Mp4MuxWindow {{
    background-color: {main_window.get('background')};
    }}
QScrollBar:vertical {{
    border: 1px solid {scroll_bar.get("base").get("border")};
    background: {scroll_bar.get("base").get("background")};
    width: 16px;
    margin: 17px 0 17px 0;
 }}
QScrollBar::handle:vertical {{	
    background-color: {scroll_bar.get("button").get("background")};
    min-height: 30px;
    border: 1px solid {scroll_bar.get("button").get("border")};
    border-radius: 3px;
    margin: 0;
}}
QScrollBar::handle:vertical:hover{{	
    border-color: {scroll_bar.get("button").get("border-hover")};
}}
QScrollBar::handle:vertical:pressed {{	
    background-color: {scroll_bar.get("button").get("background-pressed")};
}}
QScrollBar::sub-line:vertical {{
    border-bottom: 3px solid red;
    border: 1px solid {scroll_bar.get("button").get("border")};
    background-color: {scroll_bar.get("button").get("background")};
    height: 16px;
    subcontrol-position: top;
    subcontrol-origin: margin;
    border-radius: 3px;
}}
QScrollBar::sub-line:vertical:hover {{	
    border-color: {scroll_bar.get("button").get("border-hover")};
}}
QScrollBar::sub-line:vertical:pressed {{	
    background-color: {scroll_bar.get("button").get("background-pressed")};
}}
QScrollBar::add-line:vertical {{
    border: 1px solid {scroll_bar.get("button").get("border")};
    background-color: {scroll_bar.get("button").get("background")};
    height: 16px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
    border-radius: 3px;
}}
QScrollBar::add-line:vertical:hover {{	
    border-color: {scroll_bar.get("button").get("border-hover")};
}}
QScrollBar::add-line:vertical:pressed {{	
    background-color: {scroll_bar.get("button").get("background-pressed")};
}}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
    background: none;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}
QScrollBar:horizontal {{
    border: 1px solid {scroll_bar.get("base").get("border")};
    background: {scroll_bar.get("base").get("background")};
    height: 16px;
    margin: 0 17px 0 17px;
}}
QScrollBar::handle:horizontal {{	
    background-color: {scroll_bar.get("button").get("background")};
    min-width: 30px;
    border: 1px solid {scroll_bar.get("button").get("border")};
    border-radius: 3px;
    margin: 0;
}}
QScrollBar::handle:horizontal:hover{{	
    border-color: {scroll_bar.get("button").get("border-hover")};
}}
QScrollBar::handle:horizontal:pressed {{	
    background-color: {scroll_bar.get("button").get("background-pressed")};
}}
QScrollBar::sub-line:horizontal {{
    border-right: 3px solid red;
    border: 1px solid {scroll_bar.get("button").get("border")};
    background-color: {scroll_bar.get("button").get("background")};
    width: 16px;
    subcontrol-position: left;
    subcontrol-origin: margin;
    border-radius: 3px;
}}
QScrollBar::sub-line:horizontal:hover {{	
    border-color: {scroll_bar.get("button").get("border-hover")};
}}
QScrollBar::sub-line:horizontal:pressed {{	
    background-color: {scroll_bar.get("button").get("background-pressed")};
}}
QScrollBar::add-line:horizontal {{
    border: 1px solid {scroll_bar.get("button").get("border")};
    background-color: {scroll_bar.get("button").get("background")};
    width: 16px;
    subcontrol-position: right;
    subcontrol-origin: margin;
    border-radius: 3px;
}}
QScrollBar::add-line:horizontal:hover {{	
    border-color: {scroll_bar.get("button").get("border-hover")};
}}
QScrollBar::add-line:horizontal:pressed {{	
    background-color: {scroll_bar.get("button").get("background-pressed")};
}}
QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {{
    background: none;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}
"""
    return style_sheet
