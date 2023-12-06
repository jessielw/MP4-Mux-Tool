from mp4muxtool.frontend.styles.global_theme import theme_global
from mp4muxtool.frontend.styles.nav_panel import theme_nav_panel
from mp4muxtool.frontend.styles.layout_content import theme_layout_content
from mp4muxtool.frontend.styles.video_content import theme_video_content
from mp4muxtool.frontend.styles.audio_content import theme_audio_content
from mp4muxtool.frontend.styles.status_box import theme_status_box
from mp4muxtool.frontend.styles.loading_bar import theme_loading_bar
from mp4muxtool.frontend.styles.custom_combo_box import theme_custom_combo_box

class StyleFactory():
    _instance = None
    theme = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StyleFactory, cls).__new__(cls)
            
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = StyleFactory()
        return cls._instance
    
    def update_theme(cls, theme):
        cls.theme = theme
        
    def get_global_theme(cls):
        return theme_global(cls.theme)
         
    def get_nav_theme(cls):
        return theme_nav_panel(cls.theme)
    
    def get_layout_theme(cls):
        return theme_layout_content(cls.theme)
    
    def get_video_content_theme(cls):
        return theme_video_content(cls.theme)
    
    def get_audio_content_theme(cls):
        return theme_audio_content(cls.theme)    
    
    def get_status_box_theme(cls):
        return theme_status_box(cls.theme)
    
    def get_loading_bar_theme(cls):
        return theme_loading_bar(cls.theme)    
    
    def get_custom_combo_box_theme(cls):
        return theme_custom_combo_box(cls.theme)
