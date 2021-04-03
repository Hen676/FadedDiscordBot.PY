#!/usr/bin/env python3

# SPDX-License-Identifier: MIT

"""config.py: Read and write bot config to a json file."""
__author__ = "Mehmet Akif Tasova"
__copyright__ = "Copyright 2021, Mehmet Akif Tasova"
__license__ = "MIT"
__version__ = "1.0.0"

import datetime
import shutil
import json
import enum
import sys
import os
import appdirs


class ConfigKeys(enum.Enum):
    GUILDWARS = "gw2"
    GUILDWARS_TOKEN = "token"
    DISCORD = "discord"
    DISCORD_TOKEN = "token"
    DISCORD_ADMIN_ROLES = "admin_roles"
    DISCORD_MOTD_CHANNEL = "motd_channel"
    DISCORD_RAID_CHANNEL = "raid_channel"


def _(text: str):
    """placeholder for localizing error messages"""
    return text


def create_dummy_config(filepath: str):
    dummy_config = {
        ConfigKeys.GUILDWARS.value: {
            ConfigKeys.GUILDWARS_TOKEN.value: "<Your Guild Wars 2 API Token Here>"
        },
        ConfigKeys.DISCORD.value: {
            ConfigKeys.DISCORD_TOKEN.value: "<Your Discord Bot Token Here>",
            ConfigKeys.DISCORD_ADMIN_ROLES.value: ["Admin", "Guild Leader"],
            ConfigKeys.DISCORD_MOTD_CHANNEL.value: "MOTD CHANNEL",
            ConfigKeys.DISCORD_RAID_CHANNEL.value: "RAID CHANNEL"
        }
    }
    with open(filepath, 'w') as fp:
        json.dump(dummy_config, fp)

    return True


def backup_file_if_exists(filepath: str):
    """
    @return True if given file exists and backed up
    """
    if not os.path.isfile(filepath):
        return False

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = filepath + "_" + timestamp
    shutil.copyfile(filepath, backup_path)
    return True

def get_config_dir_path():
    path = appdirs.user_config_dir('FadedBotApp','Hen676')
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def get_config_file_path():
    path = os.path.join(get_config_dir_path(), "faded_bot_config.json")
    if not os.path.isfile(path):
        if not create_dummy_config(path):
            sys.exit(_("Failed to create config file {path}").format(path=path))
    return path


class Config:
    filepath = ""
    config = {}
    gw2_token = ""
    discord_token = ""
    discord_admin_roles = []
    discord_motd_channel = ""
    discord_raid_channel = ""

    def __init__(self, path: str = ""):
        if path is None or len(path) == 0:
            path = get_config_file_path()
        self.filepath = path
        self.load_config()

    def load_config(self):
        with open(self.filepath, 'r') as fp:
            self.config = json.load(fp)

        gw2_config = self.config[ConfigKeys.GUILDWARS.value]
        self.gw2_token = gw2_config[ConfigKeys.GUILDWARS_TOKEN.value]

        discord_config = self.config[ConfigKeys.DISCORD.value]
        self.discord_token = discord_config[ConfigKeys.DISCORD_TOKEN.value]
        self.discord_admin_roles = discord_config[ConfigKeys.DISCORD_ADMIN_ROLES.value]
        self.discord_motd_channel = discord_config[ConfigKeys.DISCORD_MOTD_CHANNEL.value]
        self.discord_raid_channel = discord_config[ConfigKeys.DISCORD_RAID_CHANNEL.value]

    def save_config(self):
        self.config = {
            ConfigKeys.GUILDWARS.value: {
                ConfigKeys.GUILDWARS_TOKEN.value: self.gw2_token
            },
            ConfigKeys.DISCORD.value: {
                ConfigKeys.DISCORD_TOKEN.value: self.discord_token,
                ConfigKeys.DISCORD_ADMIN_ROLES.value: self.discord_admin_roles,
                ConfigKeys.DISCORD_MOTD_CHANNEL.value: self.discord_motd_channel,
                ConfigKeys.DISCORD_RAID_CHANNEL.value: self.discord_raid_channel
            }
        }
        backup_file_if_exists(self.filepath)
        with open(self.filepath, 'w') as fp:
            json.dump(self.config, fp)

    def dump_config(self):
        print(f"{self.filepath}")
        print(f"{ConfigKeys.GUILDWARS.value}")
        print(f"\t{ConfigKeys.GUILDWARS_TOKEN.value} = {self.gw2_token}")
        print(f"{ConfigKeys.DISCORD.value}")
        print(f"\t{ConfigKeys.DISCORD_TOKEN.value} = {self.discord_token}")
        print(f"\t{ConfigKeys.DISCORD_ADMIN_ROLES.value} = {self.discord_admin_roles}")
        print(f"\t{ConfigKeys.DISCORD_MOTD_CHANNEL.value} = {self.discord_motd_channel}")
        print(f"\t{ConfigKeys.DISCORD_RAID_CHANNEL.value} = {self.discord_raid_channel}")


if '__main__' == __name__:
    config = Config()
    config.dump_config()
    config.save_config()
