import os
import importlib
import json

def load_addon(window, client, addon):
	window.print_message("[Info] Chargement de {0} {1}".format(addon.name, addon.version))
	mod = importlib.import_module('Addons.{0}'.format(addon.file))
	mod.init(window, client, addon)

def load_addons(window, client):
	path = '.\\Addons'
	files = os.listdir(path)
	for file in files:
		if file.endswith(".json"):
			addon = Addon("{0}\\{1}".format(path, file))
			try:
				error = addon.error
			except:
				if addon.status == "ENABLED":
					load_addon(window, client, addon)

class Addon():
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
				self.version = datastore["Version"]
			except:
				self.version = "1.0"
			try:
				self.prefix = datastore["Prefix"]
			except:
				self.prefix = ""
			try:
				self.file = datastore["File"]
			except:
				self.file = "File"

			try:
				self.status = datastore["Status"]
			except:
				self.stauts = "ENABLED"