# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 13:04:51 2021

@author: Hen676
"""

import gw2api
import discord
import os
import schedule
import time
from dotenv import load_dotenv

client = discord.Client()
load_dotenv()

# global Var
role_member = "Member"
role_admin = "Admin"

# global ENV Var
TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
MOTD_CHANNEL = int(os.getenv('MOTD_CHANNEL'))
RAID_CHANNEL = int(os.getenv('RAID_CHANNEL'))

# msg
help_msg = 'List of cmds this bot can do :P\ng!new (account name) - adds user to member role, if their account is part of the guild\ng!user (account name) - shows infomation about user relevent to the guild\ng!update - updates motd if required'
raid_msg = 'Vote for which Raid Wing you want training for this week'

"""
TODO:
    add raid wing vote msg
    format user info cmd
    add guild rank emblems to user info
    add pulling for g!update
    clean code
    add customization for global vars
"""

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Wash Your Hands'))
    print('We have logged in as {0.user}'.format(client))

    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not check_guild(message):
        return
    
    # help
    if message.content.startswith('g!help'):
        async with message.channel.typing():
            await message.channel.send(help_msg)
        
    # new user cmd
    if message.content.startswith('g!new'):
        print('finding user ' + message.content[6:])
        if gw2api.user_in_guild(message.content[6:]):
            # add role to user
            role = discord.utils.get(message.author.guild.roles, name=role_member)
            await message.author.add_roles(role)

    # user infomation
    if message.content.startswith('g!user'):
        info = gw2api.user_guild_info(message)
        async with message.channel.typing():
            embedmsg = discord.Embed(title="User Guild Info", color=0x00ff00)
            embedmsg.set_thumbnail(info[0])
            embedmsg.add_field(name='User Name: ', value=info[2])
            embedmsg.add_field(name='User Rank: ', value=info[1])
            embedmsg.add_field(name='User Join Date: ', value=info[3])
            await message.channel.send(embedmsg)
        
    # checks users is admin
    role = discord.utils.get(message.author.guild.roles, name=role_admin)
    if role in message.author.roles:   
        # guild motd
        if message.content.startswith('g!update motd'):
            await motd_update()
        if message.content.startswith('g!update raid'):
            await raid_update()


async def motd_update():
    motd = gw2api.guild_motd()
    channel = client.get_channel(MOTD_CHANNEL)
    if channel.last_message is not None:
        if channel.last_message.content == motd:
            return
        async with channel.typing():
            await channel.last_message.delete()
    async with channel.typing():
        await channel.send(motd)
    
async def raid_update():
    channel = client.get_channel(RAID_CHANNEL)
    message = await channel.send(raid_msg)
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')
    await message.add_reaction('3️⃣')
    await message.add_reaction('4️⃣')
    await message.add_reaction('7️⃣')
    
def check_guild(message):
    return message.guild == client.get_guild(GUILD_ID)
    
# run client
schedule.every().monday.at("12:00").do(raid_update)
schedule.every(2).hours.do(motd_update)
client.run(TOKEN)

while True:
    schedule.run_pending()
    time.sleep(4)