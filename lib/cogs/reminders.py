from datetime import datetime, timedelta
import time

from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Cog
from discord.ext.commands import command


class Reminders(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminder_objects = []
        self.bot.scheduler.add_job(self.check_reminder,
                                   CronTrigger(day_of_week=None, hour=None, minute=None, second=0))
        # triggers every
        # minute

    @Cog.listener()
    async def on_ready(self):
        pass

    # check if given time is formatted correctly.
    def parsetime(reminder_time):
        try:
            time.strptime(reminder_time, '%H:%M')
            return True
        except ValueError:
            return False

    async def check_reminder(self):
        # Doing this explicitly for readability
        if len(self.reminder_objects) != 0:
            dt = datetime.now()
            current_time = dt.strftime("%H:%M")
            for x in self.reminder_objects[:]:
                if x.reminder_time == current_time:
                    print("correctly reminded")
                    await self.send_reminder(x.author, x.message, x.channel_id)
                else:
                    pass
                    # print("x time is: " + x.reminder_time + " and current time is: " + current_time)

    async def send_reminder(self, ctx_author, ctx_message, ctx_channel_id):
        print('channel id is: ' + str(ctx_channel_id))
        response = f"Hey, {ctx_author.mention} ,You asked for a reminder about: " + ctx_message
        ctx_channel_id = int(ctx_channel_id)
        channel = self.bot.get_channel(ctx_channel_id)

        await channel.send(response)

    # Clears all reminders by an author within ReminderObjects, if they have any
    def clear_reminders(self, ctx_author):
        for x in self.reminder_objects[:]:
            if x.author == ctx_author:
                self.reminder_objects.remove(x)

    @command(name='setreminder', help='Reminds you to do something. Args: Message|Time Note: Time is in %h%m '
                                      'and uses UTC.')
    async def set_reminder(self, ctx, msg, reminder_time):
        author = ctx.message.author
        cid = ctx.message.channel.id
        isvalid = Reminders.parsetime(reminder_time)

        if isvalid:
            response = "Reminding you to do this thing: " + msg + " at:  " + reminder_time + " in this channel."
            reminder_object = ReminderObject(ctx.message.author, msg, reminder_time, cid)
            self.reminder_objects.append(reminder_object)
        else:
            response = "Time not set correctly. Set time in %h%m and use UTC time."

        await ctx.send(response)

    @command(name='clearreminder', help='Clears reminders.')
    async def clear_reminder(self, ctx):
        response = 'Reminders cleared.'
        Reminders.clear_reminders(self, ctx.message.author)
        await ctx.send(response)

    @command(name='checkreminder', help='Checks reminders.')
    async def check_reminders(self, ctx):

        response = 'You have reminders for: '
        for x in self.reminder_objects:
            if x.author == ctx.message.author:
                response += " " + x.message + " at: " + x.reminder_time

        await ctx.send(response)


class ReminderObject:
    author = ''
    message = ''
    reminder_time = ''
    channel_id = ''

    # default constructor
    def __init__(self, ctx_author, ctx_message, ctx_time, ctx_channel):
        self.author = ctx_author
        self.message = ctx_message
        self.reminder_time = ctx_time
        self.channel_id = ctx_channel


def setup(bot):
    bot.add_cog(Reminders(bot))
# bot.scheduler.add_job(...)
