import discord
import asyncio
import threading
import time
import datetime

import tkinter
from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk

global color_background
color_background = "#0D5972"

def get_now():
	now = datetime.datetime.now()
	#now.year, now.month, now.day, now.hour, now.minute, now.second
	return str("[{0}-{1}-{2} {3}:{4}:{5}]".format(now.day,now.hour,now.year,now.hour,now.minute,now.second))

class BotPendu(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.running = True
		# create the background task and run it in the background
		self.bg_task = self.loop.create_task(self.bg_task())

	async def on_ready(self):
		print('------')
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		await self.send_message(discord.Object(id='547098879007522816'), '{0} Bot lancé...'.format(get_now()))

	async def bg_task(self):

			await self.wait_until_ready()
			while not self.is_closed:
				if self.running == True:
					global discord_messages_to_send
					for message in discord_messages_to_send:
						await self.send_message(discord.Object(id=str(message[0])), '{0} {1}'.format(get_now(), message[1]))
					discord_messages_to_send = []
					await asyncio.sleep(0.1)
				else:
					await self.logout()


class ClientWindow(tkinter.Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config(background=color_background)
		self.MenuBar = MenuBar(self)
		#self.MenuBar.pack(side=TOP)
		self.MenuBar.grid(row=1)

		self.frame_bot = Frame(self, background=color_background)
		self.power_button = PowerButton(self.frame_bot)
		self.console = ChatFrame(self.frame_bot)

		self.power_button.grid(row=1, column=1)
		self.console.grid(row=2, column=2)
		#self.frame_bot.pack(side=BOTTOM)
		self.frame_bot.grid(row=2, column=1)

class MenuBar(tkinter.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config(background="#074E65")
		button_height=2
		button_width=10
		self.button_bot = Button(self, text="Bot", height=button_height, width=button_width)
		self.button_config = Button(self, text="Configurer", height=button_height, width=button_width)
		self.button_market = Button(self, text="Market", height=button_height, width=button_width)

		self.button_bot.grid(row=1, column=1)
		self.button_config.grid(row=1, column=2)
		self.button_market.grid(row=1, column=3)

class PowerButton(tkinter.Canvas):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.height = 50
		self.width = 50
		self.image = ImageTk.Image.open("src/power-button.png")
		self.image = self.image.resize((self.height, self.width), Image.ANTIALIAS)
		self.photo = ImageTk.PhotoImage(self.image)
		self.config(width=self.image.size[0], height=self.image.size[1], bg=color_background, bd=0, highlightthickness=0)
		self.create_image(0, 0, anchor=NW, image=self.photo)
		#self.pack(expand=YES, side=LEFT)



class ChatFrame(tkinter.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config(background=color_background, bd=0, highlightthickness=0)
		self.messages = Text(self)
		self.messages.config(background=color_background,font=("Courrier"),fg="white", state=DISABLED, yscrollcommand=True, bd=0, highlightthickness=0)
		self.input_user = StringVar()
		self.input_field = Entry(self, text=self.input_user)
		self.input_field.bind("<Return>", self.on_entry_press)
		self.messages.pack(expand=YES)
		self.input_field.pack(expand=YES)
		#self.pack(expand=YES)

	def print_message(self, message):
		self.messages.config(state=NORMAL)
		self.messages.insert(INSERT, '%s\n' % "{0} {1}".format(get_now(), message))
		self.messages.config(state=DISABLED)
	def on_entry_press(self, entry):
		global client
		if self.input_field.get() != "":
			if self.input_field.get() == "!stop":
				client.running = False
			else:
				self.print_message(self.input_field.get())
				global discord_messages_to_send
				discord_messages_to_send.append((547098879007522816, self.input_field.get()))
				self.input_user.set("")




def start_client():
	global client
	client.run("NDI0MTkzNjEzMjAzNzY3Mjk3.D0xUFw.qXvDxrqyI34Sn-2uMmOS1MmpfaU")


def init_client():
	global client
	global discord_messages_to_send
	discord_messages_to_send = []
	client = BotPendu()

def stop_client():
	global client
	global window
	window.console.print_message("Déconnexion du bot...")
	client.running = False


def show_window():
	global window
	window = ClientWindow()
	window.mainloop()
thread_window =threading.Thread(target=show_window)
thread_window.start()

init_client()