#!usr/bin/env python

import json
import hashlib

try:
	from Tkinter import *	# PYTHON 2
	import tkFont
	from urllib2 import urlopen
except ImportError:
	from tkinter import *	# PYTHON 3
	import tkinter.font as tkFont
	from urllib.request import urlopen
	
class Window(Frame):
	'''An api GUI template that is modified for the Marvel api. Use your own keys, these are fake.'''
	
	def __init__(self, master = None):
		Frame.__init__(self, master)

		self.master = master
		self.init_window()

	def init_window(self):
		self.master.title("Api Checker")
		self.pack(fill=BOTH, expand=1)

		# SET FONT FOR TEXT HEADERS
		verd12 = tkFont.Font(family='verdana', size=12, weight='bold')
		helv10 = tkFont.Font(family='Helvetica', size=10)

		# ADD MENU
		menu = Menu(self.master, bd=0.5)
		self.master.config(menu=menu)

		file = Menu(menu, tearoff=0)
		file.add_command(label='Exit', command=self.client_exit)
		menu.add_cascade(label='Exit', menu=file)

		help = Menu(menu, tearoff=0)
		help.add_command(label='Info', command=self.client_exit)
		help.add_command(label='Set up', command=self.client_exit)
		menu.add_cascade(label='Help', menu=help)

		# SET UP FRAMES
		lf = Frame(root)
		rf = Frame(root)
		lf.pack(side=LEFT, expand=True)
		rf.pack(padx=(18,18), side=LEFT, expand=True)
		rf.pack(pady=(18,12))
		
		# TOP LEFT PANEL LISTBOX
		self.lb_tasks = Listbox(lf, bg="white", font=helv10, width=65, height=16)
		self.lb_tasks.grid(row=0, column=0)

		# BOTTOM LEFT PANEL LISTBOX
		self.lb_tasksb = Listbox(lf, bg="white", font=helv10, width=65, height=17)
		self.lb_tasksb.grid(row=1, column=0)
				
		# LEFT PANEL TOP SCROLLBAR
		self.sb1 = Scrollbar(lf)
		self.sb1.grid(row=0,column=1, ipady=164, sticky=N)
		self.lb_tasks.configure(yscrollcommand=self.sb1.set)
		self.sb1.configure(command=self.lb_tasks.yview)
		
		# LEFT PANEL BOTTOM SCROLLBAR
		self.sb2 = Scrollbar(lf)
		self.sb2.grid(row=1,column=1, ipady=174, sticky=N)
		self.lb_tasksb.configure(yscrollcommand=self.sb2.set)
		self.sb2.configure(command=self.lb_tasksb.yview)

		# TEXT HEADER
		labelT = Label(rf, text="APPLICATION/JSON", font=verd12, fg='blue').pack(pady=(25,15)) #justify=CENTER,

		# ENTRY LABELS AND FIELDS
		label1 = Label(rf, text="Address").pack(fill=X)
		self.entry_1 = Entry(rf) #Never add stuff on the end of here
		self.entry_1.pack(fill=X)
		label2 = Label(rf, text="API-Key").pack(fill=X)
		self.entry_2 = Entry(rf)
		self.entry_2.pack(fill=X)
		label3 = Label(rf, text="Key-Hash").pack(fill=X)
		self.entry_3 = Entry(rf)
		self.entry_3.pack(fill=X, pady=(0,30))

		# BUTTONS
		subbutton = Button(rf, text="Submit", width=43, padx=2, pady=6, command=self.jsonify)
		subbutton.pack(fill=X)
		savebutton = Button(rf, text="Quit", padx=2, pady=6, command=self.client_exit)
		savebutton.pack(fill=X)
		
		# URL TEXT
		labelB = Label(rf, text="CHECK FOR OTHER URLS IN API", font=verd12, fg='blue').pack(pady=(45,20))
		
		# BUTTONS
		urlbutton = Button(rf, text="URL-Check", padx=2, pady=6, command=self.findurls)
		urlbutton.pack(fill=X)
		saveurlbutton = Button(rf, text="Submit URL", padx=2, pady=6, command=self.show_url)
		saveurlbutton.pack(fill=X)
		
		# RIGHT PANEL BOTTOM LISTBOX
		self.lb_tasksbt = Listbox(rf, bg="white", font=helv10, width=64, height=9, selectmode=SINGLE)
		self.lb_tasksbt.pack(side=LEFT, fill=X)

		# RIGHT PANEL BOTTOM SCROLLBAR
		sb3 = Scrollbar(rf)
		sb3.pack(side=RIGHT, ipady=86)
		self.lb_tasksbt.configure(yscrollcommand=sb3.set)
		sb3.configure(command=self.lb_tasksbt.yview)

	# GET API AND WRITE TO FILE 
	def jsonify(self):
		try:
			addr = self.entry_1.get()
			api_key = self.entry_2.get()
			auth_hash = self.entry_3.get()
			
			# CONCAT FIELD STRING ENTRIES
			url = addr + '?ts=1&apikey=' + api_key + '&hash=' + auth_hash
							
			with urlopen(url) as u:
				source = u.read()
			data = json.loads(source.decode('utf-8'))
			datb = json.dumps(data, indent=2)

			with open('last_api.json', 'w') as data:
				data.write(datb)
			self.jsonfile()

		except ValueError as e: 
			print(e)


	# SHOW IN TOP LEFT WINDOW
	def jsonfile(self):
		with open('last_api.json') as fo:
			for line in fo:
				self.write_window_a(str(line) + '\n')

	# FIND URLS AND SHOW IN BOTTOM RIGHT WINDOW
	def findurls(self):
		with open('last_api.json') as data:	
			datu = data.read()
			datbu = re.split(r'[,;{}]', datu)

		for line in datbu:
			if "http" in line:
				x = re.sub(r'.*http', 'http', line).strip('"')
				self.write_window_b(str(x))

			if "ftp" in line:			
				v = re.sub(r'.*ftp', 'ftp', line).strip('"')
				self.write_window_b(v)

	# QUIT PROGRAM
	def client_exit(self):
		exit()

	# WRITE TO TOP LEFT WINDOW 
	def write_window_a(self, text):
		self.lb_tasks.insert(END,str(text))
		self.update_idletasks()

	# WRITE TO BOTTOM RIGHT WINDOW
	def write_window_b(self, text):
		self.lb_tasksbt.insert(END,str(text))
		self.update_idletasks()

	# WRITE TO BOTTOM LEFT WINDOW
	def write_window_c(self, text):
		self.lb_tasksb.insert(END,str(text))
		self.update_idletasks()

	# SELECT URL FROM SEARCH AND WRITE TO FILE AND SHOW
	def show_url(self):
		try:
			url = self.lb_tasksbt.get(self.lb_tasksbt.curselection())
			api_key = self.entry_2.get()
			auth_hash = self.entry_3.get()
			
			url = url + '?ts=1&apikey=' + api_key + '&hash=' + auth_hash
			
			with urlopen(url) as u:
				source = u.read()
			data = json.loads(source.decode('utf-8'))
			datb = json.dumps(data, indent=2)

			with open('url_last_api.json', 'w') as datan:
				datan.write(datb)
				
			with open('url_last_api.json') as fo:
				for line in fo:
					self.write_window_c(str(line) + '\n')
		except ValueError as e:
			print(e)

root = Tk()
#root.configure(background='black')
root.option_add('*font', ('verdana', 10))
#root.geometry("1236x720")
#root.resizable(0, 0)
app = Window(root)
root.mainloop()
