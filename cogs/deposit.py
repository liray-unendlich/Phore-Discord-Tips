import discord, json, requests
from discord.ext import commands
from utils import parsing, mysql_module

mysql = mysql_module.Mysql()

class Deposit:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def deposit(self, ctx):
        """預け入れアドレスを表示します"""
        user = ctx.message.author
        # Check if user exists in db
        mysql.check_for_user(user.id)
        user_addy = mysql.get_address(user.id)
        await self.bot.send_message(user, user.mention + "'のデポジットアドレス: `" + str(user_addy) + "`" + "\n\n!balance を入力し残高を確認してください。同期は即座に行われるわけではないので、少々お待ちください。")
        if ctx.message.server is not None:
            await self.bot.say("{}, PMでアドレスを送信しました。このボットから送られたアドレスかご確認ください！".format(user.mention))

def setup(bot):
    bot.add_cog(Deposit(bot))
