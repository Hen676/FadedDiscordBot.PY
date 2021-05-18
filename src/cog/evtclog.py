#!/usr/bin/env python3.7

import logging
import discord
from discord.ext import commands


class EvtcLog(commands.Cog):
    _raid_log_channel = 0

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help='',
        brief=''
    )
    async def upload(self, ctx, arg):
        logging.debug('Calling upload cmd')

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.id == self.bot.user.id:
            if isinstance(message.channel, discord.DMChannel):
                x = message.attachments
                print(x)
