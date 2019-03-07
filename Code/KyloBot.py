import os
import discord
import discord.permissions
from discord.ext import commands
import asyncio
import threading
import time
import datetime
from Profiles import *
from Addon import *
import json
import urllib.request
import zipfile
from shutil import copyfile
from shutil import rmtree
from distutils.dir_util import copy_tree
import os
import sys


import tkinter
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

def get_now():
	now = datetime.datetime.now()
	return str("[{0}-{1}-{2} {3}:{4}:{5}]".format(now.day,now.hour,now.year,now.hour,now.minute,now.second))

class KyloBot(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.running = False
		self.commands = []
	async def on_ready(self):

		global window
		window.frame_general.console.print_message("[Info] Connexion effectuée !")
		window.frame_general.console.print_message("[Info] Bot: {0}".format(self.user.name))
		window.frame_general.console.print_message("[Info] Id: {0}".format(self.user.id))


		window.frame_general.servers_list.delete(0, END)
		self.servers_list = []
		for server in self.servers:
			self.servers_list.append(server)
			window.frame_general.servers_list.insert(END, server.name)

		await self.change_presence(game=discord.Game(name="Fait {0} pour obtenir de l'aide".format(self.profile.help), url="https://twitch.tv/KyloBot", type=1))

	async def on_message(self, message):
		if message.author != self.user:
			global window
			try:
				window.print_message("[Message] [{0}] {1}: {2}".format(message.channel, message.author, message.content))
			except:
				try:
					window.print_message("[Message] [{0}] {1}: {2}".format(message.channel, message.author.id, message.content))
				except:
					window.print_message("[Message] [{0}] {1}: {2}".format(message.channel.id, message.author.id, message.content))
			if message.content == self.profile.help:
				embed = discord.Embed(title="**[Aide]**", color=0xffff00)
				embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
				help = str()
				for cmd in self.commands:
					help = "{0}\n{1}".format(help, cmd)
				embed.add_field(name="__Liste des commandes:__", value=help)

				embed.set_footer(text="Développé par KyloRen3600")
				await self.send_message(message.channel, embed=embed)

	async def bg_task(self):
			await self.wait_until_ready()
			while not self.is_closed:
				if self.running == True:
					global discord_messages_to_send
					for message in discord_messages_to_send:
						await self.send_message(discord.Object(id=str(message[0])), '{0}'.format(message[1]))

					discord_messages_to_send = []
					await asyncio.sleep(0.1)
				else:
					await self.close()
					await self.logout()

def on_listbox_select(event):
	global client
	global window
	if str(event.widget) == ".!generalframe.!frame2.!frame.!frame.!listbox":
		try:
			w = event.widget
			index = int(w.curselection()[0])
			value = w.get(index)
			server = client.servers_list[index]
			window.frame_general.channels_list.delete(0, END)
			client.channels_list = []
			for channel in server.channels:
				if str(channel.type) == "text":
					client.channels_list.append(channel)
					try:
						window.frame_general.channels_list.insert(END, channel.name)
					except:
						window.frame_general.channels_list.insert(END, channel.id)
		except:
			pass
	if str(event.widget) == ".!generalframe.!frame2.!frame.!frame2.!listbox":
		try:
			w = event.widget
			index = int(w.curselection()[0])
			value = w.get(index)
			channel = client.channels_list[index]
			try:
				window.frame_general.console.print_message("[Info] Bascule sur le channel {0}.".format(channel.name))
			except:
				window.frame_general.console.print_message("[Info] Bascule sur le channel {0}.".format(channel.id))
			client.selected_channel = channel
		except:
			pass

def profiles_callback(event):
	global window
	index = event.widget.current()
	print_message("[Info] Vous avez sélectionné le bot {0}.".format(event.widget.profiles_names[index]))
	print_message("[Info] Chargement de {0}...".format(event.widget.profiles_files[index]))
	global profile_selected
	profile_selected = event.widget.profiles_files[index]
	window.frame_general.button_start.config(state=NORMAL)


class ClientWindow(tkinter.Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title("Kylo's Bot Manager")
		self.geometry("1000x500")
		self.menubar = MenuBar(self)
		self.open_general()
		with open("Version.json", 'r') as f:
			data = json.load(f)
			local_version = data["Version"]
		self.NothingGames = ttk.Label(self, text="Version {0} © NothingGames 2019".format(local_version)).pack(side=BOTTOM)

	def print_message(self, message):
		self.frame_general.console.print_message(message)

	def open_general(self):
		global client
		if client.running == False:
			try:
				self.current.pack_forget()
			except:
				pass
			self.frame_general = GeneralFrame(self)
			self.frame_general.pack(expand=YES, fill=BOTH)
			self.current = self.frame_general
		else:
			print_message("[Erreur] Impossible lorsque le Bot est lancé !")

	def open_configuration(self):
		global client
		if client.running == False:
			self.current.pack_forget()
			self.frame_configuration = ConfigurationFrame(self)
			self.frame_configuration.pack(expand=YES, fill=BOTH, side=TOP)
			self.current = self.frame_configuration
		else:
			print_message("[Erreur] Impossible lorsque le Bot est lancé !")

	def open_addons(self):
		global client
		if client.running == False:
			self.current.pack_forget()
			self.frame_configuration = AddonsFrame(self)
			self.frame_configuration.pack(expand=YES, fill=BOTH, side=RIGHT)
			self.current = self.frame_configuration
		else:
			print_message("[Erreur] Impossible lorsque le Bot est lancé !")




class GeneralFrame(tkinter.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.frame_void = Frame(self)
		void = Void(self.frame_void)
		void.pack()
		self.frame_void.pack(fill=BOTH, side=TOP)
		self.frame_buttons = Frame(self)
		self.button_start = ttk.Button(self.frame_buttons, text="Démarrer le bot", command=start_client, state=DISABLED)
		self.button_start.grid(row=1, column=1)
		void1 = Void(self.frame_buttons)
		void1.grid(row=2, column=1)
		self.profiles_text = Label(self.frame_buttons, text="Bot:").grid(row=3, column=1)
		self.profiles_select = ProfilesListBox(self.frame_buttons)
		self.profiles_select.bind('<<ComboboxSelected>>', profiles_callback)
		self.profiles_select.grid(row=4, column=1)
		void2 = Void(self.frame_buttons)
		void2.grid(row=5, column=1)
		self.channels_text = Label(self.frame_buttons, text="Channels:").grid(row=6, column=1)

		self.frame_select = Frame(self.frame_buttons)

		self.frame_select_server = Frame(self.frame_select)
		self.servers_list = Listbox(self.frame_select_server)
		self.servers_list.bind('<<ListboxSelect>>', on_listbox_select)
		self.servers_list.pack(side="left", fill="y")
		self.frame_select_server_scrollbar = ttk.Scrollbar(self.frame_select_server, orient="vertical")
		self.frame_select_server_scrollbar.config(command=self.servers_list.yview)
		self.frame_select_server_scrollbar.pack(side="right", fill="y")
		self.servers_list.config(yscrollcommand=self.frame_select_server_scrollbar.set)
		self.frame_select_server.grid(row=1, column=1)

		self.frame_select_channel = Frame(self.frame_select)

		self.channels_list = Listbox(self.frame_select_channel)
		self.channels_list.bind('<<ListboxSelect>>', on_listbox_select)
		self.channels_list.pack(side="left", fill="y")
		self.frame_select_channel_scrollbar = ttk.Scrollbar(self.frame_select_channel, orient="vertical")
		self.frame_select_channel_scrollbar.config(command=self.channels_list.yview)
		self.frame_select_channel_scrollbar.pack(side="right", fill="y")
		self.channels_list.config(yscrollcommand=self.frame_select_channel_scrollbar.set)
		self.frame_select_channel.grid(row=1, column=2)

		self.frame_select.grid(row=7, column=1)
		self.frame_buttons.pack(side=LEFT)
		self.console = ChatFrame(self)
		self.console.pack(expand=YES, side=RIGHT, fill=BOTH)

class ConfigurationFrame(tkinter.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.entry_size = 100

		self.profiles_box()

		self.frame_name = LabelFrame(self, text="Nom:", padx=20, pady=1, borderwidth=0, highlightthickness=0)
		self.input_name = StringVar()
		self.input_name.set("")
		self.input_name.trace_add("write", self.entry_callback)
		self.entry_name = ttk.Entry(self.frame_name, text=self.input_name, state=DISABLED, width=self.entry_size)
		self.entry_name.pack()
		Void(self).grid(row=21, column=1)

		self.frame_description = LabelFrame(self, text="Description:", padx=20, pady=1, borderwidth=0, highlightthickness=0)
		self.input_description = StringVar()
		self.input_description.set("")
		self.input_description.trace_add("write", self.entry_callback)
		self.entry_description = ttk.Entry(self.frame_description, text=self.input_description, state=DISABLED, width=self.entry_size)
		self.entry_description.pack()
		Void(self).grid(row=31, column=1)

		self.frame_prefix = LabelFrame(self, text="Préfixe:", padx=20, pady=1, borderwidth=0, highlightthickness=0)
		self.input_prefix = StringVar()
		self.input_prefix.set("")
		self.input_prefix.trace_add("write", self.entry_callback)
		self.entry_prefix = ttk.Entry(self.frame_prefix, text=self.input_prefix, state=DISABLED, width=self.entry_size)
		self.entry_prefix.pack()
		Void(self).grid(row=37, column=1)

		self.frame_help = LabelFrame(self, text="Commande d'aide:", padx=20, pady=1, borderwidth=0, highlightthickness=0)
		self.input_help = StringVar()
		self.input_help.set("")
		self.input_help.trace_add("write", self.entry_callback)
		self.entry_help = ttk.Entry(self.frame_help, text=self.input_help, state=DISABLED, width=self.entry_size)
		self.entry_help.pack()
		Void(self).grid(row=39, column=1)

		self.frame_token = LabelFrame(self, text="Token:", padx=20, pady=1, borderwidth=0, highlightthickness=0)
		self.input_token = StringVar()
		self.input_token.set("")
		self.input_token.trace_add("write", self.entry_callback)
		self.entry_token = ttk.Entry(self.frame_token, text=self.input_token, state=DISABLED, width=self.entry_size)
		self.entry_token.pack()
		Void(self).grid(row=41, column=1)

		self.button_save = ttk.Button(self, text="Enregistrer", command=self.save, state=DISABLED)
		Void(self).grid(row=51, column=1)

		self.button_delete = ttk.Button(self, text="Supprimer", command=self.delete, state=DISABLED)

		self.frame_name.grid(row=20, column=1)
		self.frame_description.grid(row=30, column=1)
		self.frame_prefix.grid(row=35, column=1)
		self.frame_help.grid(row=38, column=1)
		self.frame_token.grid(row=40, column=1)
		self.button_save.grid(row=50, column=1)
		self.button_delete.grid(row=60, column=1)
		self.selected_file = ""

	def profiles_callback(self, event):
		self.button_delete.config(state=DISABLED)
		self.entry_name.config(state=NORMAL)
		self.entry_description.config(state=NORMAL)
		self.entry_prefix.config(state=NORMAL)
		self.entry_help.config(state=NORMAL)
		self.entry_token.config(state=NORMAL)
		index = event.widget.current()
		if index == 0:
			self.input_name.set("Nom du Bot")
			self.input_description.set("Description du Bot")
			self.input_prefix.set("Préfixe des commandes")
			self.input_help.set("Commande d'aide")
			self.input_token.set("Token du Bot")
			self.selected_file = ""

		else:
			profile = Profile(event.widget.profiles_files[index])
			try:
				self.input_name.set(profile.name)
				self.input_description.set(profile.description)
				self.input_prefix.set(profile.prefix)
				self.input_help.set(profile.help)
				self.input_token.set(profile.token)
			except:
				pass
			self.selected_file = event.widget.profiles_files[index]
			self.button_delete.config(state=NORMAL)

	def entry_callback(self, event, event1, event2):
		done = False
		if self.input_name.get() != "":
			if self.input_description.get() != "":
				if self.input_prefix.get() != "":
					if self.input_help.get() != "":
						if self.input_token.get() != "":
							done = True
		if done == False:
			self.button_save.config(state=DISABLED)
		if done == True:
			self.button_save.config(state=NORMAL)

	def save(self):
		save = {}
		save["Name"] = self.input_name.get()
		save["Description"] = self.input_description.get()
		save["Prefix"] = self.input_prefix.get()
		save["HelpCommand"] = self.input_help.get()
		save["Token"] = self.input_token.get()
		with open("Profiles/{0}.json".format(save["Name"]), "w") as f_write:
			json.dump(save, f_write)
		self.profiles_box()
		self.entry_name.config(state=DISABLED)
		self.entry_description.config(state=DISABLED)
		self.entry_prefix.config(state=DISABLED)
		self.entry_help.config(state=DISABLED)
		self.entry_token.config(state=DISABLED)
		self.input_name.set("")
		self.input_description.set("")
		self.input_prefix.set("")
		self.input_help.set("")
		self.input_token.set("")

	def delete(self):
		try:
			os.remove(self.selected_file)
		except:
			pass
		self.profiles_box()
		self.entry_name.config(state=DISABLED)
		self.entry_description.config(state=DISABLED)
		self.entry_prefix.config(state=DISABLED)
		self.entry_help.config(state=DISABLED)
		self.entry_token.config(state=DISABLED)
		self.input_name.set("")
		self.input_description.set("")
		self.input_prefix.set("")
		self.input_help.set("")
		self.input_token.set("")

	def profiles_box(self):
		self.profiles_frame = LabelFrame(self, text="Bot:", padx=20, pady=1, borderwidth=0, highlightthickness=0)
		self.profiles_select = ProfilesListBox(self.profiles_frame)
		self.profiles_select.profiles_names.insert(0, "Créer un bot")
		self.profiles_select.profiles_files.insert(0, "")
		self.profiles_select.config(values=self.profiles_select.profiles_names, width=self.entry_size-3)
		self.profiles_select.bind('<<ComboboxSelected>>', self.profiles_callback)
		self.profiles_select.pack()
		self.profiles_frame.grid(row=10, column=1)
		Void(self).grid(row=11, column=1)

class AddonsFrame(Canvas):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config(borderwidth=0, highlightthickness=0)
		self.scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
		self.scrollbar.pack(side=RIGHT, fill="y")
		self.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.yview)


		self.frame = ttk.Frame(self)
		self.label_info = ttk.Label(self.frame, text="Attention: Les activations/désactivations d'addons prennent effet après un redémarrage !").pack(side=TOP)
		self.button_update = ttk.Button(self.frame, text="Mettre à jour les addons", command=self.download_update_ask)
		self.button_update.pack()
		global addons_list
		for addon in addons_list:
			addon_frame = AddonFrame(self.frame, text=addon.name)
			addon_frame.set_addon(addon)
			addon_frame.pack()
		self.create_window(0, 0, window=self.frame)
		self.frame.update_idletasks()
		self.config(scrollregion=self.bbox("all"))

	def download_update_ask(self):
		ask = askokcancel("Attention", "La mise à jour va écraser les Addons actuels")
		if ask == True:
			try:
				self.download_update()
			except:
				showerror("Information:", "Échec de la mise à jour !")
			else:
				showinfo("Information:", "Mise a jour réussie !")
				global addons_list
				global window
				addons_list = []
				load_addons(window, client, addons_list, False)
				window.open_addons()
	def download_update(self):
		url = "https://github.com/KyloRen3600/KyloBot-Addons/archive/master.zip"
		urllib.request.urlretrieve(url, "Temp/AddonsUpdate.zip")
		zip_ref = zipfile.ZipFile("Temp/AddonsUpdate.zip", 'r')
		zip_ref.extractall("Temp")
		zip_ref.close()
		path = './Temp/KyloBot-Addons-master'
		dst = "./Addons"
		files = os.listdir(path)
		for file in files:
			try:
				copyfile('./Temp/KyloBot-Addons-master/{0}'.format(file), "{0}/{1}".format(dst, file))
				os.remove('./Temp/KyloBot-Addons-master/{0}'.format(file))
			except:
				copy_tree('./Temp/KyloBot-Addons-master/{0}'.format(file), "{0}/{1}".format(dst, file))
				rmtree('./Temp/KyloBot-Addons-master/{0}'.format(file))
		rmtree('./Temp/KyloBot-Addons-master')
		os.remove('./Temp/AddonsUpdate.zip')

class AddonFrame(ttk.Labelframe):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	def set_addon(self, addon):
		self.addon = addon
		self.frame_info = ttk.Frame(self)
		self.label_description = ttk.Label(self.frame_info, text="Description: {0}".format(addon.description)).grid(row=10, column=1, sticky="nw")
		self.label_version = ttk.Label(self.frame_info, text="Version: {0}".format(addon.version)).grid(row=15, column=1, sticky="nw")
		self.label_file = ttk.Label(self.frame_info, text="Fichier: {0}.py".format(addon.file)).grid(row=20, column=1, sticky="nw")
		self.label_help_command = ttk.Label(self.frame_info, text="Commande d'aide: {0}".format(addon.help)).grid(row=30, column=1, sticky="nw")
		self.label_developer = ttk.Label(self.frame_info, text="Développeur: {0}".format(addon.developer)).grid(row=40, column=1, sticky="nw")
		self.label_toggle = ttk.Label(self.frame_info, text="Actif:").grid(row=50, column=1, sticky="nw")
		self.toggle = IntVar()
		if addon.status == "ENABLED":
			self.toggle.set(1)
		else:
			self.toggle.set(0)
		self.button_toggle = ttk.Checkbutton(self.frame_info, text=" ", variable=self.toggle, command=self.toggle_addon)
		self.button_toggle.grid(row=50, column=2, sticky="nw")
		self.frame_info.pack(side=LEFT, fill=BOTH)
		self.image = Image.open(self.addon.icon)
		self.image = self.image.resize((100, 100), Image.ANTIALIAS)
		self.photo = ImageTk.PhotoImage(self.image)
		canvas = Canvas(self, width=100, height=100)
		canvas.create_image(0, 0, anchor=NW, image=self.photo)
		canvas.pack(side=RIGHT)


	def toggle_addon(self):
		self.addon.toggle()


class Void(tkinter.Button):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config(relief=FLAT, state=DISABLED)


class MenuBar(tkinter.Menu):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.filemenu = Menu(self, tearoff=0)
		self.filemenu.add_command(label="Open")
		self.filemenu.add_command(label="Save")
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit")
		self.add_cascade(label="Bot", command=args[0].open_general)
		self.add_cascade(label="Configuration", command=args[0].open_configuration)
		self.add_cascade(label="Addons", command=args[0].open_addons)
		args[0].config(menu=self)




class ChatFrame(tkinter.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.messages = ScrolledText(self)
		self.messages.config(font=("Courrier"), state=DISABLED, yscrollcommand=True)
		self.input_user = StringVar()
		self.input_field = ttk.Entry(self, text=self.input_user, width=150)
		self.input_field.bind("<Return>", self.on_entry_press)
		self.messages.pack(expand=YES, fill=BOTH)
		self.input_field.pack(expand=YES)
		self.print_message("[Info] Veuillez sélectionner un bot")
		self.print_message("[Info] Pour ajouter un bot allez dans la section \"Configuration\"")

	def print_message(self, message):
		self.messages.config(state=NORMAL)
		self.messages.insert(INSERT, '%s\n' % "{0} {1}".format(get_now(), message))
		self.messages.config(state=DISABLED)
	def on_entry_press(self, entry):
		global client
		if self.input_field.get() != "":
			try:
				global discord_messages_to_send
				discord_messages_to_send.append((client.selected_channel.id, self.input_field.get()))
				try:
					self.print_message("[Message] [{0}] {1}: {2}".format(client.selected_channel.name, client.user.name, self.input_field.get()))
				except:
					self.print_message("[Message] [{0}] {1}: {2}".format(client.selected_channel.id, client.user.name, self.input_field.get()))

				self.input_user.set("")
			except:
				self.print_message("[Erreur] Aucun channel sélectionné !")
				self.input_user.set("")


def init_client():
	global client
	global discord_messages_to_send
	discord_messages_to_send = []
	client = KyloBot(".")

def start_client():
	global client
	global waiting
	waiting = False
	global window
	window.frame_general.console.print_message("[Info] Connexion du bot...")
	window.frame_general.button_start.config(state=DISABLED)
	window.frame_general.profiles_select.config(state=DISABLED)

def close():
	global window
	window.destroy()
	global client
	client.running = False
	global stop
	stop = True
	global waiting
	waiting = False

def show_window():
	global window
	window = ClientWindow()
	window.protocol("WM_DELETE_WINDOW", close)
	window.mainloop()



def print_message(message):
	global window
	window.frame_general.console.print_message(message)



stop = False
thread_window =threading.Thread(target=show_window)
thread_window.start()

init_client()
client_run = False
global window
global client
time.sleep(1)

addons_list = []
load_addons(window, client, addons_list, True)
global waiting
waiting = True
from random import randrange
while waiting == True:
	continue

if stop != True:
	global profile_selected
	profile = Profile(profile_selected)
	client.profile = profile
	client.running = True
	client.prefix = profile.prefix
	try:
		client.bg_task = client.loop.create_task(client.bg_task())
		client.run(profile.token)

	except discord.errors.LoginFailure:
		print_message("[Erreur] Token invalide:")
		window.frame_general.button_start.config(state=NORMAL)
		window.frame_general.profiles_select.config(state=NORMAL)
		client.running = False
		pass
thread_window.join()
