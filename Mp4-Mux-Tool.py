import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase

from mp4muxtool.frontend.main_window import Mp4MuxWindow


# TODO: We'll upgrade python to 10.5 or higher and remove union everywhere throughout
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    font_id = QFontDatabase.addApplicationFont("mp4muxtool/frontend/font/OpenSans-Medium.ttf")
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family, 9))
    app.setStyle("Fusion")
    main_window = Mp4MuxWindow()
    main_window.show()

    sys.exit(app.exec())