import logging
import discord
from discord.ext import commands


class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help='Shutdown, for owner use only'
    )
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.close()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name='Wash Your Hands'))
        logging.info('We have logged in as {0.user}'.format(self.bot))
