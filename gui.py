from Tkinter import *
import sys
import os
import tkMessageBox
import tkFileDialog
import shutil
import subprocess
import imp
import datetime

class GUI(object):

	def __init__(self, url, servr, user, pword, start):
		'''
		Initiates GUI object, its methods, and opens GUI window.
		'''
		# Initialize Tkinter interface within the class and set parameter variables
		self.url = url
		self.servr = servr
		self.user = user
		self.pword = pword

		self.start = start
		self.start.withdraw()
		self.start.destroy()

		self.root = Tk()

		# Set GUI interface window size
		#self.root.geometry('397x390')
		self.root.geometry('397x411')

		# Set GUI interface window title
		self.root.title("Test Scripts")

		# Closing protocol, allow smooth closing of program with X button
		self.root.protocol("WM_DELETE_WINDOW", self.quit)

		# Disable maximize button
		self.root.resizable(0,0)

		# Setup list of test scripts 
		self.script_list = []
		self.script_names = []
		self.script_total = 0

		# --- Create Menus ---

		# Create and configure dropdown menu
		menu = Menu(self.root)
		self.root.config(menu=menu)

		# Create user function dropdown menu
		selectmenu = Menu(menu)

		# Enable dropdown
		menu.add_cascade(label="Menu", menu=selectmenu)

		# Add menu options
		selectmenu.add_command(label="Add", command=self.input_file)
		selectmenu.add_command(label="Remove", command=self.remove)
		selectmenu.add_command(label="Search", command=self.lookup)	
		selectmenu.add_command(label="Run", command=self.run)

		selectmenu.add_separator()

		selectmenu.add_command(label="Clear Log", command=self.refresh)

		selectmenu.add_separator()

		selectmenu.add_command(label="Quit", command=self.quit)

		# ----- Format Window Layout -----

		# Select all check box		
		#on/off value for select all fn
		self.var_select = StringVar()
		self.var_select.set("0")
		check_select = Checkbutton(self.root, text="Select All", variable=self.var_select, command=self.select_all, anchor=N+W, height=2)
		check_select.grid(row=0, column=0, sticky=W)
		
		self.create_checkboxes()
		
		self.script_total = len(self.script_list)

		for testscript in self.script_list:
			self.script_names.append(testscript.cget("text"))

		separate = Label(self.root, text=" ")
		separate.grid(row=3, column=0, sticky=E+W)
		# --- Create Buttons ---
		# Button to run selected test script(s)
		run_button = Button(self.root, text="Run", command=self.run)
		run_button.grid(row=4, column=0, columnspan=2, sticky=E+W)

		# Create log entry in log.txt 
		self.log_header("a")

		# Open window
		mainloop()

	# ----- Class Methods -----------

	def input_file(self):
		# Opens directory for user to select a script to add to current directory, refreshes checkbox list -> make sure when adding checkbox to list, it does not change state of other checkboxes
		add_path = tkFileDialog.askopenfilename()
		add_name = os.path.basename(add_path)

		cur_dir = os.listdir(self.path)

		if add_path == "" or add_name[-3:] != ".py":                                                                                                                                                                                                                                                                                                            
			tkMessageBox.showwarning("Add Cancelled", "No test script selected.")
		elif add_name in cur_dir: #check if script does not already exist
			if tkMessageBox.askquestion("Add Conflict", "A test script with the same file name already exists.\nOverwrite the file?") == "yes":
				#find old checkbutton and replace with this one
				file_idxs = [i for i, x in enumerate(self.script_names) if x == add_name] #list of all occurences of testscript
				for file_i in file_idxs:
					del self.script_list[file_i]

				self.copy_script(add_path, self.path, add_name, True)

			else:
				tkMessageBox.showinfo("Add Abandoned", "Please add test scripts with distinct file names.")
		else:
			self.copy_script(add_path, self.path, add_name, False)

	def copy_script(self, src, dest, filename, overwrite):
		# Add script to test script folder
		if overwrite:
			self.script_list = []
			self.script_names = []			
			self.create_checkboxes()

			self.script_total = len(self.script_list)

			for testscript in self.script_list:
				self.script_names.append(testscript.cget("text"))
			
			shutil.copy(src, dest)
		else: 
			shutil.copy(src, dest)
			# Create new checkbutton for added test script
			var = StringVar()
			var.set("0")
			script = Checkbutton(text=filename, variable=var, width=50, anchor=S+W, command=self.checked)
			script.var = var
			
			#append checkbutton to list and update list length
			self.script_list.append(script)
			self.script_names.append(filename)
			self.script_total += 1

			# Embed checkbutton to GUI screen
			self.textbox.window_create(END, window=script)
					
			self.textbox.insert(END,"\n")

		print filename + " has been added."
		tkMessageBox.showinfo("Added", filename + " has been added.")
	
	def remove(self):
		# If checkbox selected, removes script from current directory (refreshes the checkbox list) and moves it to the "removed" folder
		removed_list = []
		unselected = 0		
		for testscript in self.script_list:
			if testscript.var.get() == '1':
				test_name = testscript.cget("text")				
				removed_list.append(test_name)
			else:
				unselected += 1

		total_removed = len(removed_list)
		removed_names = ""

		for i in range(total_removed):			
			removed_names += removed_list[i]

			if i+1 != total_removed:
				removed_names += ", "

		if unselected == self.script_total:
			tkMessageBox.showwarning("Remove Cancelled", "No test script selected.")
		elif tkMessageBox.askquestion("Remove?", "Remove " + removed_names +"?") == "yes":
			for testscript in self.script_list:
				if testscript.var.get() == '1':
					test_name = testscript.cget("text")
					
					file = self.path + "/" + test_name
					removed_folder = "<path to folder that contains scripts that were removed from the interface display>"
					
					removed_dir = os.listdir(removed_folder)

					if test_name in removed_dir:
						shutil.copy(file,removed_folder) #copy contents to removed file then delete from test scripts
						os.remove(file)
					else:
						shutil.move(file,removed_folder)

			# Reset the checkboxes					
			self.script_list = []
			self.script_names = []
			self.create_checkboxes() 
			self.script_total = len(self.script_list) 				
			for testscript in self.script_list:
				self.script_names.append(testscript.cget("text"))

			print removed_names + " has been removed."
			tkMessageBox.showinfo("Removed", removed_names + " has been removed.")
		else:
			pass
	
	def lookup(self):
		'''
		Opens a dialog window for user search queries. User enters name of script to be found, if exists, can click to select and/or exit lookup dialog. Else, message: "<script> not found. "
		'''
		# Open search window as a wait window, shifting focus to this window, with root and inventory lists as parameters
		self.end_search = ["option"]

		search = SearchWindow(self.root, self.script_list, self.script_names, self.end_search)
		self.root.wait_window(search.top)

		for testscript in self.script_list:
			if testscript.var.get() == "0":
				self.checked()

		if self.end_search[0] == "save":
			tkMessageBox.showinfo("Saved", "Changes to test script selection saved.")

	def run(self):
		# If checkbox selected, open module and run the test script		
		unselected = 0		
		for testscript in self.script_list:
			test_name = testscript.cget("text")
			if testscript.var.get() == '1':
				print "Executing " + test_name

				file = self.path + "/" + test_name
				
				# Open the file as a subprocess, input username and password from login info
				running = subprocess.Popen(['python.exe', file], stdin=subprocess.PIPE, stdout=subprocess.PIPE)				
				output = running.communicate(self.url+"\n"+self.servr+"\n"+self.user+"\n"+self.pword)[0]				
				running.wait()
				self.log(output)
			else:
				unselected += 1

		if unselected == self.script_total:
			tkMessageBox.showwarning("Run Cancelled", "No test script selected.")
		
	def select_all(self):
		if self.var_select.get() == '1':
			for testscript in self.script_list:
				testscript.var.set('1')
		else:
			for testscript in self.script_list:
				testscript.var.set('0') 

	def checked(self):
		# Unselects the "SELECT ALL" checkbox if it is already checked when a script has been unselected
		self.var_select.set("0")
		
	def quit(self):
		'''
		Closes program smoothly, without leaving behind any running interfaces.
		'''
		#output confirmation for quitting the program
		if tkMessageBox.askquestion("Quit", "You wish to exit the Test Script Program?") == 'yes':
			# Destroy master Tkinter interface instance 'root', closing the windows
			self.root.destroy()

	def create_checkboxes(self):
		'''
		Creates textbox in user interface.
		'''
		#create scrollbar and textbox objects
		self.scrollbar = Scrollbar(self.root, orient=VERTICAL)
		self.textbox = Text(self.root, yscrollcommand=self.scrollbar.set, height=20, width=47, relief=FLAT, bg="#f0f0ed")
		self.scrollbar.config(command=self.textbox.yview)

		#snap textbox and scrollbar to the grid system
		self.textbox.grid(row=2, column=0,sticky=S+E+W)
		self.scrollbar.grid(row=2,column=1,sticky=N+S+W)
		
		#populate the textbox with checkbox test scripts
		self.load_scripts()

		self.textbox.config(state=DISABLED)

		self.textbox.focus()

	def load_scripts(self):
		self.path = "<path to folder that contains automated scripts>" 
		
		#Open file directory
		directory = os.listdir(self.path)

		# Create checkbox for each testscript
		for testscript in directory:
			self.name = testscript
			if self.name[-3:] == ".py":
				var = StringVar()
				var.set("0")
				script = Checkbutton(text=self.name, variable=var, width=50, anchor=S+W, command=self.checked)
				script.var = var

				self.script_list.append(script)#append each checkbutton to list

				self.textbox.window_create(END, window=script)
				
				self.textbox.insert(END,"\n")

	def log(self,script_output):
		'''
		Writes any changes in the patient's medication history text file, saves the changes
		'''
		# Eliminate the raw_input prompts for username and password at the beginning of each script
		log_info = script_output[33:]

		#opens the log text file and writes data into it
		logfile = open('log.txt','a')
		logfile.write(log_info)
		logfile.close()

	def log_header(self, write_as):
		date = str(datetime.datetime.now())
		logfile = open('log.txt', write_as)
		logfile.write("-----------------------------------------------------------\nUser: " + self.user + "\nURL: " + self.url + "\nServer: " + self.servr + "\n" + date + "\n-----------------------------------------------------------\n\n")
		logfile.close()

	def refresh(self):
		if tkMessageBox.askquestion("Clear Log", "Clear log and create new entry?") == "yes":
			self.log_header('w')


