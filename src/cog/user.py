#!/usr/bin/env python3.7

import logging
import discord
from discord.ext import commands
from src.util import discordhelper, gw2api
from src.util.discordhelper import Field
import src.database.user as us


class User(commands.Cog):
    _gw2api = None
    _members = None
    _user = None

    def __init__(self, bot, database, gw2api_module, members_module):
        self.bot = bot
        self._user = us.User(database)
        self._gw2api = gw2api_module
        self._members = members_module

    # TODO: Finalising
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
        if gw2api.check_token(arg):
            self._user.create_user(discord_id=ctx.author.id, token=arg)
            ctx.send("Token added to user {}".format(ctx.author.name), delete_after=60)

    # TODO: db Rework
    @commands.command(
        help='Takes account name and returns users guild information',
        brief='Shows users guild information'
    )
    async def user(self, ctx):
        logging.debug('Calling user cmd')
        user = self._user.get_user(ctx.author.id)
        if not len(user) == 1:
            return
        info = self._gw2api.user_guild_info(user[0][0])
        if info is None:
            return
        async with ctx.channel.typing():
            embedmsg = discordhelper.embed_msg_builder(title="Users Guild Info",
                                                       thumbnail=info.get_rank_icon(),
                                                       fields=[Field('Name', info.get_name()),
                                                               Field('Rank', info.get_rank()),
                                                               Field('Join Date', info.get_join_date())])
            await ctx.send(embed=embedmsg)
