import discord, os, itertools
from discord.ext import commands
from utils import parsing, checks, mysql_module

mysql = mysql_module.Mysql()


class Server:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    @commands.check(checks.in_server)
    @commands.check(checks.is_owner)
    async def allowsoak(self, ctx, enable: bool):
        """
        サーバー上のユーザーに対してsoakを利用可能に
        """
        mysql.set_soak(ctx.message.server, int(enable))
        if enable:
            await self.bot.say("Soakは現在利用可能です。")
        else:
            await self.bot.say("Soakは現在利用できません。")

    @commands.command(pass_context=True)
    @commands.check(checks.in_server)
    @commands.check(checks.is_owner)
    async def checksoak(self, ctx):
        """
        サーバー上でsoakが利用可能かチェック
        """
        result_set = mysql.check_soak(ctx.message.server)
        if result_set:
            await self.bot.say("Soakは利用可能です。")
        else:
            await self.bot.say("Soakは利用できません。")


def setup(bot):
    bot.add_cog(Server(bot))
