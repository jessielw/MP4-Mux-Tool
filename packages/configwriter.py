from configparser import ConfigParser

from packages.configparams import config_file


def config_writer(section, option, value, cfg_file=config_file):
    """simple function to write information to config"""
    cfg = ConfigParser()
    cfg.read(cfg_file)
    cfg.set(section=section, option=option, value=value)
    with open(cfg_file, "w") as configfile:
        cfg.write(configfile)
