#-*- encoding:utf8 -*-
#!/usr/bin/python3

import tkinter as tk
from tkinter import colorchooser
from constants import *

class OptionGUI(tk.Toplevel): #TODO : make an option window to pick colors for error highlighting, add new filters
	def __init__(self, master = None):
		super(OptionGUI, self).__init__()
		global AUTO_RELOAD
		global MAX_LUA_MEMORY
		self.master = master
		self.master.title = "Options"
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
