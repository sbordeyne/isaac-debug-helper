import configparser

OPTIONSOPEN = False
VERSION = "2.1.0" #Used to check for updates
try: 
	config = configparser.ConfigParser()
	config.read("config.cfg")
	TAGS = config["TAGS"]
	MAX_LUA_MEMORY = config["GENERAL"].getint("maxmem")
	AUTO_RELOAD = config["GENERAL"].getboolean("autoreload")
	GEOMETRY = config["GEOMETRY"]["x"] + "x" + config["GEOMETRY"]["y"]
except KeyError or IOError: 
	import tkinter.messagebox as messagebox
	messagebox.showinfo(title="Error", icon="error", message="Config file not found or damaged. Config has been set to default!")
	config = configparser.ConfigParser()
	config["TAGS"] = {'error': '#ff0080','warning': '#00FF00', 'info': '#0000FF', 'luadebug': '#000000'}
	config["GENERAL"] = {}
	config["GENERAL"]["maxmem"] = "3096"
	config["GENERAL"]["autoreload"] = "True"
	config["GEOMETRY"] = {}
	config["GEOMETRY"]["x"] = "1018"
	config["GEOMETRY"]["y"] = "882"
	with open('config.cfg', 'w') as configfile:
		config.write(configfile)
	config.read("config.cfg")
	TAGS = config["TAGS"]
	MAX_LUA_MEMORY = config["GENERAL"].getint("maxmem")
	AUTO_RELOAD = config["GENERAL"].getboolean("autoreload")
	GEOMETRY = config["GEOMETRY"]["x"] + "x" + config["GEOMETRY"]["y"]	
