from mp4muxtool.frontend.styles.main_window import theme_main_window


def theme_global(theme: dict):
    # we have to add main window in global since they are applied in the same place
    main_window = theme_main_window(theme)

    scroll_bar_theme = theme.get("scroll-bar")
    scroll_bar = f"""
QScrollBar:vertical {{
    border: 1px solid {scroll_bar_theme.get("base").get("border")};
    background: {scroll_bar_theme.get("base").get("background")};
    width: 16px;
    margin: 17px 0 17px 0;
 }}
QScrollBar::handle:vertical {{	
    background-color: {scroll_bar_theme.get("button").get("background")};
    min-height: 30px;
    border: 1px solid {scroll_bar_theme.get("button").get("border")};
    border-radius: 3px;
    margin: 0;
}}
QScrollBar::handle:vertical:hover{{	
    border-color: {scroll_bar_theme.get("button").get("border-hover")};
}}
QScrollBar::handle:vertical:pressed {{	
    background-color: {scroll_bar_theme.get("button").get("background-pressed")};
}}
QScrollBar::sub-line:vertical {{
    border-bottom: 3px solid red;
    border: 1px solid {scroll_bar_theme.get("button").get("border")};
    background-color: {scroll_bar_theme.get("button").get("background")};
    height: 16px;
    subcontrol-position: top;
    subcontrol-origin: margin;
    border-radius: 3px;
}}
QScrollBar::sub-line:vertical:hover {{	
    border-color: {scroll_bar_theme.get("button").get("border-hover")};
}}
QScrollBar::sub-line:vertical:pressed {{	
    background-color: {scroll_bar_theme.get("button").get("background-pressed")};
}}
QScrollBar::add-line:vertical {{
    border: 1px solid {scroll_bar_theme.get("button").get("border")};
    background-color: {scroll_bar_theme.get("button").get("background")};
    height: 16px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
    border-radius: 3px;
}}
QScrollBar::add-line:vertical:hover {{	
    border-color: {scroll_bar_theme.get("button").get("border-hover")};
}}
QScrollBar::add-line:vertical:pressed {{	
    background-color: {scroll_bar_theme.get("button").get("background-pressed")};
}}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
    background: none;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}
QScrollBar:horizontal {{
    border: 1px solid {scroll_bar_theme.get("base").get("border")};
    background: {scroll_bar_theme.get("base").get("background")};
    height: 16px;
    margin: 0 17px 0 17px;
}}
QScrollBar::handle:horizontal {{	
    background-color: {scroll_bar_theme.get("button").get("background")};
    min-width: 30px;
    border: 1px solid {scroll_bar_theme.get("button").get("border")};
    border-radius: 3px;
    margin: 0;
}}
QScrollBar::handle:horizontal:hover{{	
    border-color: {scroll_bar_theme.get("button").get("border-hover")};
}}
QScrollBar::handle:horizontal:pressed {{	
    background-color: {scroll_bar_theme.get("button").get("background-pressed")};
}}
QScrollBar::sub-line:horizontal {{
    border-right: 3px solid red;
    border: 1px solid {scroll_bar_theme.get("button").get("border")};
    background-color: {scroll_bar_theme.get("button").get("background")};
    width: 16px;
    subcontrol-position: left;
    subcontrol-origin: margin;
    border-radius: 3px;
}}
QScrollBar::sub-line:horizontal:hover {{	
    border-color: {scroll_bar_theme.get("button").get("border-hover")};
}}
QScrollBar::sub-line:horizontal:pressed {{	
    background-color: {scroll_bar_theme.get("button").get("background-pressed")};
}}
QScrollBar::add-line:horizontal {{
    border: 1px solid {scroll_bar_theme.get("button").get("border")};
    background-color: {scroll_bar_theme.get("button").get("background")};
    width: 16px;
    subcontrol-position: right;
    subcontrol-origin: margin;
    border-radius: 3px;
}}
QScrollBar::add-line:horizontal:hover {{	
    border-color: {scroll_bar_theme.get("button").get("border-hover")};
}}
QScrollBar::add-line:horizontal:pressed {{	
    background-color: {scroll_bar_theme.get("button").get("background-pressed")};
}}
QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {{
    background: none;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}
"""

    # TODO: need to dynamically add this stuff
    # TODO: make tabs slightly over lap each other horizontally

    q_tab_widget = f"""
#tabArea {{
    background-color: #2f3132;
    border-radius: 5px;
}}   
QTabWidget::pane {{ /* The tab widget frame */
    border: 1px solid #545454;
    border-radius: 5px;
}}
QTabWidget::tab-bar {{
    left: 5px; /* move to the right by 5px */
    top: 8px;
}}
QTabBar QToolButton {{
    border: 1px solid #686a6b;
    background-color: #3f3f3f;
    border-radius: 3px;
}}
QTabBar QToolButton:hover {{
    background-color: #2f3132;;
}}
/* Style the tab using the tab sub-control. Note that
    it reads QTabBar _not_ QTabWidget */
QTabBar::tab {{
    color: #939393;
    background: #3f3f3f;
    border: 1px solid #545454;
    border-bottom-color: #545454; /* same as the pane color */
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    min-width: 12ex;
    padding: 4px;
}}
QTabBar::tab:selected, QTabBar::tab:hover {{
    color: #3498db;
    background: #2f3132;
}}
QTabBar::tab:selected {{
    border-color: #9B9B9B;
    border-bottom-color: #2f3132; /* same as pane color */
}}
QTabBar::tab:selected {{
    margin-top: 2px; /* make non-selected tabs look smaller */
}} 
"""

    tool_tip = f"""
QToolTip {{
    background-color: #434547;
    border: 1px solid #d3d3d3;
    padding: 2px;
    border-radius: 2px;
    color: #d3d3d3;
}}
"""
# TODO properly pass svgs here 
    spinbox_style_widgets = """
QSpinBox, 
QDoubleSpinBox,
QDateTimeEdit {
	background-color: #434547;
	color: #d3d3d3;
	border: 1px solid #686a6b;
	border-radius: 3px;
	padding : 2px;
}

QSpinBox::disabled, 
QDoubleSpinBox::disabled,
QDateTimeEdit::disabled {
	background-color: #404040;
	color: #d3d3d3;
	border-color: #434547;
}

QSpinBox:hover, 
QDoubleSpinBox::hover,
QDateTimeEdit::hover {
    background-color: #434547;
    border: 1px solid #d3d3d3;
    color:  #d3d3d3;
    padding: 2px
}

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button,
QDateTimeEdit::up-button, QDateTimeEdit::down-button {
    background-color: #363636;
	border-radius: 2px;
    height: 11px;
}

QSpinBox::disabled, 
QDoubleSpinBox::disabled,
QDateTimeEdit::disabled {
	background-color: #404040;
	color: #656565;
	border-color: #686a6b;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover,
QDateTimeEdit::up-button:hover, QDateTimeEdit::down-button:hover {
    background-color: #3f3f3f;
}

QSpinBox::up-button:disabled, QSpinBox::down-button:disabled,
QDoubleSpinBox::up-button:disabled, QDoubleSpinBox::down-button:disabled,
QDateTimeEdit::up-button:disabled, QDateTimeEdit::down-button:disabled {
	background-color: #404040;
	color: #656565;
	border-color: #686a6b;
}

QSpinBox::up-button:pressed, QSpinBox::down-button:pressed,
QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button::pressed,
QDateTimeEdit::up-button:pressed, QDateTimeEdit::down-button::pressed {
    background-color: #3498db;
    border: 1px solid #3498db;
}

QSpinBox::down-arrow,
QDoubleSpinBox::down-arrow,
QDateTimeEdit::down-arrow {
    image: url(mp4muxtool/frontend/svg/arrow_drop_down.svg);
    width: 20px;
    height: 20px;
}

QSpinBox::up-arrow,
QDoubleSpinBox::up-arrow,
QDateTimeEdit::up-arrow {
    image: url(mp4muxtool/frontend/svg/arrow_drop_up.svg);
    width: 20px;
    height: 20px;
}
"""

    return main_window + scroll_bar + q_tab_widget + tool_tip + spinbox_style_widgets
