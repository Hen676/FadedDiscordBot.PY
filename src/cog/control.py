#!/usr/bin/env python3.7

import logging
import discord
from discord.ext import commands
import src.database.shard as sh
import src.database.user as us


class Control(commands.Cog):
    _shard = None
    _user = None

    def __init__(self, bot, database):
        self.bot = bot
        self._shard = sh.Shard(database)
        self._user = us.User(database)

    @commands.command(
        hidden=True
    )
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.close()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self._shard.create_shard(guild.id, guild.owner_id)

    # TODO: add listener for owner change.

    @commands.command(
        description="Server setup",
        help="""Takes two parameters, 1st type of data you want to add to your bot. 
         Command only works in private chat with the server owner.
         2nd the value of that data.
         Example: g!setup motdchannel 📅motd"""
    )
    async def setup(self, ctx, *args):
        if ctx.guild is None:
            return
        if not len(args) == 2:
            ctx.send("{} arguments found needs 2".format(len(args)), delete_after=30)
            return
        if not ctx.author.id == ctx.guild.owner_id:
            ctx.send("cmd for server owner only", delete_after=30)
            return
        if self._insert_value(ctx.guild.id, args):
            ctx.send("{} value add to {}".format(args[1], args[0]), delete_after=30)
            return
        else:
            ctx.send("Incorrect first argument {} found: valid args are: {}".format(args[0], self._shard.get_column()),
                     delete_after=30)
            return

    def _insert_value(self, id, args):
        columns = self._shard.get_column()
        if args[0] == columns[0]:
            self._shard.insert_shard(id, args[0], args[1])
        elif args[0] in columns[1:3]:
            self._shard.insert_shard(id, args[0], int(args[1]))
        else:
            return False
        return True

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name='Wash Your Hands'))
        logging.info('We have logged in as {0.user}'.format(self.bot))

    @commands.command(
        help=''
    )
    @commands.has_permissions(administrator=True)
    async def analytics(self, ctx):
        # TODO: add analytics command.
        print("TODO")
