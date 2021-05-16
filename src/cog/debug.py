from discord.ext import commands, tasks


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