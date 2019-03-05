from discord.ext import commands

bot = commands.Bot('.')

@bot.event
async def on_message(msg):
    print("in on_message #1")
    await bot.process_commands(msg)  # so `Command` instances will still get called


@bot.listen()
async def on_message(msg):
    print("in on_message #2")


@bot.listen()
async def on_message(msg):
    print("in on_message #3")

bot.run("NDI0MTkzNjEzMjAzNzY3Mjk3.D0xUFw.qXvDxrqyI34Sn-2uMmOS1MmpfaU")