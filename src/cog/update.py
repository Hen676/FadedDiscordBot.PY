#!/usr/bin/env python3.7

import asyncio
import logging
from enum import Enum
from discord.ext import commands, tasks
from src.util import discordschedule, discordhelper


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


# TODO: toggles?
# TODO: db Rework
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
        logging.debug('Calling update cmd')
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
        embedmsg = discordhelper.embed_msg_builder(title="Raid Training Vote",
                                                   description=self._raid_disc,
                                                   thumbnail=self._gw2api.raid_icon())
        message = await channel.send(embed=embedmsg)
        for reaction in RaidEmoji:
            await message.add_reaction(reaction.value)

    @motd_update.before_loop
    async def before_motd_update(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(discordschedule.sleep_to_next_hour())

    @raid_update.before_loop
    async def before_raid_update(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(discordschedule.sleep(14, 30, 1))
