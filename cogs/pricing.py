import discord, os
from discord.ext import commands
#from utils import checks, output
from aiohttp import ClientSession
import urllib.request
import json

class Pricing:
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @commands.command()
    async def price(self, amount=1):
        """
        PHRの価格情報を確認できます。
        """
        try:
            async with ClientSession() as session:
                async with session.get("https://api.coinmarketcap.com/v1/ticker/phore/?convert=JPY") as response:
                    responseRaw = await response.read()
                    priceData = json.loads(responseRaw)[0]
                    embed = discord.Embed(colour=0x00FF00)
                    embed.add_field(name="順位", value="{} 位".format(priceData["rank"]))
                    embed.add_field(name="価格(BTC)", value="{} BTC".format(priceData["price_btc"]))
                    embed.add_field(name="価格(JPY)", value="{} JPY".format(priceData["price_jpy"]))
                    embed.add_field(name="流通枚数", value="{} PHR".format((priceData["available_supply"])))
                    await self.bot.say(embed=embed)
        except:
            await self.bot.say(":エラー: 価格情報の取得に失敗しました!")


def setup(bot):
    bot.add_cog(Pricing(bot))
