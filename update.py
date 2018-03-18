import configparser
import os
import tkinter.messagebox as messagebox
from urllib.request import urlretrieve as download
import webbrowser

from constants import VERSION

class updateCheckClass():
	def update():
		updateCheck = messagebox.askyesno(title="Update check", message="Check for updates?")
		if updateCheck == True:
			try:
				download("http://raw.githubusercontent.com/teamdodo/isaac-debug-helper/master/update/update.cfg" , "update.cfg")
				config = configparser.ConfigParser()
				config.read("update.cfg")
				latestVersion = config["UPDATE"]["latestVersion"]
				latestVersionUrl = config["UPDATE"]["latestVersionUrl"]
				os.remove("update.cfg")
				if VERSION != latestVersion:
					updateMessage = "Un update is avaliable, do you want to download it? This will launch your default browser and open a link to download the update"
					updateDetail = "Your version: {0} \nLatest version: {1}".format(VERSION,latestVersion)
					updateDownload = messagebox.askyesno(title="Update avaliable", message=updateMessage, detail=updateDetail)
					if updateDownload == True:
						webbrowser.open(latestVersionUrl, new=1, autoraise=True)
				if VERSION == latestVersion:
					messagebox.showinfo(title="No update avaliable", message="No updates avaliable. You already have the latest version")
			except urllib.error.HTTPError:
				messagebox.showinfo(title="Error", icon="error", message="Error while downloading update info. Try again later")
			except KeyError or IOError:
				messagebox.showinfo(title="Error", icon="error", message="Error while reading update info. Try again later")
			except OSError:
				messagebox.showinfo(title="Error", icon="error", message="Error while deleting update info update.cfg. Try to delete it manually")
			except webbrowser.Error:
				messagebox.showinfo(title="Error", icon="error", message="Error while opening your browser. Try again later or visit manually {0}".format(latestVersionUrl))
			except:
				messagebox.showinfo(title="Error", icon="error", message="Unmanaged error while checking for updates. Try again later. \nIf this persists contact the developers.")
	pass
