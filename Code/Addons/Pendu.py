from KyloBot import *
from Addon import *
import asyncio
from random import choice
import string
import discord
from discord import *

class Word():
	def __init__(self, word):
		self.word = word
		self.hided = []
		i = 0
		while i < len(self.word):
			self.hided.append("-")
			i += 1

def choice_word():
	with open("Addons\\src\\words.txt", "r") as file:
		text = file.read()
		words = text.split()
		return choice(words).lower()

def build_embed(user):
	embed = discord.Embed(title="[Pendu]", url="https://www.regles-jeux-plein-air.com/regle-du-pendu/")
	embed.set_author(name=user.name, icon_url=user.avatar_url)
	embed.set_thumbnail(url="https://storenotrefamilleprod.blob.core.windows.net/images/cms/nouveausite_nf/ressources/images/jeux/pendu/pendu-etape00.gif")
	embed.add_field(name="Partie lancée", value="Bonne chance !", inline=True)
	embed.add_field(name="Mot:", value="".join(word.hided), inline=True)
	embed.set_footer(text="Développé par KyloRen3600")

def init(window, client, addon):
	window.print_message("[Pendu] Chargement réussi !")
	window.print_message("[Pendu] Version: {0}".format(addon.version))

	global games
	games = {}


	@client.listen()
	async def on_message(message):
		args = message.content.split(" ")

		if message.content.startswith(addon.prefix):
			if args[1] == "start":
					word = Word(choice_word())
					window.print_message("[Pendu] Mot: {0}".format(word.word))
					games["{0}".format(message.channel.id)] = word
					embed = discord.Embed(title="[Pendu]", url="https://www.regles-jeux-plein-air.com/regle-du-pendu/")
					embed.set_author(name=message.author.name, icon_url = message.author.avatar_url)
					embed.set_thumbnail(url="https://storenotrefamilleprod.blob.core.windows.net/images/cms/nouveausite_nf/ressources/images/jeux/pendu/pendu-etape00.gif")
					embed.add_field(name="Partie lancée", value = "Bonne chance !", inline = True)
					embed.add_field(name="Mot:", value = "".join(word.hided), inline = True)
					embed.set_footer(text="Développé par KyloRen3600")
					await client.send_message(message.channel, embed=embed)


			if args[1] == "reveal":
				try:
					await client.send_message(message.channel, "[Pendu] Le mot était {0}".format(games["{0}".format(message.channel.id)].word))

				except:
					await client.send_message(message.channel, "[Pendu] Aucune partie démarrée !")

			if args[1] == "l" or args[1] == "lettre":
				try:
					word = games["{0}".format(message.channel.id)]
				except:
					await client.send_message(message.channel, "[Pendu] Veuillez démarrer une partie en faisant \"{0} start\" !".format(addon.prefix))
					return
				try:
					letter = args[2]
				except:
					await client.send_message(message.channel, "[Pendu] Veuillez préciser une lettre {0} !".format(message.author.mention))
				else:
					if len(letter) == 1 and any(letter in s for s in list(string.ascii_lowercase)):
						await client.send_message(message.channel, "[Pendu] {0} propose la lettre {1}...\nCette lettre est dans le mot !".format(message.author.mention, args[2]))
					else:
						await client.send_message(message.channel, "[Pendu] Veuillez préciser une lettre {0} !".format(message.author.mention))
