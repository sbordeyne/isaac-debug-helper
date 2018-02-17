import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from constants import *
from functions import *

class DebugFrame(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self,master)
		self.master = master
		self.started = False
		self.log_path = get_log_path()
		self.oldline = "  "
		self.tags = TAGS
		self.max_mem = MAX_LUA_MEMORY*1024
		self.mem = 0
		self.init_layout()
		pass

	def init_layout(self):	
		self.labelStatus = tk.Label(self, text="Debugger status: stopped", foreground="red")
		self.labelStatus.pack(side=tk.TOP, fill=tk.X)
		
		self.scrollbar = tk.Scrollbar(self)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.progressbar = ttk.Progressbar(self, orient="horizontal", length=410, mode="determinate")
		self.progressbar.pack(side=tk.BOTTOM, fill=tk.X)
		self.progressbar["value"] = 0
		self.progressbar["maximum"] = self.max_mem
		
		
		self.label = tk.Label(self, text=("LUA", "memory","usage",":", self.mem, "of", self.max_mem, "Bytes"))
		self.label.pack(side=tk.BOTTOM,in_=self.progressbar)

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
				if "err" in tmp or "exception" in tmp and not "overlayeffect" in tmp and not "animation" in tmp: #Error filter to display
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
					
					self.mem = kb*1024+by
					self.label.config(text=("LUA", "memory","usage",":", self.mem, "of", self.max_mem, "Bytes"))
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
		self.labelStatus.config(text="Debugger status: started", foreground="green")
		self.log_f = open(self.log_path, "r")
		self.started = True
		self.readfile()
		pass
	def stop(self):
		try: #In case of click on "Stop" when debugger has never been started. Otherwise raises exception "DebugFrame has no object log_f"
			self.log_f.close()
			self.labelStatus.config(text="Debugger status: stopped", foreground="red")
			self.started = False
		except AttributeError:
			pass
		pass
	def clear(self):
		if not self.started :
			self.output.delete(1.0,"end")
			self.progressbar["value"] = 0
			self.mem = 0
			self.label.config(text=("LUA", "memory","usage",":", self.mem, "of", self.max_mem, "Bytes"))
		else:
			messagebox.showinfo(title="Warning", icon="warning", message="Debugger is running! You have to stop it before you can clear the text.")
		pass

	def auto_reload(self):
		global AUTO_RELOAD
		if AUTO_RELOAD:
			if is_isaac_running() and not self.started:
				self.start()
			elif not is_isaac_running() and self.started:
				self.stop()
	pass
