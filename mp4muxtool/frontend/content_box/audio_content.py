from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QToolButton, QTabWidget

from mp4muxtool.frontend.styles.styles import StyleFactory
from mp4muxtool.frontend.content_box.form_layout import LayoutContent
from mp4muxtool.backend.video_content import VideoContentBackEnd


class AudioContentTabbed(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("AudioContentTabbed")
        # self.setStyleSheet(StyleFactory.get_instance().get_audio_content_theme())
        
        # self.tab_data = []
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self._close_tab)
        # self.currentChanged.connect(self._update_tabs)     
        self.tabBar().tabMoved.connect(self._update_tabs)
        
        self._add_new_tab()    
                
        
    def _add_new_tab(self):
        new_tab = QWidget()
        new_tab.setObjectName("tabArea")
        # new_tab.setStyleSheet("background-color: #2f3132;")
        
        # audio_content.setObjectName("AudioLayout")
        # main_area = DummyAudioClass(self.count())
        # audio_content = AudioContent(self.theme)
        audio_content = LayoutContent(VideoContentBackEnd, "audio", "AudioLayout", self._get_supported_extensions(), 10)
        # self.tab_data.append(main_area)
        audio_content.setObjectName("tabArea")
        
        tab_layout = QVBoxLayout(new_tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)        
        tab_layout.addWidget(audio_content, 6)
        
        new_tab_button = LayoutContent._build_icon_buttons(QToolButton, "add_circle.svg", "addNewTab")
        new_tab_button.setStyleSheet(StyleFactory.get_instance().get_audio_content_theme())   
        new_tab_button.setFixedHeight(28)
        new_tab_button.setToolTip("Add new audio track")
        new_tab_button.clicked.connect(self._add_new_tab)   

        # Add your button or other widgets to the layout
        tab_layout.addWidget(new_tab_button, 1, Qt.AlignmentFlag.AlignRight)

        # Add the new tab to the QTabWidget
        self.addTab(new_tab, f"Track {self.count() + 1}")
        
        self.setCurrentIndex(self.count() - 1)       
    
    def _close_tab(self, index):
        if self.count() != 1:
            self.removeTab(index)
            self._update_tabs()
            
    # def _tabs_moved(self, from_index, to_index):
    #     # Update the track numbers based on the tab movement
    #     moved_tab = self.tab_data.pop(from_index)
    #     self.tab_data.insert(to_index, moved_tab)

    #     # Print the current state
    #     print([(f"Current {x.track}", f"OG {x.og_track}") for x in self.tab_data])
                  
    def _update_tabs(self):
        for tab_index in range(self.count()):
            self.setTabText(tab_index, f"Track {tab_index + 1}")  
            
            
        # for tab in self.count():
        #     print(tab)       
                 
            # Access the DummyAudioClass instance for the current tab
            # dummy_instance = self.widget(tab_index).findChild(DummyAudioClass)
            # if dummy_instance:
            #     print(f"Tab {tab_index + 1} - Track: {dummy_instance.track}, OG Track: {dummy_instance.og_track}")            
                         
        
    @staticmethod
    def _get_supported_extensions():
        return (
            ".avi",
            ".mp4",
            ".m1v",
            ".m2v",
            ".m4v",
            ".264",
            ".h264",
            ".hevc",
            ".h265",
            ".avc",
            # TODO: remove this once we're done testing
            ".mkv",
        )        