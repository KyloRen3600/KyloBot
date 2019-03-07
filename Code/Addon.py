import os
import importlib
import json

def load_addon(window, client, addon):
	window.print_message("[Info] Chargement de {0} {1}".format(addon.name, addon.version))
	mod = importlib.import_module('Addons.{0}'.format(addon.file))
	mod.init(window, client, addon)
	if addon.help != "" and addon.help_description != "":
		client.commands.append("`{0}` *{1}*".format(addon.help, addon.help_description))

def load_addons(window, client, addons_list, load):
	path = '.\\Addons'
	files = os.listdir(path)
	for file in files:
		if file.endswith(".json"):
			addon = Addon("{0}\\{1}".format(path, file))
			try:
				error = addon.error
				window.print_message("[Erreur] Échec du chargement de {0}: {1}".format("{0}\\{1}".format(path, file), addon.error))
			except:
				addons_list.append(addon)
				if load == True:
					if addon.status == "ENABLED":
						load_addon(window, client, addon)

class Addon():
	def __init__(self, file):
		with open(file, 'r') as f:
			self.datastore = json.load(f)
			self.json = file
			try:
				self.name = self.datastore["Name"]
			except:
				self.error = "Name"
			try:
				self.description = self.datastore["Description"]
			except:
				self.description = "Description non définie"
			try:
				self.version = self.datastore["Version"]
			except:
				self.version = "1.0"
			try:
				self.prefix = self.datastore["Prefix"]
			except:
				self.prefix = ""
			try:
				self.help = self.datastore["HelpCommand"]
			except:
				self.help = ""
			try:
				self.help_description = self.datastore["HelpCommandDescription"]
			except:
				self.help_description = ""
			try:
				self.file = self.datastore["File"]
			except:
				self.file = "File"
			try:
				self.status = self.datastore["Status"]
			except:
				self.status = "ENABLED"
			try:
				self.developer = self.datastore["Developer"]
			except:
				self.developer = "Inconnu"
			try:
				self.icon = self.datastore["Icon"]
			except:
				self.icon = "src/Unknown.png"

	def toggle(self):
		if self.status == "ENABLED":
			self.status = "DISABED"
		else:
			self.status = "ENABLED"
		self.datastore["Status"] = self.status
		with open(self.json, "w") as f_write:
			json.dump(self.datastore, f_write)