#-*- encoding:utf-8 -*-
#!/usr/bin/python3

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import time
import configparser
from tkinter import colorchooser

from constants import *
from functions import *
from debug import DebugFrame


class GUI(tk.Frame):
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
		self.menubar.add_command(label="Clear", command=self.tab_debugger.clear)
		self.menubar.add_command(label="Options", command=self.open_options)
		self.menubar.add_command(label="Check for updates", command=updateCheckClass.update)
		self.menubar.add_command(label="About", command=self.about)
		self.master.config(menu=self.menubar)
		pass
	def on_closing(self):
		if not OPTIONSOPEN:
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
		Isaac Debug Helper\n
		Version 2.1.0\n
		Fork by Team Dodo (based on software by Dogeek)\n
		For additional information, check out\n
		http://github.com/dogeek/isaac-debug-helper\n
		http://github.com/teamdodo/isaac-debug-helper\n
		License : GNU GPL 3.0
		"""
		messagebox.showinfo("About", message)
		pass

	def open_options(self):
		global OPTIONSOPEN
		if not OPTIONSOPEN:
			OPTIONSOPEN = True
			OptionGUI(master=self).mainloop()
	pass

class OptionGUI(tk.Toplevel): #TODO : make an option window to pick colors for error highlighting, add new filters
	def __init__(self, master = None):
		super(OptionGUI, self).__init__()
		global AUTO_RELOAD
		global MAX_LUA_MEMORY
		self.master = master
		self.title = "Options"
		self.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.tags = TAGS
		self.maxmem_var = tk.IntVar()
		self.maxmem_var.set(MAX_LUA_MEMORY)
		self.checkbutton_var = tk.IntVar()
		if AUTO_RELOAD:
			self.checkbutton_var.set(1)
		else:
			self.checkbutton_var.set(0)
		self.labels = []
		self.buttons = []
		self.config()
	def config(self):
		i=0
		for key, value in self.tags.items():
			self.labels.append(tk.Label(self, text=key))
			but = tk.Button(self, text=" ", width=10, background=value, command=lambda x=i: self.open_color_picker(x))
			self.buttons.append(but)
			i += 1
		for i in range(len(self.labels)):
			self.labels[i].grid(column=0, row=i)
			self.buttons[i].grid(column=1, row=i)
			self.buttons[i].config(command=lambda x=i:self.open_color_picker(x))
		self.checkbutton = tk.Checkbutton(self, variable=self.checkbutton_var, text="Auto-reload")
		self.checkbutton.grid(row=4, column=0, columnspan=2)
		tk.Label(self, text="Maximum LUA Memory (KB): ").grid(row=5, column=0)
		self.maxmem_scale = tk.Scale(self, variable=self.maxmem_var, orient="horizontal", from_=1, to=10*1024, command=self.scaleToGlobal)
		self.maxmem_scale.grid(row=5, column=1)

		self.reset_button = tk.Button(self, text="Reset to default", command=self.onResetButton)
		self.ok_button = tk.Button(self, text="Ok", command=self.onOkButton)
		self.cancel_button = tk.Button(self, text="Cancel", command=self.onCancelButton)
		self.reset_button.grid(row=6, columnspan=2, sticky="ew")
		self.ok_button.grid(column=0, row=7, sticky="ew")
		self.cancel_button.grid(column=1, row=7, sticky="ew")
		self.loopCheck()
	
	def on_closing(self):
		global OPTIONSOPEN
		OPTIONSOPEN = False
		self.destroy()	
	def open_color_picker(self, i):
		color = colorchooser.askcolor()
		if color[1] is not None:
			color = color[1]
		else:
			color = self.buttons[i]["background"]
		self.buttons[i].config(background=color)
		self.tags[self.labels[i]["text"]] = color
	def onOkButton(self):
		global TAGS
		global OPTIONSOPEN
		TAGS=self.tags
		OPTIONSOPEN = False
		
		config = configparser.ConfigParser()
		config["TAGS"] = TAGS
		config["GENERAL"] = {}
		config["GENERAL"]["maxmem"] = str(MAX_LUA_MEMORY)
		config["GENERAL"]["autoreload"] = str(AUTO_RELOAD)
		config["GEOMETRY"] = {}
		config["GEOMETRY"]["x"] = str(self.master.winfo_height())
		config["GEOMETRY"]["y"] = str(self.master.winfo_width())
		with open('config.cfg', 'w') as configfile:
			config.write(configfile)
		self.destroy()
	def onCancelButton(self):
		global OPTIONSOPEN
		OPTIONSOPEN = False
		self.destroy()
	def onResetButton(self):
		resetConfirm = messagebox.askyesno(title="Reset config", icon="warning", message="This will reset options to default AND CLOSE THE DEBUGGER. \n Are you sure?")
		if resetConfirm == True:
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
			sys.exit()
		else:
			global OPTIONSOPEN
			OPTIONSOPEN = False
			self.destroy()
	def scaleToGlobal(self, arg):
		global MAX_LUA_MEMORY
		MAX_LUA_MEMORY = self.maxmem_var.get()
	def loopCheck(self):
		global AUTO_RELOAD
		if self.checkbutton_var.get():
			AUTO_RELOAD = True
		else:
			AUTO_RELOAD = False
		self.after(20, self.loopCheck)
	pass
	
	
if __name__ == "__main__":
	root = tk.Tk()
	root.title("Isaac Debug Helper")
	root.geometry(GEOMETRY)
	gui = GUI(root)
	gui.pack()
	gui.mainloop()

