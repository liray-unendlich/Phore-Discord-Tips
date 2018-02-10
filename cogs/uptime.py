import discord, datetime, time
from discord.ext import commands

start_time = time.time()

class Uptime:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uptime(self):
        """
        ボットの稼働時間を確認できます。
        """
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xFF0000)
        embed.add_field(name="稼働時間", value=text)
        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say("現在の稼働時間: " + text)


def setup(bot):
    bot.add_cog(Uptime(bot))
