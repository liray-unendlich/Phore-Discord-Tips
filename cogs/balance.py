import discord
from discord.ext import commands
from utils import rpc_module, mysql_module

# result_set = database response with parameters from query
# db_bal = nomenclature for result_set["balance"]
# snowflake = snowflake from message context, identical to user in database
# wallet_bal = nomenclature for wallet reponse

rpc = rpc_module.Rpc()
mysql = mysql_module.Mysql()


class Balance:

    def __init__(self, bot):
        self.bot = bot

    async def do_embed(self, name, db_bal, db_bal_unconfirmed):
        # Simple embed function for displaying username and balance
        embed = discord.Embed(colour=0xff0000)
        embed.add_field(name="ユーザー", value=name.mention)
        embed.add_field(name="残高", value="{:.8f} PHR".format(
            round(float(db_bal), 8)))
        if float(db_bal_unconfirmed) != 0.0:
            embed.add_field(name="未確認のデポジット", value="{:.8f} PHR".format(
                round(float(db_bal_unconfirmed), 8)))
        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        """残高を表示します"""
        # Set important variables
        snowflake = ctx.message.author.id

        # Check if user exists in db
        mysql.check_for_user(snowflake)

        balance = mysql.get_balance(snowflake, check_update=True)
        balance_unconfirmed = mysql.get_balance(
            snowflake, check_unconfirmed=True)

        # Execute and return SQL Query
        await self.do_embed(ctx.message.author, balance, balance_unconfirmed)

    @commands.command(pass_context=True)
    async def getbalance(self, addr):
        """指定アドレスの残高を表示します"""
        url = "https://chainz.cryptoid.info/phr/api.dws?q=getbalance&key=625644bccfa9&a="+addr
        try:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    responseRaw = await response.read()
                    priceData = json.loads(responseRaw)[0]
                    embed = discord.Embed(colour=0x00FF00)
                    embed.add_field(name="アドレス", value=addr)
                    embed.add_field(
                        name="残高", value="{}PHR".format(priceData))

                    await self.bot.say(embed=embed)
        except:
            await self.bot.say(":error: データ取得に失敗しました！")

def setup(bot):
    bot.add_cog(Balance(bot))
