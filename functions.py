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

def is_update_available(current_version):
	try:
		import requests
		from bs4 import BeautifulSoup
		import re
		from distutils.version import StrictVersion
	except ImportError:
		import tkinter.messagebox as messagebox
		messagebox.showerror("Error", message="You need BeautifulSoup4, distutils and requests installed for version checking to work.")

	url = "https://github.com/Dogeek/isaac-debug-helper/releases"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	versions = [x for x in soup.find_all("span", class_="css-truncate-target")]
	github_version = versions[-1] if versions else "0.1"

	regex = re.compile(r"([\d.]+)")
	assert regex.match(current_version) is not None, "Current Version doesn't match the standardized version format (x.x.x.x)"
	assert regex.match(github_version) is not None, "Github Version doesn't match the standardized version format (x.x.x.x)"
	return StrictVersion(github_version)>StrictVersion(current_version)
