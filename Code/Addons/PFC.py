from KyloBot import *
from Addon import *
from random import choice
import discord
from discord import *

def build_embed(message, color):
	embed = discord.Embed(title="[PFC]", color=color)
	embed.set_thumbnail(url="https://github.com/KyloRen3600/KyloBot/blob/master/Addons/PFC/PFC.jpg?raw=true")
	embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
	embed.set_footer(text="Développé par KyloRen3600")
	return embed

def play(message, item):
	item = item.lower()

	choices = ["Pierre", "Feuille", "Ciseaux"]
	i = choice(choices)

	if item == "feuille" or item == "f":
		item = "Feuille"
		if i == "Pierre":
			win = True
		elif i == "Feuille":
			win = 3
		elif i == "Ciseaux":
			win = False

	elif item == "pierre" or item == "p":
		item = "Pierre"
		if i == "Pierre":
			win = 3
		elif i == "Feuille":
			win = False
		elif i == "Ciseaux":
			win = True

	elif item == "ciseaux" or item == "c":
		item = "Ciseaux"
		if i == "Pierre":
			win = False
		elif i == "Feuille":
			win = True
		elif i == "Ciseaux":
			win = 3

	if win == True:
		embed = build_embed(message, 0x00ff00)
		embed.add_field(name="Attaque:",value=item, inline=True)
		embed.add_field(name="Bot:",value=i, inline=True)
		embed.add_field(name="Résultat:",value="Vous avez gagné !", inline=True)

	elif win == False:
		embed = build_embed(message, 0xff0000)
		embed.add_field(name="Attaque:",value=item, inline=True)
		embed.add_field(name="Bot:",value=i, inline=True)
		embed.add_field(name="Résultat:",value="Vous avez perdu...", inline=True)
	elif win == 3:
		embed = build_embed(message, 0xffff00)
		embed.add_field(name="Attaque:",value=item, inline=True)
		embed.add_field(name="Bot:",value=i, inline=True)
		embed.add_field(name="Résultat:",value="Égalité.", inline=True)
	return embed






def init(window, client, addon):
	window.print_message("[PFC] Chargement réussi !")
	window.print_message("[PFC] Version: {0}".format(addon.version))

	@client.listen()
	async def on_message(message):
		args = message.content.split(" ")
		cmd_args = ["pierre", "p", "feuille", "f", "ciseaux", "c"]
		if message.content.startswith(addon.prefix):
		#	attack = args[1].lower()
		#	embed = play(message, args[1])
		#	await client.send_message(message.channel, embed=embed)
			try:
				attack = args[1].lower()
				embed = play(message, args[1])
				await client.send_message(message.channel, embed=embed)

			except Exception as E:
				print(E)
				embed = build_embed(message, 0xffff00)
				embed.add_field(name="Veuillez proposer une attaque !", value="Utilisation: \"{0} <p/f/c>\".".format(addon.prefix))
				await client.send_message(message.channel, embed=embed)

