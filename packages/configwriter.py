from configparser import ConfigParser


def config_writer(file, section, option, value):
    """simple function to write information to config"""
    cfg = ConfigParser()
    cfg.read(file)
    cfg.set(section=section, option=option, value=value)
    with open(file, "w") as configfile:
        cfg.write(configfile)
