from typing import Optional
import discord
import random


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


def _random_hex_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def embed_msg_builder(title, description="", thumbnail: Optional[str] = None, fields: Optional[list[Field]] = None):
    """
    Create an embed msg for discord

    :param string title: title for embed
    :param description: description for embed
    :param thumbnail: thumbnail for embed
    :param fields: list of fields for embed
    :return: embed(object): discord embed
    """
    embedmsg = discord.Embed(title=title, color=_random_hex_color(), description=description)
    if thumbnail is not None:
        embedmsg.set_thumbnail(url=thumbnail)
    if fields is not None:
        for field in fields:
            embedmsg.add_field(name=field.name, value=field.value, inline=field.inline)
        return embedmsg
    else:
        return embedmsg


def embed_loading_msg(description):
    return embed_msg_builder(title="Loading", description=description, thumbnail="https://imgur.com/gVRSRmt.gif")
