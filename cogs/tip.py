import discord, json, requests, pymysql.cursors
from discord.ext import commands
from utils import rpc_module, mysql_module, parsing, checks

rpc = rpc_module.Rpc()
mysql = mysql_module.Mysql()


class Tip:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.check(checks.in_server)
    async def tip(self, ctx, user:discord.Member, amount:float):
        """ユーザーに対してtipをします。"""
        snowflake = ctx.message.author.id

        tip_user = user.id
        if snowflake == tip_user:
            await self.bot.say("{} **:warning:自分にtipすることは出来ません!:warning:**".format(ctx.message.author.mention))
            return

        if amount <= 0.0:
            await self.bot.say("{} **:warning:0以下の枚数をtipすることは出来ません!:warning:**".format(ctx.message.author.mention))
            return

        mysql.check_for_user(snowflake)
        mysql.check_for_user(tip_user)

        balance = mysql.get_balance(snowflake, check_update=True)

        if float(balance) < amount:
            await self.bot.say("{} **:warning:所持金より多くtipすることは出来ません!:warning:**".format(ctx.message.author.mention))
        else:
            mysql.add_tip(snowflake, tip_user, amount)
            await self.bot.say("{} **{} へ {} PHR をtipしました! :money_with_wings:**".format(ctx.message.author.mention, user.mention, str(amount)))

def setup(bot):
    bot.add_cog(Tip(bot))
