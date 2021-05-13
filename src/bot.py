#!/usr/bin/env python3.7
"""
Created on Sat Feb  6 13:04:51 2021

bot.py: brains of the bot
"""
__author__ = "Henry John Timms"
__copyright__ = "Copyright 2021, Henry John Timms"
__license__ = "MIT"
__version__ = '1.3.0'

from typing import Optional

import discord
from discord.ext import commands, tasks
import asyncio
import config
import logging
from enum import Enum

from src.util import discordSchedule, gw2api, members


class RaidEmoji(Enum):
    """
    Raid emoji enum
    """
    ONE = '1️⃣'
    TWO = '2️⃣'
    THREE = '3️⃣'
    FOUR = '4️⃣'
    FIVE = '5️⃣'
    SIX = '6️⃣'
    SEVEN = '7️⃣'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Field:
    """
    Field class used for embed_msg_builder()

    :param string name: Name of the field
    :param string value: Content of the field
    :param bool inline: Weather the field appears inline
    """

    def __init__(self, name: str, value: str, inline=False):
        self.name = name
        self.value = value
        self.inline = inline


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


class User(commands.Cog):
    _gw2api = None
    _members = None

    def __init__(self, bot, gw2api_module, members_module):
        self.bot = bot
        self._gw2api = gw2api_module
        self._members = members_module

    @commands.command(
        help='Takes account name and if there in the guild add them as a member',
        brief='Adds user to member rank if there in the guild'
    )
    async def new(self, ctx, arg):
        logging.info('Calling new cmd')
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
        logging.info('Calling user cmd')
        info = self._gw2api.user_guild_info(arg)
        if info is None:
            return
        async with ctx.channel.typing():
            embedmsg = embed_msg_builder(title="Users Guild Info",
                                         thumbnail=info.get_rank_icon(),
                                         fields=[Field('Name', info.get_name()),
                                                 Field('Rank', info.get_rank()),
                                                 Field('Join Date', info.get_join_date())])
            await ctx.send(embed=embedmsg)


class Update(commands.Cog):
    _raid_channel = 0
    _motd_channel = 0
    _raid_disc = ''
    _gw2api = None

    def __init__(self, bot, gw2api_module, raid_disc, raid_channel, motd_channel):
        self.bot = bot
        self._raid_channel = raid_channel
        self._motd_channel = motd_channel
        self._raid_disc = raid_disc
        self._gw2api = gw2api_module
        self.raid_update.start()
        self.motd_update.start()

    @commands.command(
        help='motd for guild msg update and raid to create a new raid vote',
        brief='Updates Guild posts'
    )
    @commands.has_permissions(administrator=True)
    async def update(self, ctx, arg):
        logging.info('Calling update cmd')
        if arg == 'motd':
            await self.motd_update()
        if arg == 'raid':
            await self.raid_update()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == self._raid_channel:
            if not RaidEmoji.has_value(payload.emoji.name):
                channel = self.bot.get_channel(self._raid_channel)
                msg = await channel.fetch_message(payload.message_id)
                if msg.author.id == self.bot.user.id:
                    await msg.remove_reaction(payload.emoji, payload.member)

    @tasks.loop(hours=2)
    async def motd_update(self):
        motd = self._gw2api.guild_motd()
        channel = self.bot.get_channel(self._motd_channel)
        msg = await channel.fetch_message(channel.last_message_id)

        if msg is not None:
            if msg.content == motd:
                return
            else:
                await msg.delete()
        await channel.send(motd)

    @tasks.loop(hours=168)
    async def raid_update(self):
        channel = self.bot.get_channel(self._raid_channel)
        embedmsg = embed_msg_builder(title="Raid Training Vote",
                                     description=self._raid_disc,
                                     thumbnail=self._gw2api.raid_icon())
        message = await channel.send(embed=embedmsg)
        for reaction in RaidEmoji:
            await message.add_reaction(reaction.value)

    @motd_update.before_loop
    async def before_motd_update(self):
        await self.bot.wait_until_ready()

    @raid_update.before_loop
    async def before_raid_update(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(discordSchedule.sleep(14, 30, 1))


class Debug(commands.Cog):
    _raid_channel = 0
    _motd_channel = 0

    def __init__(self, bot, raid_channel, motd_channel):
        self.bot = bot
        self._raid_channel = raid_channel
        self._motd_channel = motd_channel
        self.debug_schedule.start()

    @commands.command(
        help='Debug, for owner use only'
    )
    @commands.is_owner()
    async def debug(self):
        channel = self.bot.get_channel(self._motd_channel)
        msg = await channel.fetch_message(channel.last_message_id)
        print(msg.content)

    @tasks.loop(seconds=60)
    async def debug_schedule(self):
        channel = self.bot.get_channel(716264737603584061)
        msg = await channel.fetch_message(channel.last_message_id)
        print(msg.content)

    @debug_schedule.before_loop
    async def before_debug_schedule(self):
        await self.bot.wait_until_ready()


def embed_msg_builder(title, description="", thumbnail: Optional[str] = None, fields: Optional[list[Field]] = None):
    """
    Create an embed msg for discord

    :param string title: title for embed
    :param description: description for embed
    :param thumbnail: thumbnail for embed
    :param fields: list of fields for embed
    :return: embed(object): discord embed
    """

    embedmsg = discord.Embed(title=title, color=0x00ff00, description=description)
    if thumbnail is not None:
        embedmsg.set_thumbnail(url=thumbnail)
    if fields is not None:
        for field in fields:
            embedmsg.add_field(name=field.name, value=field.value, inline=field.inline)
        return embedmsg
    else:
        return embedmsg


class FadedBot:
    _gw2_token = ''
    _discord_token = ''
    _discord_raid_channel = 0
    _discord_motd_channel = 0
    _discord_admin_roles = []

    def __init__(self, debug=False):
        self._bot = commands.Bot(command_prefix='g!', description='g!help for help :P')
        self._members = members.Members()
        self._config = config.Config()
        self.assign_config()

        self._gw2api = gw2api.GuildApi(self._gw2_token)

        control_cog = Control(self._bot)
        user_cog = User(self._bot, self._gw2api, self._members)
        update_cog = Update(self._bot,
                            self._gw2api,
                            'Vote for which Raid Wing you want training for this week',
                            self._discord_raid_channel,
                            self._discord_motd_channel)

        if debug:
            debug_cog = Debug(self._bot, self._discord_raid_channel, self._discord_motd_channel)
            self._bot.add_cog(debug_cog)

        self._bot.add_cog(control_cog)
        self._bot.add_cog(user_cog)
        self._bot.add_cog(update_cog)

    def assign_config(self):
        self._gw2_token = self._config.gw2_token
        self._discord_token = self._config.discord_token
        self._discord_raid_channel = int(self._config.discord_raid_channel)
        self._discord_motd_channel = int(self._config.discord_motd_channel)
        self._discord_admin_roles = self._config.discord_admin_roles

    def start(self):
        self._bot.run(self._discord_token)


if '__main__' == __name__:
    # run bot tests
    logging.basicConfig(filename='../debug.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')
    faded_bot = FadedBot(True)
    faded_bot.start()
