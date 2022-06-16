import datetime
import json
import os
from datetime import date

import requests
from apscheduler.triggers.cron import CronTrigger
from bs4 import BeautifulSoup
from dateutil.parser import parse
from discord import Embed
from discord.ext.commands import Cog, command
from ..db import db


class Runescape(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.scheduler.add_job(self.DailyDiscordGains, CronTrigger(hour=0, minute=30, second=0))

    @Cog.listener()
    async def on_ready(self):
        pass

    # def LoadVis(self):
    #     cwd = os.getcwd()
    #     path = cwd + '/data/appdata/preferences.json'
    #
    #     with open(path) as f:
    #         data = json.load(f)
    #
    #         url = data['visurl']
    #         url = url.strip("'")
    #         return url

    # @command(name='vis', help='Gives viswax combo for the current day, scraped from the forum page.')
    # async def vis(self, ctx):
    # # collect web page
    # self.LoadVis()
    # print(self.visurl)
    #
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # page = requests.get(self.visurl, headers=headers)
    # # create bs object
    # soup = BeautifulSoup(page.text, "html.parser")
    # print(soup.get_text())
    # # get the time the post was last edited
    # data = soup.find("p", class_="forum-post__time-below")
    #
    # # data = data.get_text()
    # # print(data.get_text())
    # # this gives:
    # # 19 - Apr - 2018
    # # 13: 48:50
    # # - Last
    # # edited
    # # on
    # # 27 - Jun - 2020
    # # 01: 20:53
    # # by
    # # Tiamat Rider
    #
    # # we only care about the date so only get span info for the first one
    # children = data.find("span", recursive=False)
    #
    # # this should give date e.g 27-jun-2020 01:20:54
    # # we only want the first part, 27-jun-2020
    #
    # # make it into a string so we can delimit it
    # children = children.get_text()
    # # delimit it by the space
    # children_array = children.split(" ")
    # children = children_array[0]
    #
    # # print(children)
    #
    # date = "Vis wax for: " + children
    #
    # # get rune data
    # quote_parent = soup.find("span", class_="quote")
    # # remove unwanted tags
    # for child in quote_parent.find_all():
    #     child.decompose()
    # # this gives the runes plus some random trash at the end
    # s = quote_parent.get_text()
    #
    # # split by the -
    # array = s.split("-")
    #
    # # this should give an array like:
    # # - cosmic (alternatives...)
    # # - chaos (alternatives...)
    # # - smoke (alternatives...)
    # #  - chaos (alternatives...)
    #
    # # this is in the format:
    # # first rune
    # # second rune(s)
    #
    # # third slot is random.
    #
    # first_rune = array[1]
    # second_rune = array[2] + "\r\n" + array[3] + "\r\n" + array[4]
    #
    # # print (first_rune)
    # # print (second_rune)
    #
    # # create embedbuilder
    # embed = Embed(title="Runescape Vis Wax", description=date,
    #               colour=0xFF0000, timestamp=datetime.utcnow())
    # fields = [("Name", "Rune", True),
    #           ("First Rune: ", first_rune, True),
    #           ("Second Rune: ", second_rune, True)]
    # for name, Rune, inline in fields:
    #     embed.add_field(name=name, value=Rune, inline=inline)
    #
    # await ctx.send(embed=embed)
    # await ctx.send('Exception thrown: Not yet implemented. Jagex changed their forum protection which made this implementation obselete.')

    # @command(name='updatevis', help='Updates the vis wax URL until next restart.')
    # async def updatevis(self, ctx, msg):
    #     # self.visurl = msg
    #     url = msg
    #     cwd = os.getcwd()
    #     print(url)
    #     path = cwd + '/data/appdata/preferences.json'
    #     with open(path, "r+") as f:
    #         data = json.load(f)
    #
    #         data['visurl'] = url
    #
    #         f.seek(0)
    #         json.dump(data, f)
    #         f.truncate()
    #         print(data["visurl"])
    #         self.visurl = self.LoadVis()
    #     await ctx.send('vis wax url changed.')

    @command(name='daily', help='daily exp gains for your Discord servers clan')
    async def DailyClanGains(self, ctx):
        clan = db.record("SELECT ClanName from ClanURLS WHERE DiscordID = (?)", ctx.guild.id)
        if clan is not None:
            clan = clan[0].replace(" ", "_")
            URL = f'http://www.runeclan.com/clan/{clan}/xp-tracker'

            page = requests.get(URL)
            soup = BeautifulSoup(page.text, "lxml")

            # gets the first table
            table = soup.find("td", class_="clan_right")
            # gets the table holding the data
            table = table.find("table", class_="regular")
            # get all headings of table
            headings = []

            for th in table.find_all("th"):
                # remove any newlines and extra spaces from left and right
                headings.append(th.text.replace('\n', ' ').strip())

            # print(headings)

            desc = [""]
            counter = 0
            for td in table.find_all("td"):
                if not len(td.text) == 0:
                    # remove any newlines and extra spaces from left and right
                    desc.append(td.text.replace('\n', ' ').strip())
                    # print(desc)

            # print (desc)

            # getting the padright amount by getting the size of the largest string in headings and elements
            largest_string_size = 12

            for element in headings:
                if len(element) > largest_string_size:
                    largest_string_size = len(element)
                    # print(f"largest size changed to: {element} at length: {int(largest_string_size)}")
            for element in desc:
                if len(element) > largest_string_size:
                    largest_string_size = len(element)
                    # print(f"largest size changed to: {element} at length: {int(largest_string_size)}")
            new_response = "```"

            for element in headings:
                new_element = element.ljust(largest_string_size) + " | "
                # print(new_element)
                new_response += new_element
            new_response += "\n"
            # print(new_response)
            counter = 0

            for element in desc:
                if not element.isspace() or element == "\n" or element == "":
                    new_element = element.ljust(largest_string_size) + " | "
                    # print(new_element)
                    new_response += new_element
                    counter = counter + 1
                    if counter == 5:
                        new_response += "\n"
                        counter = 0

            new_response += "```"

            # print(new_response)
            # forming a response
            await ctx.send(f"Daily gains for {clan}...")
            await ctx.send(new_response)
        else:
            await ctx.send("You have not yet chosen a clan. Please use $setclaninfo.")

    @command(name='subscribe', help='Subscribes to daily clan information.')
    async def subscribe_to_clan_info(self, ctx):
        db.record("UPDATE ClanURLS SET ShowDaily = 'Yes' WHERE DiscordID = (?)", ctx.guild.id)
        await ctx.send("Subscription added!")

    @command(name='unsubscribe', help='Unsubscribes to daily clan information.')
    async def unsubscribe_to_clan_info(self, ctx):
        db.record("UPDATE ClanURLS SET ShowDaily = 'No' WHERE DiscordID = (?)", ctx.guild.id)
        await ctx.send("Subscription removed!")

    @command(name='setclaninfo', help='Sets the clan name and channel for providing clan information')
    async def StoreClanInformation(self, ctx, *, target=None):
        if target is not None:
            db.record("INSERT OR REPLACE INTO ClanURLS VALUES (?, ?, ?, 'No')", ctx.guild.id, ctx.channel.id, target)
            await ctx.send("Clan Added! Please run $subscribe to get daily notifications in this channel.")
        else:
            await ctx.send("Please choose a clan to target.")

    @command(name='removeclaninfo', help='Removes the clan name and channel for providing clan information')
    async def RemoveClanInformation(self, ctx):
        print(ctx.guild.id)
        db.record("DELETE FROM ClanURLS WHERE DiscordID = (?)", ctx.guild.id)
        await ctx.send("Clan Removed!")

    async def DailyDiscordGains(self):
        clans = db.records("SELECT * FROM ClanURLS WHERE ShowDaily = 'Yes'")
        for clan in clans:
            print(clan[2])
            c = clan[2].replace(" ", "_")
            URL = f'http://www.runeclan.com/clan/{c}/xp-tracker'

            page = requests.get(URL)
            soup = BeautifulSoup(page.text, "lxml")

            # gets the first table
            table = soup.find("td", class_="clan_right")
            # gets the table holding the data
            table = table.find("table", class_="regular")
            # get all headings of table
            headings = []

            for th in table.find_all("th"):
                # remove any newlines and extra spaces from left and right
                headings.append(th.text.replace('\n', ' ').strip())

            desc = [""]
            counter = 0
            for td in table.find_all("td"):
                if not len(td.text) == 0:
                    # remove any newlines and extra spaces from left and right
                    desc.append(td.text.replace('\n', ' ').strip())
                    # print(desc)

            # getting the padright amount by getting the size of the largest string in headings and elements
            largest_string_size = 12

            for element in headings:
                if len(element) > largest_string_size:
                    largest_string_size = len(element)
                    # print(f"largest size changed to: {element} at length: {int(largest_string_size)}")
            for element in desc:
                if len(element) > largest_string_size:
                    largest_string_size = len(element)
                    # print(f"largest size changed to: {element} at length: {int(largest_string_size)}")
            new_response = "```"

            for element in headings:
                new_element = element.ljust(largest_string_size) + " | "
                # print(new_element)
                new_response += new_element
            new_response += "\n"
            # print(new_response)
            counter = 0

            for element in desc:
                if not element.isspace() or element == "\n" or element == "":
                    new_element = element.ljust(largest_string_size) + " | "
                    # print(new_element)
                    new_response += new_element
                    counter = counter + 1
                    if counter == 5:
                        new_response += "\n"
                        counter = 0

            new_response += "```"

            # print(new_response)
            # forming a response
            channel = self.bot.get_channel(clan[1])
            await channel.send(f"Daily gains for {clan[2]}...")
            await channel.send(new_response)

    @command(name='Merch', aliases=['merch'], help='Gets todays merch stock.')
    async def Merch(self, ctx):
        response = requests.get('https://api.weirdgloop.org/runescape/tms/current')

        if response.status_code == 200:
            resp = response.json()
            embed = Embed()
            embed.title = "Travelling Merchant Stock - Today"
            embed.description = "{} \n {} \n {} \n {}".format(resp[0], resp[1], resp[2], resp[3])
            embed.set_footer(text=str(date.today()))
            await ctx.send(embed=embed)
        elif response.status_code == 404:
            await ctx.send('Something went wrong. 404 Not found.')

    @command(name='Baks', aliases=['baks', 'bloods', 'bloodwood', 'Bloodwoods'],
             help='Gives bloodwood tree locations')
    async def baks(self, ctx):
        msg = ""
        msg += "[1. South of the Pirates' Hideout (Single-way area)](https://imgur.com/a/QrWaqRq) \n"
        msg += "[2. North-east of the Demonic Ruins (Multi-way area)](https://i.imgur.com/sowggJQ.png) \n"
        msg += "[3. Next to the Chaos Temple (multi-way area)](https://i.imgur.com/UgpTIUN.png) \n"
        msg += "[4. In the Manor Farm (requires 225,000 Farming reputation)](https://i.imgur.com/EMDzJY6.png) \n"
        msg += "[5. Soul Wars (after Nomad's Requiem)](https://i.imgur.com/zganVp2.png) \n"
        msg += "[6. Ritual Plateau (after Ritual of the Mahjarrat) (Outside Glacor Cave Fairy Ring DKQ)](https://i.imgur.com/A2PQmiM.png) \n"
        msg += "[7. Near the Darkmeyer Arboretum (after The Branches of Darkmeyer)](https://i.imgur.com/1x5BGJm.png) \n"
        msg += "[8. In the Gorajo resource dungeon in Prifddinas (after Plague's End and level 95 Dungeoneering)](https://i.imgur.com/KyH5h4V.png) \n"
        embed = Embed()
        embed.description = msg
        await ctx.send(embed=embed)

    @command(name="alog", aliases=["log"], help="username|rsn - Shows user adventurer log for yourself, or another user.")
    async def display_adventurer_log(self, ctx, *, target=None):
        if target is None:
            target = ctx.message.author.id

            username = db.record("SELECT Username FROM UserGains WHERE UserID = ?", target)
            if username is not None:
                username = username[0]
                user = username.replace(" ", "+")
        elif target is not None:
            username = target
            user = target.replace(" ", "+")
        if username is not None:

            URL = f"https://apps.runescape.com/runemetrics/profile/profile?user={user}&activities=20"
            response = requests.get(URL)
            if response.status_code == 200:
                resp = response.json()
                if resp.get('error') is not None:
                    await ctx.send("This profile is private. Please set this to public and try again.")
                else:
                    desc = "```"
                    for element in resp.get('activities'):
                        desc += f"[{element['date']}] {element['text']}\n"
                    desc += "```"
                    res = requests.get(f"http://secure.runescape.com/m=avatar-rs/{username}/chat.png")
                    redirectedUrl = res.url
                    embed = Embed()
                    embed.title = f"{username}'s Adventurer Log"
                    embed.url = URL
                    embed.set_thumbnail(url=redirectedUrl)
                    embed.description = desc
                    embed.set_footer(text=str(date.today()))
                    await ctx.send(embed=embed)
            elif response.status_code == 404:
                await ctx.send('Something went wrong. 404 Not found.')
        else:
            await ctx.send("You are not currently being tracked by Pybot. Please add your username using $setrsn.")

    @command(name="setgainz", aliases=["setrsn", "changersn"], help="username|rsn - Sets your username for related Runescape Info functions.")
    async def set_gainz_username(self, ctx, *, username=None):
        if username is None:
            await ctx.send("Please add your username to the command.")
        else:
            print(username)
            db.record("INSERT OR REPLACE INTO UserGains VALUES (?, ?)", ctx.message.author.id, username)
            await ctx.send("Username changed.")

    @command(name="gainz", aliases=["gains"], help="username|rsn - gets your current experience gain today, or a target username's.")
    async def display_gainz(self, ctx, *, target=None):
        if target is None:
            target = ctx.message.author.id

            username = db.record("SELECT Username FROM UserGains WHERE UserID = ?", target)
            if username is not None:
                username = username[0].replace(" ", "+")
        elif target is not None:
            username = target.replace(" ", "+")
        if username is not None:
            URL = f"https://www.runeclan.com/user/{username}"
            print(URL)
            page = requests.get(URL)
            soup = BeautifulSoup(page.text, "lxml")
            table = soup.find("table", class_="regular")
            headings = []
            desc = []
            for tr in table.find_all("tr"):
                thCounter = 0
                tdCounter = 0
                for th in tr.find_all("th"):
                    if (3 < thCounter <= 6) or thCounter == 0:
                        text = th.text.strip()
                        text = text.replace("DXP Live", "")
                        headings.append(text)
                    thCounter += 1
                for td in tr.find_all("td"):
                    if (3 < tdCounter <= 6) or tdCounter == 0:
                        desc.append(td.text.strip())
                    tdCounter += 1

            # getting the padright amount by getting the size of the largest string in headings and elements
            largest_string_size = 8

            for element in headings:
                if len(element) > largest_string_size:
                    largest_string_size = len(element)
                    # print(f"largest size changed to: {element} at length: {int(largest_string_size)}")
            for element in desc:
                if len(element) > largest_string_size:
                    largest_string_size = len(element)
                    # print(f"largest size changed to: {element} at length: {int(largest_string_size)}")
            new_response = "```"
            for element in headings:
                new_element = element.ljust(13) + " | "
                # print(new_element)
                new_response += new_element
            new_response += "\n"
            # print(new_response)
            counter = 0

            for element in desc:
                if not element.isspace() or element == "\n" or element == "":
                    new_element = element.ljust(13) + " | "
                    # print(new_element)
                    new_response += new_element
                    counter = counter + 1
                    if counter == 4:
                        new_response += "\n"
                        counter = 0

            new_response += "```"
            await ctx.send(new_response)
        else:
            await ctx.send("You are not currently being tracked by Pybot. Please add your username using $setrsn.")

    @command(name="invite", help="Shows the bot's invite link.")
    async def invite_bot(self, ctx):
        embed = Embed()
        embed.title = "Invite Link for Pybot"
        embed.description = "A Runescape Companion bot"
        embed.url = "https://discord.com/api/oauth2/authorize?client_id=725832497035739170&permissions=137439267840&scope=bot"
        embed.set_footer(text=str(date.today()))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Runescape(bot))
