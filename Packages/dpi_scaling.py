import ctypes


def enable_dpi_scaling():
    """Enables high DPI scaling for Windows"""
    # if your windows version >= 8.1
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    # win 8.0 or less
    except:
        ctypes.windll.user32.SetProcessDPIAware()
