

class BundledApps:

    def __init__(self, main_gui):
        pass

    def mp4box(self):
        pass

    def mkv_extract(self):
        pass

    # # Bundled apps --------------------------------------------------------------------------------------------------------
    # mp4box = config['mp4box_path']['path']
    #
    # if not pathlib.Path(mp4box.replace('"', '')).is_file():  # Checks config for bundled app paths path
    #     # mp4box -----------------------------------------------------------------------
    #     if pathlib.Path('apps/mp4box/MP4Box.exe').is_file():  # If mp4box.exe is located in the apps folder
    #         messagebox.showinfo(title='Info', message='Program will use the included '
    #                                                   '"mp4box.exe" located in the "apps" folder')
    #         mp4box = '"' + str(pathlib.Path('apps/mp4box/MP4Box.exe')) + '"'  # sets variable to mp4box.exe
    #         try:  # Write path location to config.ini file
    #             config.set('mp4box_path', 'path', mp4box)
    #             with open(config_file, 'w') as configfile:
    #                 config.write(configfile)
    #         except (Exception,):  # If unable to write path to mp4box.exe present error message
    #             messagebox.showerror(title='Error!', message=f'Could not save path to mp4box at '
    #                                                          f'\n{mp4box}\n please try again')
    #     elif not pathlib.Path('apps/mp4box/MP4Box.exe').is_file():  # If mp4box.exe does not exist
    #         messagebox.showerror(title='Error!', message='Please download mp4box.exe and set path to '
    #                                                      'mp4box.exe in the Options menu')  # Error message
    #         webbrowser.open('https://www.mediafire.com/file/8pymy2869rmy5x5/mp4box.zip/file')  # Gets recent build
    #     # mp4box ------------------------------------------------------------------------
    #
    # mkvextract = config['mkvextract_path']['path']
    # if not pathlib.Path(mkvextract.replace('"', '')).is_file():  # Checks config for bundled app paths path
    #     # mkvextract -----------------------------------------------------------------------
    #     if pathlib.Path('apps/mkvextract/mkvextract.exe').is_file():  # If mkvextract.exe is located in the apps folder
    #         messagebox.showinfo(title='Info', message='Program will use the included '
    #                                                   '"mkvextract.exe" located in the "apps" folder')
    #         mkvextract = '"' + str(
    #             pathlib.Path('apps/mkvextract/mkvextract.exe')) + '"'  # sets variable to mkvextract.exe
    #         try:  # Write path location to config.ini file
    #             config.set('mkvextract_path', 'path', mkvextract)
    #             with open(config_file, 'w') as configfile:
    #                 config.write(configfile)
    #         except (Exception,):  # If unable to write path to mp4box.exe present error message
    #             messagebox.showerror(title='Error!', message=f'Could not save path to mkvextract at '
    #                                                          f'\n{mkvextract}\n please try again')
    #     elif not pathlib.Path('apps/mkvextract/mkvextract.exe').is_file():  # If mkvextract.exe does not exist
    #         messagebox.showerror(title='Error!', message='Please download mkvextract.exe and set path to '
    #                                                      'mkvextract.exe in the Options menu')  # Error message
    #         webbrowser.open('https://www.fosshub.com/MKVToolNix.html?dwl=mkvtoolnix-64-bit-64.0.0.7z')
    #         # Opens default web-browser to mkvextract (mkvtoolnix)
    #     # mkvextract ------------------------------------------------------------------------