import discord, json, requests, pymysql.cursors
from discord.ext import commands
from utils import rpc_module, mysql_module, parsing
import math

rpc = rpc_module.Rpc()
mysql = mysql_module.Mysql()


class Withdraw:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def withdraw(self, ctx, address: str, amount: float):
        """あなたのアカウントから任意のアドレスへPhoreを引き出せます"""
        snowflake = ctx.message.author.id
        if amount <= 0.0:
            await self.bot.say("{} **:warning:0以下の枚数を引き出すことは出来ません!:warning:**".format(ctx.message.author.mention))
            return

        abs_amount = abs(amount)
        if math.log10(abs_amount) > 8:
            await self.bot.say(":warning:**不正な枚数です!**:warning:")
            return

        mysql.check_for_user(snowflake)

        conf = rpc.validateaddress(address)
        if not conf["isvalid"]:
            await self.bot.say("{} **:warning:アドレスが正しくありません!:warning:**".format(ctx.message.author.mention))
            return

        ownedByBot = False
        for address_info in rpc.listreceivedbyaddess(0, True):
            if address_info["address"] == address:
                ownedByBot = True
                break

        if ownedByBot:
            await self.bot.say("{} **:warning:このボットの持つアドレスへは送金できません!:warning:** Please use tip instead!".format(ctx.message.author.mention))
            return

        balance = mysql.get_balance(snowflake, check_update=True)
        if float(balance) < amount:
            await self.bot.say("{} **:warning:所持金以上に送金することは出来ません!:warning:**".format(ctx.message.author.mention))
            return

        txid = mysql.create_withdrawal(snowflake, address, amount)
        if txid is None:
            await self.bot.say("{} 十分な枚数を持っているにもかかわらず引き出しが出来ませんでした。サポートへご連絡下さい。".format(ctx.message.author.mention))
        else:
            await self.bot.say("{} **{} PHR 引き出しました! :money_with_wings:**\nトランザクションデータはここから: https://chainz.cryptoid.info/phr/tx.dws?{}.htm".format(ctx.message.author.mention, str(amount), txid))

def setup(bot):
    bot.add_cog(Withdraw(bot))
