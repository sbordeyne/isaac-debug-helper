import configparser

OPTIONSOPEN = False
config = configparser.ConfigParser()
config.read("config.cfg")
TAGS = config["TAGS"]
MAX_LUA_MEMORY = config["GENERAL"].getint("maxmem")
AUTO_RELOAD = config["GENERAL"].getboolean("autoreload")
GEOMETRY = config["GEOMETRY"]["x"] + "x" + config["GEOMETRY"]["y"]