class SearchWindow(GUI):
	def __init__(self, parent, scripts, names, end):#inventory, shop_boxes, cates):
		'''
		Creates SearchWindow object window as a child of GUI window, opening a dialog window where the user can search for a desired item using a searchbar or an interactive list box.
		'''
		# Initialize wait_window parameters
		self.top = Toplevel(parent)
		self.root = parent
		# Set window title
		self.top.wm_title("Test Script Search")

		# Disable maximize button
		self.top.resizable(0,0)

		# Initialize class variables
		self.scripts = scripts
		self.names = names
		self.end = end

		# Initialize list of items to add to list
		self.inv_search = []
		self.inv_search_names = []
		
		# Create searchbar for user input
		self.input = Entry(self.top)
		self.input.grid(row=0, column=0, columnspan=2, sticky=E+W)

		# Create button to initialize search
		search_b = Button(self.top, text="Search", command=self.search)
		search_b.grid(row=0, column=1, columnspan=2, sticky=E)
		
		separation1 = Label(self.top, text=" ", height=0)
		separation1.grid(row=1, columnspan=2, sticky=E+W)
		
		# Create and populate a listbox with all products available
		self.text_exist = False
		self.populate("")

		separation2 = Label(self.top, text=" ", height=0)
		separation2.grid(row=3, columnspan=2, sticky=E+W)

		# Create button to save selection of items found in search to the main gui window
		save_b = Button(self.top, text="Save Selection", command=self.save)
		save_b.grid(row=4, columnspan=2, sticky=E+W)

	def search(self):
		'''
		Generates search results from restrictions in the search bar.
		input:
		'''
		# Call function to generate search results in listbox
		if self.text_exist:
			self.searchbox.grid_forget()
		self.populate(self.input.get())

	def populate(self, param):
		'''
		Creates listbox and scrollbar for the window, filling the list with selectable
		   item object descriptions.
		'''
		# Create scrollbar and textbox objects
		self.scrollbar = Scrollbar(self.top, orient=VERTICAL)
		self.searchbox = Text(self.top, yscrollcommand=self.scrollbar.set, width=47, height=10, relief=FLAT, bg="#f0f0ed")
		self.scrollbar.config(command=self.searchbox.yview)

		# Snap textbox and scrollbar to the grid system
		self.searchbox.grid(row=2, column=0, columnspan=2, sticky=N+E+S+W)
		self.scrollbar.grid(row=2, column=2, sticky=N+S+W)

		self.found_total = 0

		for testscript in self.scripts:
			# Check for restrictions from searchbar and find matches of testscript name with the restriction
			if param == "" or param.lower() in testscript.cget("text").lower():
				self.found_checkbox(testscript, param)				
			
		if self.found_total == 0:
			# Default add if list is empty after restrictions
			self.searchbox.insert(END, "No test scripts found.")

		self.searchbox.config(state=DISABLED)
		self.searchbox.focus()

		self.text_exist = True

	def found_checkbox(self, script, param):
		name = script.cget("text")
		on_off = StringVar()

 		# Retain the check status if checkbox has been previously selected/unselected while user manipulating search window
		if name in self.inv_search_names or (name in self.inv_search_names and param == ""): 
			idx_list = [i for i, x in enumerate(self.inv_search_names) if x == name] #list of all occurences of name, and extract the most recent
			script_idx = idx_list[-1] 

			check_status = self.inv_search[script_idx].var.get()

			on_off.set(check_status)
		else:
			on_off.set(script.var.get())

		# Create test script checkbutton and update check status
		found_script = Checkbutton(self.top, text=name, variable=on_off, width=50, anchor=S+W) 
		found_script.var = on_off

		if found_script.var.get() == "1":
			found_script.select()
		else:
			found_script.deselect()
		
		# Add checkbutton to list
		self.inv_search.append(found_script)
		self.inv_search_names.append(name)

		# Embed found script to search window
		self.searchbox.window_create(END, window = found_script)
		self.searchbox.insert(END, "\n")

		self.found_total += 1

	def save(self):				
		if tkMessageBox.askquestion("Save?", "Save changes and exit search?") == "yes":			
			for test in self.inv_search:
				new_var = test.var.get()
				script_idx = self.names.index(test.cget("text"))
				
				if self.scripts[script_idx].var.get() != new_var:
					self.scripts[script_idx].var.set(new_var)

			# Close search window
			self.top.destroy()
			self.end[0] = "save"
		else:
			tkMessageBox.showinfo("Save Cancelled", "Changes to test script selection discarded.\nContinue Search.")
