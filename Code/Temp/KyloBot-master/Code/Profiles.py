import os
import json
import tkinter
from tkinter.ttk import *
from tkinter import *



def load_profiles():
	global profiles
	profiles = []
	path = '.\\Profiles'
	files = os.listdir(path)
	for file in files:
		if file.endswith(".json"):
			with open("{0}\\{1}".format(path, file), 'r') as f:
				datastore = json.load(f)
				#print(datastore["Name"])
				profiles.append("{0}\\{1}".format(path, file))



class ProfilesListBox(Combobox):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		load_profiles()
		self.profiles_names = []
		self.profiles_files = []
		global profiles
		if len(profiles) > 0:
			for profile in profiles:
				with open(profile, 'r') as f:
					datastore = json.load(f)
					try:
						test = Profile(profile)
						try:
							a = test.error
						except:
							self.profiles_names.append(datastore["Name"])
							self.profiles_files.append(profile)
							pass
					except:
						pass
			try:
				self.current(0)
			except:
				pass
			self.box_value = StringVar()
			self.box_value.set("Choisissez un bot")
			self.config(state="readonly", textvariable=self.box_value, values=self.profiles_names)


class Profile():
	def __init__(self, file):
		with open(file, 'r') as f:
			datastore = json.load(f)
			try:
				self.name = datastore["Name"]
			except:
				self.error = "Name"
			try:
				self.description = datastore["Description"]
			except:
				self.description = "Description non définie"
			try:
				self.prefix = datastore["Prefix"]
			except:
				self.prefix = "!"
			try:
				self.help = datastore["HelpCommand"]
			except:
				self.help = "help"
			try:
				self.token = datastore["Token"]
			except:
				self.error = "Token"


