import logging

import discord
from discord.ext import commands

from src.util import discordhelper
from src.util.discordhelper import Field


class User(commands.Cog):
    _gw2api = None
    _members = None

    def __init__(self, bot, gw2api_module, members_module):
        self.bot = bot
        self._gw2api = gw2api_module
        self._members = members_module

    @commands.command(
        help='',
        brief=''
    )
    async def token(self, ctx, arg):
        if not isinstance(ctx.channel, discord.DMChannel):
            ctx.message.delete()
            ctx.send("Use private DM to send me token :D", delete_after=60)
            channel = ctx.author.dm_channel
            if channel is None:
                channel = await ctx.author.create_dm()
            await channel.send("Call the command here")

    @commands.command(
        help='Takes account name and if there in the guild add them as a member',
        brief='Adds user to member rank if there in the guild'
    )
    async def new(self, ctx, arg):
        logging.debug('Calling new cmd')
        if self._gw2api.user_in_guild(arg):
            # add role to user
            role = discord.utils.get(ctx.author.guild.roles, name='Member')
            self._members.add_member(ctx.author.id, arg)
            self._members.save_members()
            await ctx.author.add_roles(role)

    @commands.command(
        help='Takes account name and returns users guild information',
        brief='Shows users guild information'
    )
    async def user(self, ctx, arg):
        logging.debug('Calling user cmd')
        info = self._gw2api.user_guild_info(arg)
        if info is None:
            return
        async with ctx.channel.typing():
            embedmsg = discordhelper.embed_msg_builder(title="Users Guild Info",
                                                       thumbnail=info.get_rank_icon(),
                                                       fields=[Field('Name', info.get_name()),
                                                               Field('Rank', info.get_rank()),
                                                               Field('Join Date', info.get_join_date())])
            await ctx.send(embed=embedmsg)
