import sys
from os.path import expanduser
#External libraries
import psutil

def get_log_path():
	p = ""
	if sys.platform == "linux" or sys.platform == "linux2":
		p = expanduser("~/.local/share/binding of isaac afterbirth+/log.txt")
	elif sys.platform == "darwin":
		p = expanduser("~/Library/Application Support/Binding of Isaac Afterbirth+/log.txt")
	elif sys.platform == "win32":
		p = expanduser("~/Documents/My Games/binding of isaac afterbirth+/log.txt")
	return p

def is_isaac_running():
	for p in psutil.process_iter():
		try:
			if 'isaac-ng' in p.name():
				return True
		except psutil.Error:
			pass
	return False
