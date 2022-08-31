from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord
from discord.ext.commands import Bot as BotBase, CommandNotFound
from ..db import db
from glob import glob
from sys import platform as _platform
from ..bot import configuration

# constants
PREFIX = "$"
OWNER_IDS = [228981959274004480]

#if windows use \\ if ubuntu use / and assume mac os uses the same as ubuntu as I can't check
delimiter = None
#ubuntu
if _platform.startswith('linux'):
    delimiter = "/"
#windows
elif _platform.startswith('win'):
    delimiter = "\\"
#mac
elif _platform.startswith('darwin'):
    delimiter = "/"

COGS = [path.split(delimiter)[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Bot(BotBase):
    def __init__(self):
        # calls init function of botbase
        self.PREFIX = PREFIX
        self.ready = False
        # self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")

    def run(self, version):
        self.VERSION = version

        self.TOKEN = configuration.discordToken
        print("running bot...")
        self.setup()
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, event_method, *args, **kwargs):
        if event_method == "on_command_error":
            # if error type is on_command_error
            await args[0].send("Something went wrong.")

        raise

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            pass
        elif hasattr(exception, "original"):
            raise exception.original
        else:
            raise exception

    async def on_ready(self):
        if not self.ready:
            print("bot ready")
            await bot.change_presence(activity=discord.Game(name="Use $help for commands!"))
            self.ready = True
            self.scheduler.start()

        else:
            print("bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
