from configparser import ConfigParser

config_file = "runtime/config.ini"  # Creates (if it doesn't exist) and defines location of config.ini
config = ConfigParser()
config.read(config_file)

if not config.has_section("mp4box_path"):
    config.add_section("mp4box_path")
if not config.has_option("mp4box_path", "path"):
    config.set("mp4box_path", "path", "")

if not config.has_section("mkvextract_path"):
    config.add_section("mkvextract_path")
if not config.has_option("mkvextract_path", "path"):
    config.set("mkvextract_path", "path", "")

if not config.has_section("ffmpeg_path"):
    config.add_section("ffmpeg_path")
if not config.has_option("ffmpeg_path", "path"):
    config.set("ffmpeg_path", "path", "")

if not config.has_section("debug_option"):
    config.add_section("debug_option")
if not config.has_option("debug_option", "option"):
    config.set("debug_option", "option", "Default")

if not config.has_section("auto_close_progress_window"):
    config.add_section("auto_close_progress_window")
if not config.has_option("auto_close_progress_window", "option"):
    config.set("auto_close_progress_window", "option", "on")

if not config.has_section("auto_chapter_import"):
    config.add_section("auto_chapter_import")
if not config.has_option("auto_chapter_import", "option"):
    config.set("auto_chapter_import", "option", "on")

if not config.has_section("reset_program_on_start_job"):
    config.add_section("reset_program_on_start_job")
if not config.has_option("reset_program_on_start_job", "option"):
    config.set("reset_program_on_start_job", "option", "off")

if not config.has_section("last_saved_dir"):
    config.add_section("last_saved_dir")
if not config.has_option("last_saved_dir", "dir"):
    config.set("last_saved_dir", "dir", "on")

if not config.has_section("window_positions"):
    config.add_section("window_positions")
if not config.has_option("window_positions", "mp4_gui"):
    config.set("window_positions", "mp4_gui", "")
if not config.has_option("window_positions", "demux_window"):
    config.set("window_positions", "demux_window", "")

if not config.has_section("theme"):
    config.add_section("theme")
if not config.has_option("theme", "selected_theme"):
    config.set("theme", "selected_theme", "system_default")

with open(config_file, "w") as configfile:
    config.write(configfile)
