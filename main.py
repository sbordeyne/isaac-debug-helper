#-*- encoding:utf8 -*-
#!/usr/bin/python3

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import time
import configparser

from constants import *
from functions import *
from options import OptionGUI
from debug import DebugFrame


class GUI(tk.Frame): #TODO: lua mem usage filter to display in a separate widget to not clutter the text widget, add scroll bar, try to auto reload if the lua file is deleted & add a about/options menu
	def __init__(self, master=None):
		tk.Frame.__init__(self,master)
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.init_layout()
		pass

	def init_layout(self):
		self.tabBar = ttk.Notebook(self)
		self.tabBar.pack(fill=tk.BOTH, padx=2, pady=3)
		self.tab_debugger = DebugFrame(self.tabBar)
		self.tabBar.add(self.tab_debugger, text="Debugger")

		self.menubar = tk.Menu(self)
		self.menubar.add_command(label="Start", command=self.tab_debugger.start)
		self.menubar.add_command(label="Stop", command=self.tab_debugger.stop)
		self.menubar.add_command(label="Options", command=self.open_options)
		self.menubar.add_command(label="About", command=self.about)
		self.master.config(menu=self.menubar)
		pass
	def on_closing(self):
		config = configparser.ConfigParser()
		config["TAGS"] = TAGS
		config["GENERAL"] = {}
		config["GENERAL"]["maxmem"] = str(MAX_LUA_MEMORY)
		config["GENERAL"]["autoreload"] = str(AUTO_RELOAD)
		config["GEOMETRY"] = {}
		config["GEOMETRY"]["x"] = str(self.winfo_height())
		config["GEOMETRY"]["y"] = str(self.winfo_width())
		with open('config.cfg', 'w') as configfile:
			config.write(configfile)
		self.master.destroy()
	def about(self):
		message = """
		Isaac Debug Helper by Dogeek\n
		For additional information, check out\n
		http://github.com/dogeek/isaac-debug-helper\n
		License : Creative Commons
		"""
		messagebox.showinfo("About", message)
		pass

	def open_options(self):
		global OPTIONSOPEN
		if not OPTIONSOPEN:
			OPTIONSOPEN = True
			options = OptionGUI(master=self.master)
			options.mainloop()
	pass

if __name__ == "__main__":
	root = tk.Tk()
	root.title("Isaac Debug Helper")
	root.geometry(GEOMETRY)
	gui = GUI(root)
	gui.pack()
	gui.mainloop()
