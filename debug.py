#-*- encoding:utf8 -*-
#!/usr/bin/python3
#By Dogeek - Lead Developper of The Binding Of Isaac - Stillbirth
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser
import sys
import time
from os.path import expanduser
import configparser
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

OPTIONSOPEN = False
config = configparser.ConfigParser()
config.read("config.cfg")
TAGS = config["TAGS"]
MAX_LUA_MEMORY = config["GENERAL"].getint("maxmem")
AUTO_RELOAD = config["GENERAL"].getboolean("autoreload")
GEOMETRY = config["GEOMETRY"]["x"] + "x" + config["GEOMETRY"]["y"]
"""
TAGS = {
			"error":"#FF0000",
			"warning":"#00FF00",
			"info":"#0000FF",
			"luadebug":"#000000"
}
MAX_LUA_MEMORY = 1024*1024*3 #bytes (3MB)
AUTO_RELOAD = True
"""

class OptionGUI(tk.Toplevel): #TODO : make an option window to pick colors for error highlighting, add new filters
	def __init__(self, master = None):
		super(OptionGUI, self).__init__()
		global AUTO_RELOAD
		global MAX_LUA_MEMORY
		self.master = master
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

		self.ok_button = tk.Button(self, text="Ok", command=self.onOkButton)
		self.cancel_button = tk.Button(self, text="Cancel", command=self.onCancelButton)
		self.ok_button.grid(column=0, row=6)
		self.cancel_button.grid(column=1, row=6)
		self.loopCheck()

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
		self.destroy()
	def onCancelButton(self):
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

class GUI(tk.Frame): #TODO: lua mem usage filter to display in a separate widget to not clutter the text widget, add scroll bar, try to auto reload if the lua file is deleted & add a about/options menu
	def __init__(self, master=None):
		super(GUI, self).__init__()
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.started = False
		self.log_path = get_log_path()
		self.oldline = "  "
		self.tags = TAGS
		self.max_mem = MAX_LUA_MEMORY*1024
		self.init_layout()
		pass

	def init_layout(self):
		self.menubar = tk.Menu(self)
		self.menubar.add_command(label="Start", command=self.start)
		self.menubar.add_command(label="Stop", command=self.stop)
		self.menubar.add_command(label="Options", command=self.open_options)
		self.master.config(menu=self.menubar)

		self.scrollbar = tk.Scrollbar(self)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.progressbar = ttk.Progressbar(self, orient="horizontal", length=410, mode="determinate")
		self.progressbar.pack(side=tk.BOTTOM, fill=tk.X)
		self.progressbar["value"] = 0
		self.progressbar["maximum"] = self.max_mem

		self.output = tk.Text(self)
		self.tag_config()
		self.output.config(font="sans 10", width=200, height=60, yscrollcommand=self.scrollbar.set)
		self.output.pack(side=tk.LEFT, fill=tk.BOTH)
		self.scrollbar.config(command=self.output.yview)
		self.readfile()
		pass

	def tag_config(self):
		for key, value in self.tags.items():
			self.output.tag_config(key, foreground=value)
		pass

	def readfile(self):
		if self.started:
			self.tags = TAGS
			self.tag_config()
			tmp = self.log_f.readline().lower()
			if self.oldline != tmp: #display spam only once@FileLoad
				self.output.config(state=tk.NORMAL)
				if "err" in tmp or "error" in tmp and not "overlayeffect" in tmp and not "animation" in tmp: #Error filter to display
					self.output.insert(tk.END, tmp, "error")
				elif "lua mem usage" in tmp:
					mem_txt = tmp.split("lua mem usage: ")[1]
					kb = mem_txt.split(" kb")[0]
					by = mem_txt.split(" and ")[1].split(" bytes")[0]
					try:
						kb = int(kb)
						by = int(by)
					except ValueError as e:
						print(e)
						exit(1)
					self.progressbar["value"] = kb*1024+by
				elif "lua" in tmp and not "debug" in tmp:
					self.output.insert(tk.END, tmp, "info")
				elif "warn" in tmp:
					self.output.insert(tk.END, tmp, "warning")
				elif "lua debug" in tmp:
					self.output.insert(tk.END, tmp, "luadebug")
				self.oldline = tmp
			self.output.see(tk.END)
			self.update_idletasks()
			self.after(5, self.readfile)
		pass
	def start(self):
		self.log_f = open(self.log_path, "r")
		self.started = True
		self.readfile()
		pass
	def stop(self):
		self.log_f.close()
		self.started = False
		pass

	def auto_reload(self):
		global AUTO_RELOAD
		if AUTO_RELOAD:
			if is_isaac_running() and not self.started:
				self.start()
			elif not is_isaac_running() and self.started:
				self.stop()
	def open_options(self):
		global OPTIONSOPEN
		if not OPTIONSOPEN:
			OPTIONSOPEN = True
			options = OptionGUI(master=self.master)
			options.mainloop()
	def on_closing(self):
		config = configparser.ConfigParser()
		config["TAGS"] = TAGS
		config["GENERAL"] = {}
		config["GENERAL"]["maxmem"] = str(MAX_LUA_MEMORY)
		config["GENERAL"]["autoreload"] = str(AUTO_RELOAD)
		config["GEOMETRY"] = {}
		config["GEOMETRY"]["x"] = GEOMETRY.split("x")[0]
		config["GEOMETRY"]["y"] = GEOMETRY.split("x")[1]
		with open('config.cfg', 'w') as configfile:
			config.write(configfile)
		self.master.destroy()
	pass

if __name__ == "__main__":
	root = tk.Tk()
	root.title("Isaac Debug Helper")
	root.geometry(GEOMETRY)
	gui = GUI(root)
	gui.pack()
	gui.mainloop()
