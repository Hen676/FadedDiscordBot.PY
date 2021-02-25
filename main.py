#!/usr/bin/env python3.7
"""
Created on Sat Feb  6 13:04:51 2021

@author: Hen676

Faded Vanguard Discord Bot

Todo:
    * clean code
    * add customization for global vars
    * change all responces over to embed msg format
    * add reaction control to raid msg (can't react with anything other than 1,2,3,4,7)
"""

import gw2api,discord,os,schedule,time,logging,appdirs
from discord.ext import commands
from enum import Enum
from dotenv import load_dotenv

# discord bot
bot = commands.Bot(command_prefix='g!',description='g!help for help :P')
# load ENV
load_dotenv()

# global ENV Var
FADEDBOT_TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
MOTD_CHANNEL = int(os.getenv('MOTD_CHANNEL'))
RAID_CHANNEL = int(os.getenv('RAID_CHANNEL'))

# role enum
class Role(Enum):
    MEMBER = 'Member'
    ADMIN = 'Admin'
            
class Field:
    name = ''
    value = ''
    inline = None
    
    def __init__(self,name,value,inline=False):
        self.name = name
        self.value = value
        self.inline = inline

# msg
help_msg_dis = "List of cmds this bot can do"
help_msg_field = [Field('g!new (account name)',
                        'adds user to member role, if their account is part of the guild'),
                  Field('g!user (account name)',
                        'shows infomation about user relevent to the guild'),
                  Field('g!update',
                        'updates motd if required')]
raid_msg = 'Vote for which Raid Wing you want training for this week'

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Wash Your Hands'))
    logging.info('We have logged in as {0.user}'.format(bot))

@bot.command(
    help='Takes account name and if there in the guild add them as a member',
    brief='Adds user to member rank if there in the guild'
    )
async def new(ctx, arg):
    logging.info('Calling new cmd')
    if gw2api.user_in_guild(arg):
        # add role to user
        role = discord.utils.get(ctx.author.guild.roles, name=Role.MEMBER.value)
        await ctx.author.add_roles(role)

@bot.command(
    help='Takes account name and returns users guild infomation',
    brief='Shows users guild infomation'
    )
async def user(ctx, arg):
    logging.info('Calling user cmd')
    info = gw2api.user_guild_info(arg)
    async with ctx.channel.typing():
        embedmsg = embed_msg_builder(title="Users Guild Info",
                                     thumbnail=info.rank_icon,
                                     fields=[Field('Name',info.name),
                                             Field('Rank',info.rank),
                                             Field('Join Date',info.join_date)])
        await ctx.channel.send(embed=embedmsg)

@bot.command(
    help='motd for guild msg update and raid to create a new raid vote',
    brief='Updates Guild posts'
    )
async def update(ctx, arg):
    logging.info('Calling update cmd')
    role = discord.utils.get(ctx.author.guild.roles, name=Role.ADMIN.value)
    if role in ctx.author.roles:
        if arg == 'motd':
            await motd_update()
        if arg == 'raid':
            await raid_update()

async def motd_update():
    motd = gw2api.guild_motd()
    channel = bot.get_channel(MOTD_CHANNEL)
    if channel.last_message != None:
        if channel.last_message.content == motd:
            return
        else:
            await channel.last_message.delete()
    await channel.send(motd)
    
async def raid_update():
    channel = bot.get_channel(RAID_CHANNEL)
    embedmsg = embed_msg_builder(title="Raid Training Vote", 
                                 description=raid_msg, 
                                 thumbnail=gw2api.raid_icon())
    message = await channel.send(embed=embedmsg)
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')
    await message.add_reaction('3️⃣')
    await message.add_reaction('4️⃣')
    await message.add_reaction('7️⃣')
        
    
def embed_msg_builder(title, thumbnail=None, fields=None, description=""):
    """
    Create an embed msg for discord
    
    Parameters:
        title(str): title for embed
        thumbnail(str): thumbnail for embed
        fields(2D list): list of fields
        
    Returns:
        embed(object): discord embed
    """
    
    embedmsg = discord.Embed(title=title, color=0x00ff00, description=description)
    if thumbnail != None:
        embedmsg.set_thumbnail(url=thumbnail)
    if fields != None:
        for field in fields:
            embedmsg.add_field(name=field.name, value=field.value, inline=field.inline)
        return embedmsg
    else:
        return embedmsg
    
# run client (commented out until im not shit and it works correctly)
# schedule.every().monday.at("12:00").do(raid_update)
# schedule.every(2).hours.do(motd_update)

logging.basicConfig(filename='debug.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')

bot.run(FADEDBOT_TOKEN)

while True:
    schedule.run_pending()
    time.sleep(4)
