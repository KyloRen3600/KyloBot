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
		self.revealed = 0
		i = 0
		while i < len(self.word):
			self.hided.append("-")
			i += 1
		self.used_lifes = 0

	def reveal_letter(self, letter):
		finded = False
		for i, l in enumerate(self.word):
			if l == letter:
				self.hided[i] = letter
				self.revealed += 1
				finded = True
		return finded



def choice_word():
	with open("Addons\\src\\words.txt", "r") as file:
		text = file.read()
		words = text.split()
		return choice(words).lower()

def build_embed(user, channel, color):

	word = games["{0}".format(channel.id)]
	embed = discord.Embed(title="[Pendu]", url="https://www.regles-jeux-plein-air.com/regle-du-pendu/", color=color)
	embed.set_author(name=user.name, icon_url=user.avatar_url)
	if word.used_lifes < 10:
		embed.set_thumbnail(url="https://raw.githubusercontent.com/KyloRen3600/KyloBot/master/Addons/Pendu/pendu-etape0{0}.gif".format(word.used_lifes))
	else:
		embed.set_thumbnail(url="https://raw.githubusercontent.com/KyloRen3600/KyloBot/master/Addons/Pendu/pendu-etape{0}.gif".format(word.used_lifes))
	embed.set_footer(text="Développé par KyloRen3600")
	return embed

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
				try:
					word = games["{0}".format(message.channel.id)]
					embed = build_embed(message.author, message.channel, 0xffff00)
					embed.add_field(name="Partie déjà lancée !", value="Faites \"{0} reveal\" pour abandonner.".format(addon.prefix), inline=True)
					embed.add_field(name=" Mot:", value="".join(word.hided), inline=True)
					await client.send_message(message.channel, embed=embed)
				except:
					word = Word(choice_word())
					window.print_message("[Pendu] Mot: {0}".format(word.word))
					games["{0}".format(message.channel.id)] = word
					embed = build_embed(message.author, message.channel, 0x00ff00)
					embed.add_field(name="Partie lancée", value="Bonne chance !", inline=True)
					embed.add_field(name="Mot:", value="".join(word.hided), inline=True)
					await client.send_message(message.channel, embed=embed)
			if args[1] == "reveal":
				try:
					word = games["{0}".format(message.channel.id)]
					word.used_lifes = 10
					embed = build_embed(message.author, message.channel, 0xff0000)
					embed.add_field(name="Partie terminée", value="Vous avez abandonné", inline=True)
					embed.add_field(name=" Mot:", value=word.word, inline=True)
					del games["{0}".format(message.channel.id)]
					await client.send_message(message.channel, embed=embed)

				except:
					word = Word("Aucun")
					games["{0}".format(message.channel.id)] = Word("Aucun")
					games["{0}".format(message.channel.id)].used_lifes = 11
					embed = build_embed(message.author, message.channel, 0xffff00)
					embed.add_field(name="Aucune partie en cours", value="Faites \"{0} start\" pour commencer.".format(addon.prefix))
					embed.add_field(name=" Mot:", value=word.word)
					del games["{0}".format(message.channel.id)]
					await client.send_message(message.channel, embed=embed)

			elif args[1] == "p" or args[1] == "proposition" :
				try:
					word = games["{0}".format(message.channel.id)]
				except:
					word = Word("Aucun")
					games["{0}".format(message.channel.id)] = Word("Aucun")
					games["{0}".format(message.channel.id)].used_lifes = 11
					embed = build_embed(message.author, message.channel, 0xffff00)
					embed.add_field(name="Aucune partie en cours", value="Faites \"{0} start\" pour commencer.".format(addon.prefix))
					embed.add_field(name=" Mot:", value=word.word)
					del games["{0}".format(message.channel.id)]
					await client.send_message(message.channel, embed=embed)
					return
				try:
					proposal = args[2]
				except:
					embed = build_embed(message.author, message.channel, 0xffff00)
					embed.add_field(name="Veuillez préciser une lettre/un mot !", value="{0} p <mot/lettre>".format(addon.prefix), inline=True)
					embed.add_field(name="Mot:", value="".join(word.hided), inline=True)
					await client.send_message(message.channel, embed=embed)
				else:
					if len(proposal) == 1 and any(proposal in s for s in list(string.ascii_lowercase)):
						if word.reveal_letter(proposal) == True:
							if word.revealed == len(word.word):
								embed = build_embed(message.author, message.channel, 0x00ff00)
								embed.add_field(name="Proposition:", value="{0}\nLettre présente !\nPartie gagnée !".format(args[2].upper()), inline=True)
								embed.add_field(name="Mot:", value="".join(word.word), inline=True)
								await client.send_message(message.channel, embed=embed)
							else:
								embed = build_embed(message.author, message.channel, 0x00ff00)
								embed.add_field(name="Proposition:", value="{0}\nLettre présente !".format(args[2].upper()), inline=True)
								embed.add_field(name="Mot:", value="".join(word.hided), inline=True)
								await client.send_message(message.channel, embed=embed)
						else:
							word.used_lifes += 1
							if word.used_lifes < 10:
								embed = build_embed(message.author, message.channel, 0xff0000)
								embed.add_field(name="Proposition:", value="{0}\nLettre incorrecte...".format(args[2].upper()), inline=True)
								embed.add_field(name="Mot:", value="".join(word.hided), inline=True)
								await client.send_message(message.channel, embed=embed)
							else:
								embed = build_embed(message.author, message.channel, 0xff0000)
								embed.add_field(name="Proposition:", value="{0}\nLettre incorrecte\nPartie perdue...".format(args[2].upper()), inline=True)
								embed.add_field(name="Mot:", value="".join(word.word), inline=True)
								del games["{0}".format(message.channel.id)]
								await client.send_message(message.channel, embed=embed)
					elif len(proposal) != 1:
						if word.word == args[2]:
							embed = build_embed(message.author, message.channel, 0x00ff00)
							embed.add_field(name="Proposition:".format(args[2]), value="{0}\nMot exact !\nPartie gagnée !".format(args[2]), inline=True)
							embed.add_field(name="Mot:", value="".join(word.word), inline=True)
							del games["{0}".format(message.channel.id)]
							await client.send_message(message.channel, embed=embed)
						else:
							word.used_lifes += 1
							if word.used_lifes < 10:
								embed = build_embed(message.author, message.channel, 0xff0000)
								embed.add_field(name="Proposition:".format(args[2]), value="{0}\nMot incorrect...".format(args[2]), inline=True)
								embed.add_field(name="Mot:", value="".join(word.hided), inline=True)
								await client.send_message(message.channel, embed=embed)
							else:
								embed = build_embed(message.author, message.channel, 0xff0000)
								embed.add_field(name="Proposition:".format(args[2]), value="{0}\nMot incorrect\nPartie perdue...".format(args[2]), inline=True)
								embed.add_field(name="Mot:", value="".join(word.word), inline=True)
								del games["{0}".format(message.channel.id)]
								await client.send_message(message.channel, embed=embed)
					elif len(proposal) == 1:
						embed = build_embed(message.author, message.channel, 0xffff00)
						embed.add_field(name="Proposition:".format(args[2]), value="{0}\nCaractère non pris en charge".format(args[2]), inline=True)
						embed.add_field(name="Mot:", value="".join(word.hided), inline=True)
						await client.send_message(message.channel, embed=embed)