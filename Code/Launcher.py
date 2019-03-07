import urllib.request
import json
from tkinter.messagebox import *
import zipfile
from shutil import copyfile
from shutil import rmtree
from distutils.dir_util import copy_tree
import os
import urllib.request, json


def download_update(self):
	url = "https://github.com/KyloRen3600/KyloBot/archive/master.zip"
	urllib.request.urlretrieve(url, "Temp/Update.zip")
	zip_ref = zipfile.ZipFile("Temp/Update.zip", 'r')
	zip_ref.extractall("Temp")
	zip_ref.close()
	path = './Temp/KyloBot-master'
	dst = ""
	files = os.listdir(path)
	for file in files:
		try:
			copyfile('./Temp/KyloBot-master/{0}'.format(file), "{1}".format(dst, file))
			os.remove('./Temp/KyloBot-master/{0}'.format(file))
		except:
			copy_tree('./Temp/KyloBot-master/{0}'.format(file), "{1}".format(dst, file))
			rmtree('./Temp/KyloBot-master/{0}'.format(file))
	rmtree('./Temp/KyloBot-master')
	os.remove('./Temp/Update.zip')






with urllib.request.urlopen("https://raw.githubusercontent.com/KyloRen3600/KyloBot/master/Code/Version.json") as url:
	data = json.loads(url.read().decode())
	version = data["Version"]

with open("Version.json", 'r') as f:
	data = json.load(f)
	local_version = data["Version"]

if version != local_version:
	print("Mise à jour disponible")
	ask = askyesno("Mise à jour disponible !", "Voulez vous l'installer ?")
	if ask == True:
		print("Installation")


else:
	print("A jour")






#import KyloBot