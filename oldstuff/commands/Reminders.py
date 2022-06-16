# import discord
# import asyncio
# from datetime import datetime, timedelta
# from discord.ext import commands
# import time
# import sched
# import threading
#
#
# class Reminders(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.ReminderObjects = []
#         self.bot.loop.create_task(self.CheckReminder())
#
#     def ParseTime(rTime):
#         try:
#             time.strptime(rTime, '%H:%M')
#             return True
#         except ValueError:
#             return False
#
#     async def CheckReminder(self):
#
#         print('checkreminder debug')
#         while True:
#             print('checkreminder 2')
#
#             await asyncio.sleep(5) #check every this number of seconds
#             print('checkreminder debug3')
#
#             dt = datetime.now()
#             currentTime = dt.strftime("%H:%M")
#             for x in self.ReminderObjects[:]:
#              if x.rTime == currentTime:
#                 print("correctly reminded")
#                 await self.SendReminder(x.author, x.message, x.channelId)
#              else:
#                 print("x time is: " + x.rTime + " and current time is: " + currentTime)
#
#     async def SendReminder(self, ctxAuthor, ctxMessage, ctxChannelId):
#         print('channel id is: ' + str(ctxChannelId))
#         response = "Hey! You asked for a reminder about: " + ctxMessage
#         bot = commands.Bot(command_prefix='$')
#         ctxChannelId = int(ctxChannelId)
#         channel = bot.get_channel(ctxChannelId)
#         await channel.send(response)
#     # Clears all reminders by an author within ReminderObjects, if they have any
#     def ClearReminders(self, ctxAuthor):
#         for x in self.ReminderObjects[:]:
#             if x.author == ctxAuthor:
#                 self.ReminderObjects.remove(x)
#
#     @commands.command(name='setreminder', help='Reminds you to do something. Args: Message|Time Note: Time is in %h%m '
#                                                'and uses UTC.')
#     async def SetReminder(self, ctx, msg, rTime):
#         author = ctx.message.author
#         isValid = Reminders.ParseTime(rTime)
#         if isValid == True:
#             response = "Reminding you to do this thing: " + msg + " at:  " + rTime + " in this channel. id: " + str(ctx.message.channel.id)
#             reminderObject = ReminderObject(ctx.message.author, msg, rTime, ctx.message.channel.id)
#             self.ReminderObjects.append(reminderObject)
#         else:
#             response = "Time not set correctly. Set time in %h%m and use UTC time."
#
#         await ctx.send(response)
#
#     @commands.command(name='clearreminder', help='Clears reminders.')
#     async def ClearReminder(self, ctx):
#         response = 'Reminders cleared.'
#         Reminders.ClearReminders(self, ctx.message.author)
#         await ctx.send(response)
#
#     @commands.command(name='checkreminder', help='Checks reminders.')
#     async def CheckReminders(self, ctx):
#
#         response = 'You have reminders for: '
#         for x in self.ReminderObjects:
#             if x.author == ctx.message.author:
#                 response += " " + x.message + " at: " + x.rTime
#
#         await ctx.send(response)
#
#
# class ReminderObject():
#     author = ''
#     message = ''
#     rTime = ''
#     channelId = ''
#
#     # default constructor
#     def __init__(self, ctxAuthor, ctxMessage, ctxTime, ctxChannel):
#         self.author = ctxAuthor
#         self.message = ctxMessage
#         self.rTime = ctxTime
#         self.channelId = ctxChannel
#
#
# def setup(bot):
#     bot.add_cog(Reminders(bot))
