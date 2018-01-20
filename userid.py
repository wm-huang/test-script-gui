from Tkinter import *
from gui import *
import os
import tkMessageBox

class Login(object):
	def __init__(self, window):
		'''
		Initiates Login object, its methods, and opens Login window.
		'''

		# Initialize Tkinter interface within the class
		start = self.start = window
		
		# Set Login window appearance attributes
		start.geometry('175x260')
		start.title("Login")
		start.resizable(0,0)

		# URL dropdown
		Label(start, text="URL").pack()
		sites = ["URL1","URL2"]
		self.site_var = StringVar()
		self.site_var.set(sites[0])
		drop_url = OptionMenu(start,self.site_var,*sites)
		drop_url.pack(padx=5, fill=X)

		# Server dropdown		
		Label(start, text="Server").pack()
		servers = ["Server1","Server2", "Server3"]
		self.server_var = StringVar()
		self.server_var.set(servers[0])
		drop_svr = OptionMenu(start,self.server_var,*servers)
		drop_svr.pack(padx=5, fill=X)

		# Create labels and user entry boxes within the window
		Label(start, text="Username").pack()
		# User entry information is stored for login
		self.uname = Entry(start)
		self.uname.pack(padx=5, fill=X)

		Label(start, text="Password").pack()
		self.passw = Entry(start)
		self.passw.pack(padx=5, fill=X)

		# Create a button to trigger login process
		login_button = Button(start, text="Login", command=self.login)
		login_button.pack(pady=5, fill=X)

		# Create a button to trigger adding new userid process
		create_button = Button(start, text="Add User ID", command=self.userid_create)
		create_button.pack(pady=5, fill=X)

		# Open window
		mainloop()

	# ----- Class Methods -----
	def login(self):
		'''
		Searches through text file database for matching login information.
		'''
		# URL information
		url_option = self.site_var.get()
		self.url = self.sitefn(url_option)

		# Server information
		server_option = self.server_var.get()		
		self.server = self.serverfn(server_option)

		# Verify login credentials
		creds = open('userid.txt', 'r')
		credslist = creds.readlines()

		usertotal = len(credslist)	
		
		if self.uname.get().replace(" "," ") == "" or self.passw.get().replace(" "," ") == "":
		    tkMessageBox.showerror("Empty Fields", "Fields must not be left empty")
		else:	   
			i = 0 
			log_error = "user not found"

			while i <= usertotal:
				userline = credslist[i]
				passwline = credslist[i+1]
				if userline[0:4] == "user" and userline[5:-1] == self.uname.get():
					if passwline[5:-1] != self.passw.get():
						log_error = "invalid passw"
						break	
					else:	
						log_error = "none"
						break
				i += 3

			if log_error == "invalid passw":
				# Error dialog for incorrect password
				tkMessageBox.showerror("Login Error", "Password invalid. Try again.")
			elif log_error == "none":
				# Create instance for GUI class
				instance = GUI(self.url, self.server, self.uname.get(), self.passw.get(), self.start)	
			else:
				# Error dialog for incorrect username
				tkMessageBox.showerror("Login Error", "User not found. Try again or add new User ID.")	
			
			creds.close()

	def userid_create(self):
		'''
		Creates new login account information to be stored in userid.txt
		'''
		if self.uname.get().replace(" "," ") == "" or self.passw.get().replace(" "," ") == "":
		    tkMessageBox.showerror("Empty Fields", "Fields must not be left empty")
		else:
			credentials = "user: " + self.uname.get() + "\npass: " + self.passw.get() + "\n"
			if tkMessageBox.askquestion("Confirm?", credentials) == "yes":
				creds = open('userid.txt', 'r')
				credslist = creds.readlines()
				usertotal = len(credslist)	

				add_fail = False

				i = 0
				while i <= usertotal:
					userline = credslist[i]
					passwline = credslist[i+1]
					
					if userline[0:4] == "user" and userline[5:-1] == self.uname.get():
						# Error dialog for username already exists
						tkMessageBox.showerror("Invalid User ID", "An account with the same user name already exists.")
						add_fail = True
						break
					
					i += 3

				if not add_fail:
					creds_w = open('userid.txt','a')
					creds_w.write("\n" + credentials)
					creds_w.close()

	def serverfn(self, value):
		if value ==	"Server1":
			return "Server1's address"
		elif value == "Server2":
			return	"Server2's address"
		elif value == "Server3":
			return "Server3's address"

	def sitefn(self, value):
		if value == "URL1":
			return "URL1"
		elif value == "URL2":
			return "URL2"

			