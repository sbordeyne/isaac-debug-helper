#-*- encoding:utf8 -*-
#!/usr/bin/python3
#By Dogeek - Lead Developper of The Binding Of Isaac - Stillbirth
import tkinter as tk
import tkinter.ttk as ttk
import sys
import time
from os.path import expanduser

def get_log_path():
	p = ""
	if sys.platform == "linux" or sys.platform == "linux2":
		p = expanduser("~/.local/share/binding of isaac afterbirth+/log.txt")
	elif sys.platform == "darwin":
		p = expanduser("~/Library/Application Support/Binding of Isaac Afterbirth+/log.txt")
	elif sys.platform == "win32":
		p = expanduser("~/Documents/My Games/binding of isaac afterbirth+/log.txt")
	return p

TAGS = {
			"error":"#FF0000",
			"warning":"#00FF00",
			"info":"#0000FF",
			"luadebug":"#000000"
}

class OptionGUI(tk.Frame): #TODO : make an option window to pick colors for error highlighting, add new filters
	def __init__(self, master = None):
		super(OptionGUI, self).__init__()
		self.master = master
		self.tags = TAGS
		self.labels = []
		self.buttons = []
		self.config()
	def config(self):
		for key, value in self.tags.items():
			self.labels.append(tk.Label(self, text=key))
			self.buttons.append(tk.Button(self, text=" ", width=10, background=value, command=lambda: self.open_color_picker(i)))
		for i in range(len(self.labels)):
			self.labels[i].grid(column=0, row=i)
			self.buttons[i].grid(column=1, row=i)

	def open_color_picker(self, i):
		color = tk.colorchooser.askcolor()
		color = color[1]
		self.buttons[i] = color
		self.buttons[i].config(background=color)
		TAGS[self.labels[i]["text"]] = color
	pass

class GUI(tk.Frame): #TODO: lua mem usage filter to display in a separate widget to not clutter the text widget, add scroll bar, try to auto reload if the lua file is deleted & add a about/options menu
	def __init__(self, master=None):
		super(GUI, self).__init__()
		self.master = master
		self.start_stop = False
		self.log_path = get_log_path()
		self.oldline = "  "
		self.tags = TAGS
		self.max_mem = 1024*1024*3 #bytes (3MB)
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
		self.output.insert(tk.END, "lololol\n"*440)
		self.scrollbar.config(command=self.output.yview)
		self.readfile()
		pass

	def tag_config(self):
		for key, value in self.tags.items():
			self.output.tag_config(key, foreground=value)
		pass

	def readfile(self):
		if self.start_stop:
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
		pass
	def start(self):
		self.log_f = open(self.log_path, "r")
		self.start_stop = True
		self.readfile()
		pass
	def stop(self):
		self.log_f.close()
		self.start_stop = False
		pass
	def open_options(self):
		options_master = tk.Toplevel()
		options = OptionGUI(master=options_master)
		options.pack()
		options.mainloop()
	pass

if __name__ == "__main__":
	root = tk.Tk()
	root.title("Isaac Debug Helper")
	root.geometry("650x500")
	gui = GUI(root)
	gui.pack()
	gui.mainloop()
