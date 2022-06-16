import discord
from discord.ext.commands import Cog
from discord import Embed
from discord.ext.commands import command
from aiohttp import request


class Util(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="meme")
    async def meme(self, ctx):
        url = 'https://some-random-api.ml/meme'
        image_url = ''
        caption = ''
        category = ''

        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data["image"]
                embed = Embed(title=data["caption"],
                              description='',
                              colour=ctx.author.color)
                if image_url is not None:
                    embed.set_image(url=image_url)
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} status.")



def setup(bot):
    bot.add_cog(Util(bot))
