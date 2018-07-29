import math
import discord
from discord.ext import commands
from utils import rpc_module, mysql_module, checks, parsing
import random

rpc = rpc_module.Rpc()
mysql = mysql_module.Mysql()


class Soak:
    def __init__(self, bot):
        self.bot = bot
        soak_config = parsing.parse_json('config.json')['soak']
        '''
        soak_max_recipients でsoakに参加できる最大人数を指定します。
        soak_min_received でユーザーごとの受け取るsoakの最小値を指定します。
        soakの参加者数は各種制限により変動します。
        if enabled via use_max_recipients and use_min_received
        '''
        self.soak_max_recipients = soak_config["soak_max_recipients"]
        self.use_max_recipients = soak_config["use_max_recipients"]
        self.soak_min_received = soak_config["soak_min_received"]
        self.use_min_received = soak_config["use_min_received"]

    @commands.command(pass_context=True)
    @commands.check(checks.allow_soak)
    async def soak(self, ctx, amount: float):
        """オンラインのユーザーに投げ銭します"""
        if self.use_max_recipients and self.soak_max_recipients == 0:
            await self.bot.say("**:warning: soakの最大ユーザーが0に設定されています。開発者に連絡し、修正を依頼してください。:warning:**")
            return

        snowflake = ctx.message.author.id

        mysql.check_for_user(snowflake)
        balance = mysql.get_balance(snowflake, check_update=True)

        if float(balance) < amount:
            await self.bot.say("{} **:warning:所持金より多くをsoakすることは出来ません。!:warning:**".format(ctx.message.author.mention))
            return

        online_users = [x for x in ctx.message.server.members if x.status == discord.Status.online]
        if ctx.message.author in online_users:
            online_users.remove(ctx.message.author)

        for user in online_users:
            if user.bot:
                online_users.remove(user)

        if self.use_max_recipients:
            len_receivers = min(len(online_users), self.soak_max_recipients)
        else:
            len_receivers = len(online_users)

        if self.use_min_received:
            len_receivers = min(len_receivers, amount / self.soak_min_received)

        if len_receivers == 0:
            await self.bot.say("{}, you are all alone if you don't include bots! Trying soaking when people are online.".format(ctx.message.author.mention))
            return

        amount_split = math.floor(float(amount) * 1e8 / len_receivers) / 1e8
        if amount_split == 0:
            await self.bot.say("{} **:warning:{} is not enough to split between {} users:warning:**".format(ctx.message.author.mention, amount, len_receivers))
            return

        receivers = []
        for i in range(len_receivers):
            user = random.choice(online_users)
            receivers.append(online_users.remove(user))
            mysql.check_for_user(user.id)
            mysql.add_tip(snowflake, user.id, amount_split)

#        long_soak_msg = "{} ** {} PHR を {} [{}] 人へsoakしました！:money_with_wings:**".format(ctx.message.author.mention, str(amount_split), ', '.join([x.mention for x in receivers]), str(amount))

#        if len(long_soak_msg) > 2000:
        await self.bot.say("{} ** {} PHR を {} ユーザーへsoakしました！ [{}] :money_with_wings:**".format(ctx.message.author.mention, str(amount_split), len_receivers, str(amount)))
#        else:
#            await self.bot.say(long_soak_msg)

    @commands.command()
    async def soak_info(self):
        if self.use_max_recipients:
            st_max_users = str(self.soak_max_recipients)
        else:
            st_max_users = "<disabled>"

        if self.use_min_received:
            st_min_received = str(self.soak_min_received)
        else:
            st_min_received = "<disabled>"

        await self.bot.say("Soak 情報: 最大参加者 {}, 受け取りに必要な枚数 {}".format(st_max_users, st_min_received))

def setup(bot):
    bot.add_cog(Soak(bot))
