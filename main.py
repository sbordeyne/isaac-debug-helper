import sys
from os.path import expanduser
#External libraries
try:
	import psutil
except ImportError:
	import tkinter.messagebox as messagebox
	messagebox.showinfo(title="Psutil not found", icon="error", message="Psutil not found. Autoreload will NOT work. \n Install it and launch the debugger again.")


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
	try:
		for p in psutil.process_iter():
			try:
				if 'isaac-ng' in p.name():
					return True
			except psutil.Error: 
				pass
		return False
	except  NameError: #NameError in case of psutil not found
		return False
