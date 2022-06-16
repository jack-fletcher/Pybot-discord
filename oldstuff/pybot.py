# #imports
# import discord
# import config
#
# from discord.ext import commands
#
# bot = commands.Bot(command_prefix=config.prefix)
#
# @bot.event
# async def on_ready():
#
#     print(config.welcomeMessage)
#     print('Logged in as')
#     print(bot.user.name)
#     activity = discord.Game(name="with Python")
#     await bot.change_presence(status=discord.Status.idle, activity=activity)
# #Load command cogs
# # bot.load_extension("commands/Greetings")
# # bot.load_extension("commands/Reminders")
#
# #Load discord token
# bot.run(config.discordToken)
