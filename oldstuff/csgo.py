import urllib
import requests
from bs4 import BeautifulSoup
from discord.ext.commands import Cog, command


class CSGO(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        pass

    # TODO CSGOStash web scrape
    @command(name='csgostash', help='Scrapes csgostash for an item price. //TODO')
    async def csgostash(self, ctx, gun: str, skin: str):
        query = f"csgostash {gun} + {skin}"
        query.replace(' ', '+')
        URL = f"https://google.com/search?q={query}"

        # desktop user agent
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        # mobile user agent
        MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")

            results = []
            for g in soup.find_all('div', class_='r'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    title = g.find('h3').text
                    item = {
                        "title": title,
                        "link": link
                    }
                    results.append(item)
                    # gets the link to the first result page
            stashURL = (results[0]["link"])
        # start scraping the csgostash page
        page = requests.get(stashURL)
        # get the page html
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            # get the parent of the span class that holds content
            searchQuery = soup.find_all("a", {"class": "btn btn-default btn-sm market-button-skin"})

            queryChildren = searchQuery[0].findChildren("span")

            for child in queryChildren:
                print(child)


def setup(bot):
    bot.add_cog(CSGO(bot))
