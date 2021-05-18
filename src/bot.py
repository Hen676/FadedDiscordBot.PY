#!/usr/bin/env python3.7

from discord.ext import commands
import config
import logging
from src.cog.control import Control
from src.cog.debug import Debug
from src.cog.evtclog import EvtcLog
from src.cog.update import Update
from src.cog.user import User
from src.util import gw2api, members


class FadedBot:
    _gw2_token = ''
    _discord_token = ''
    _discord_raid_channel = 0
    _discord_motd_channel = 0
    _discord_admin_roles = []
    _cogs = []

    def __init__(self, debug=False):
        self._bot = commands.Bot(command_prefix='f!', description='f!help for help :P')
        self._members = members.Members()
        self._config = config.Config()
        self.assign_config()

        self._gw2api = gw2api.GuildApi(self._gw2_token)

        self._cogs.append(Control(self._bot))
        self._cogs.append(User(self._bot, self._gw2api, self._members))
        self._cogs.append(Update(self._bot,
                                 self._gw2api,
                                 'Vote for which Raid Wing you want training for this week',
                                 self._discord_raid_channel,
                                 self._discord_motd_channel))
        self._cogs.append(EvtcLog(self._bot))

        if debug:
            self._cogs.append(Debug(self._bot, self._discord_raid_channel, self._discord_motd_channel))

        for cog in self._cogs:
            self._bot.add_cog(cog)

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
