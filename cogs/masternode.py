import discord
from discord.ext import commands
from utils import rpc_module, mysql_module
from datetime import *

#result_set = database response with parameters from query
#db_bal = nomenclature for result_set["balance"]
#snowflake = snowflake from message context, identical to user in database
#wallet_bal = nomenclature for wallet reponse


rpc = rpc_module.Rpc()

JST = timezone(timedelta(hours=+9), 'JST')

class Masternode:

    def __init__(self, bot):
        self.bot = bot

    async def do_embed(self, name, status_data, address, paidtime):
        # Simple embed function for displaying username and balance
        embed = discord.Embed(colour=0xff0000)
        embed.add_field(name="ユーザー", value=name.mention)
        embed.add_field(name="ステータス", value=status_data)
        embed.add_field(name="アドレス", value=address)
        embed.add_field(name="最新支払い日時", value=paidtime)
        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True)
    async def getmnstatus(self, ctx, param):
        """マスターノードの状態を確認"""
        # post listmasternodes to rpc client
        result = rpc.masternodestatus(param)
        status = result['status']
        addr = result['addr']
        lastpaid_time = result['lastpaid']
        last_paid_time = datetime.fromtimestamp(lastpaid_time, JST)


        # Execute and return SQL Query
        await self.do_embed(ctx.message.author, status, addr, last_paid_time)

def setup(bot):
    bot.add_cog(Masternode(bot))