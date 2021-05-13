#!/usr/bin/env python3.7
"""
Created on Tue May  4 19:45:45 2021

config.py: shards config
"""
__author__ = "Henry John Timms"
__copyright__ = "Copyright 2021, Henry John Timms"
__license__ = "MIT"
__version__ = '1.0.0'

import enum
import json
import os
import sys

import appdirs


class ShardKeys(enum.Enum):
    GUILDWARS = "gw2"
    GUILDWARS_GUILD_ID = "id"
    GUILDWARS_TOKEN = "token"
    SERVER = "shard"
    SERVER_ID = "id"
    SERVER_MOTD_CHANNEL = "motd_channel"
    SERVER_RAID_CHANNEL = "raid_channel"
    SERVER_RAID_LOG_CHANNEL = "raid_log_channel"
    SERVER_RAID_EMOJI = "raid_emoji"


def create_dummy_shard(filepath: str):
    dummy_config = {
        ShardKeys.GUILDWARS.value: {
            ShardKeys.GUILDWARS_TOKEN.value: "<Guild owners api key>",
            ShardKeys.GUILDWARS_GUILD_ID.value: "<Guild id>"
        },
        ShardKeys.SERVER.value: {
            ShardKeys.SERVER_ID.value: 0,
            ShardKeys.SERVER_MOTD_CHANNEL.value: 0,
            ShardKeys.SERVER_RAID_CHANNEL.value: 0,
            ShardKeys.SERVER_RAID_LOG_CHANNEL.value: 0,
            ShardKeys.SERVER_RAID_EMOJI.value: [1, 2, 3, 4, 7]
        }
    }
    with open(filepath, 'w') as file:
        json.dump(dummy_config, file)
    return True


def get_data_file_dir():
    path = appdirs.user_data_dir('FadedBotApp', 'Hen676')
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def get_data_file_path(token: str):
    path = os.path.join(get_data_file_dir(), token)
    path = os.path.join(path, 'shard_config.json')
    if not os.path.isfile(path):
        if not create_dummy_shard(path):
            sys.exit("Failed to create members file {path}".format(path=path))
    return path


class ShardConfig:
    _filepath = ""
    _shard_config = {}

    _guildwars_token = ""
    _guildwars_guild_id = ""
    _server_id = 0
    _server_motd_channel = 0
    _server_raid_channel = 0
    _server_raid_log_channel = 0
    _server_raid_emoji = []

    def __init__(self):
        path = get_data_file_path(token="id")
        self._filepath = path
        self.load_shard()

    def dump_shard(self):
        print(f'{self._filepath}')
        print(f"{ShardKeys.GUILDWARS.value}")
        print(f"\t{ShardKeys.GUILDWARS_TOKEN.value} = {self._guildwars_token}")
        print(f"\t{ShardKeys.GUILDWARS_GUILD_ID.value} = {self._guildwars_guild_id}")
        print(f"{ShardKeys.SERVER.value}")
        print(f"\t{ShardKeys.SERVER_ID.value} = {self._server_id}")
        print(f"\t{ShardKeys.SERVER_MOTD_CHANNEL.value} = {self._server_motd_channel}")
        print(f"\t{ShardKeys.SERVER_RAID_CHANNEL.value} = {self._server_raid_channel}")
        print(f"\t{ShardKeys.SERVER_RAID_LOG_CHANNEL.value} = {self._server_raid_log_channel}")
        print(f"\t{ShardKeys.SERVER_RAID_EMOJI.value} = {self._server_raid_emoji}")

    def load_shard(self):
        with open(self._filepath, 'r') as file:
            self._shard_config = json.load(file)

        guildwars_config = self._shard_config[ShardKeys.GUILDWARS.value]
        self._guildwars_token = guildwars_config[ShardKeys.GUILDWARS_TOKEN.value]
        self._guildwars_guild_id = guildwars_config[ShardKeys.GUILDWARS_GUILD_ID.value]

        server_config = self._shard_config[ShardKeys.SERVER.value]
        self._server_id = server_config[ShardKeys.SERVER_ID.value]
        self._server_motd_channel = server_config[ShardKeys.SERVER_MOTD_CHANNEL.value]
        self._server_raid_channel = server_config[ShardKeys.SERVER_RAID_CHANNEL.value]
        self._server_raid_log_channel = server_config[ShardKeys.SERVER_RAID_LOG_CHANNEL.value]
        self._server_raid_emoji = server_config[ShardKeys.SERVER_RAID_EMOJI.value]

    def save_shard(self):
        self._shard_config = {
            ShardKeys.GUILDWARS.value: {
                ShardKeys.GUILDWARS_TOKEN.value: self._guildwars_token,
                ShardKeys.GUILDWARS_GUILD_ID.value: self._guildwars_guild_id
            },
            ShardKeys.SERVER.value: {
                ShardKeys.SERVER_ID.value: self._server_id,
                ShardKeys.SERVER_MOTD_CHANNEL.value: self._server_motd_channel,
                ShardKeys.SERVER_RAID_CHANNEL.value: self._server_raid_channel,
                ShardKeys.SERVER_RAID_LOG_CHANNEL.value: self._server_raid_log_channel,
                ShardKeys.SERVER_RAID_EMOJI.value: self._server_raid_emoji
            }
        }
        with open(self._filepath, 'w') as file:
            json.dump(self._shard_config, file)


if '__main__' == __name__:
    shard = ShardConfig()
    shard.dump_shard()
    shard.save_shard()
