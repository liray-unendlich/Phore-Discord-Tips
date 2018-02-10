import discord, os
from discord.ext import commands
from utils import checks, output
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
        headers={"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"}
        try:
            async with ClientSession() as session:
                async with session.get("https://api.coinmarketcap.com/v1/ticker/") as response:
                    responseRaw = await response.read()
                    priceData = json.loads(responseRaw)['phore']
                    embed = discord.Embed(colour=0x00FF00)
                    embed.add_field(name="24h-Volume USD", value="{} USD".format(priceData['24h_volume_usd']))
                    embed.add_field(name="marketcap USD", value="{} USD".format(priceData['market_cap_usd']))
                    embed.add_field(name="price_BTC", value="{} BTC".format(priceData['price_btc']))
                    embed.add_field(name="price-JPY", value="{} JPY".format((priceData['price_jpy'])))
                    await self.bot.say(embed=embed)
        except:
            await self.bot.say(":エラー: 価格情報の取得に失敗しました!")


def setup(bot):
    bot.add_cog(Pricing(bot))
