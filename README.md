# Mp4-Mux-Tool # 
[![v1_21.png](https://thumbs2.imgbox.com/f7/c7/HoqzbyR2_t.png)](https://images2.imgbox.com/f7/c7/HoqzbyR2_o.png)

## New version of the app is being developed slowly as time allows ##
I'm working on a new version in a modern framework for the UI. This will support all of the same features as this one plus some. 
I am developing it slowly as I have time, this means this particular version is in "maintenance mode". It's stable enough and 
reliable in the mean time. I'll fix bugs as they are reported though. If you're interested in the progress of this, you can follow
this [branch](https://github.com/jlw4049/MP4-Mux-Tool/tree/qt-re-work).

## Supported Operating Systems ##
Windows 8 - Windows 11

*Technically it could work on linux/mac, but these builds would not include mp4box/mkvextract, for the new version I'm working on this will have that support*

# How to use #
## Main Gui ##
1. Extract program from archive to a folder of your choice or Run program from the archive (if you run from archive the 
program cannot save user settings)
2. Open/Drag and Drop Video Source into Video Input, select optional options
3. Open/Drag and Drop Audio Source into Audio Input, select optional settings - Program supports files with multiple 
audio tracks, you may select which track you want to be added into the final mux via the track selection window
4. Open/Drag and Drop Subtitle source, Chapter Source, etc...
5. Program only needs a video source to mux, you can also drag the same source for both video/audio if you need.
6. Output is automatically defined, the user can however select another location by pressing 'Output' if they desire
7. Press 'Mux' to begin muxing
8. Selecting 'View Command' will open a small window with the entire command line output being sent to mp4box.exe
9. In 'Options' menu above there is configurable options that are saved when selected, if you have any issues please set 
the 'Shell Options' from 'Progress Bars' to 'Debug' to see what error is provided 
