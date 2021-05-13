import secrets
from enum import Enum
from typing import Optional


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


class Shard:
    _token = ""
    _id: int = 0
    _motd_channel: int = 0
    _raid_channel: int = 0
    _raid_log_channel: int = 0
    _guild_token = ""
    _guild_id = ""

    def __init__(self):
        print("will get values via db")

    @property
    def get_id(self):
        return self._id

    @property
    def get_motd_channel(self):
        return self._motd_channel
