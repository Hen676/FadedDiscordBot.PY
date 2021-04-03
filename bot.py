#!/usr/bin/env python3.7
"""
Created on Sat Feb  6 13:04:51 2021

bot.py: brains of the bot
"""
__author__ = "Henry John Timms"
__copyright__ = "Copyright 2021, Henry John Timms"
__license__ = "MIT"
__version__ = '1.2.0'

import discord 
from discord.ext import commands, tasks
import nest_asyncio
import gw2api
import config
import schedule
import logging
import members
from enum import Enum
    
# raid emoji enum
class Raid_Emoji(Enum):
    ONE = '1️⃣'
    TWO = '2️⃣'
    THREE = '3️⃣'
    FOUR = '4️⃣'
    SEVEN = '7️⃣'
            
class Field:
    _name = ''
    _value = ''
    _inline = None
    
    def __init__(self,name: str,value: str,inline=False):
        self._name = name
        self._value = value
        self._inline = inline

class Startup(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name='Wash Your Hands'))
        logging.info('We have logged in as {0.user}'.format(self.bot))
        
class User(commands.Cog):
    _gw2api = None
    _members = None
    
    def __init__(self,bot,gw2api,members):
        self.bot = bot
        self._gw2api = gw2api
        self._members = members
    
    @commands.command(
        help='Takes account name and if there in the guild add them as a member',
        brief='Adds user to member rank if there in the guild'
        )
    async def new(self, ctx, arg):
        logging.info('Calling new cmd')
        if self._gw2api.user_in_guild(arg):
            # add role to user
            role = discord.utils.get(ctx.author.guild.roles, name='Member')
            self._members.add_member(ctx.author.id, arg)
            self._members.save_members()
            await ctx.author.add_roles(role)
            
    
    @commands.command(
        help='Takes account name and returns users guild infomation',
        brief='Shows users guild infomation'
        )
    async def user(self, ctx, arg):
        logging.info('Calling user cmd')
        info = self._gw2api.user_guild_info(arg)
        async with ctx.channel.typing():
            embedmsg = embed_msg_builder(title="Users Guild Info",
                                         thumbnail=info._rank_icon,
                                         fields=[Field('Name',info._name),
                                                 Field('Rank',info._rank),
                                                 Field('Join Date',info._join_date)])
            await ctx.send(embed=embedmsg)

class Update(commands.Cog):
    _raid_channel = 0
    _motd_channel = 0
    _raid_disc = ''
    _gw2api = None
    _admin_roles = []
    
    def __init__(self,bot,gw2api,raid_disc,raid_channel,motd_channel,roles):
        self.bot = bot
        self._raid_channel = raid_channel
        self._motd_channel = motd_channel
        self._raid_disc = raid_disc
        self._gw2api = gw2api
        self._admin_roles = roles
        schedule.every().monday.at("12:00").do(self.raid_update)
        schedule.every(2).hours.do(self.motd_update)
        
    
    @commands.command(
        help='motd for guild msg update and raid to create a new raid vote',
        brief='Updates Guild posts'
        )
    async def update(self, ctx, arg):
        logging.info('Calling update cmd')
        if any(xs in ctx.author.roles for xs in self._admin_roles):
            if arg == 'motd':
                await self.motd_update()
            if arg == 'raid':
                await self.raid_update()

    @tasks.loop(seconds=1)
    async def loop(self):
        schedule.run_pending()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == self._raid_channel:
            if payload.user_id == self.bot.user.id:
                if(payload.emoji not in Raid_Emoji._value2member_map_):
                    print(payload.emoji)
                #   (payload.message_id).remove_reation(payload.emoji,)
                # if reation valid, else remove

    async def motd_update(self):
        motd = self._gw2api.guild_motd()
        channel = self.bot.get_channel(self._motd_channel)
        msg = await channel.fetch_message(channel.last_message_id)
        
        if msg != None:
            if msg.content == motd:
                return
            else:
                await msg.delete()
        await channel.send(motd)
    
    async def raid_update(self):
        channel = self.bot.get_channel(self._raid_channel)
        embedmsg = embed_msg_builder(title="Raid Training Vote", 
                                     description=self._raid_disc, 
                                     thumbnail=self._gw2api.raid_icon())
        message = await channel.send(embed=embedmsg)
        for reaction in Raid_Emoji:
            message.add_reaction(reaction.value)
        
        
class Debug(commands.Cog):
    _raid_channel = 0
    _motd_channel = 0
    
    def __init__(self,bot,raid_channel,motd_channel):
        self.bot = bot
        self._raid_channel = raid_channel
        self._motd_channel = motd_channel
        
    @commands.command(
        help='Debug, for internal use only'
        )
    async def debug(self, ctx):
        channel = self.bot.get_channel(self._motd_channel)
        msg = await channel.fetch_message(channel.last_message_id)
        print(msg.content)

    
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
    
    
class Faded_Bot:
    _bot = None
    _config = None
    _members = None
    _gw2api = None
    
    _gw2_token = ''
    _discord_token = ''
    _discord_raid_channel = 0
    _discord_motd_channel = 0
    _discord_admin_roles = []
    
    def __init__(self, debug = False):
        self._bot = commands.Bot(command_prefix='g!',description='g!help for help :P')
        self._members = members.Members()
        self._config = config.Config()
        self.assign_config()
        
        self._gw2api = gw2api.Guild_api(self._gw2_token)
        
        if debug:
            self._bot.add_cog(Debug(self._bot,
                                    self._discord_raid_channel,
                                    self._discord_motd_channel))
        
        self._bot.add_cog(Startup(self._bot))
        self._bot.add_cog(User(self._bot,self._gw2api,self._members))
        self._bot.add_cog(Update(self._bot,
                                 self._gw2api,
                                 'Vote for which Raid Wing you want training for this week',
                                 self._discord_raid_channel,
                                 self._discord_motd_channel))
        
    def assign_config(self):
        self._gw2_token = self._config.gw2_token
        self._discord_token = self._config.discord_token
        self._discord_raid_channel = int(self._config.discord_raid_channel)
        self._discord_motd_channel = int(self._config.discord_motd_channel)
        self._discord_admin_roles = self._config.discord_admin_roles
        
    def start(self):
        nest_asyncio.apply()
        self._bot.run(self._discord_token)
        
    
if '__main__' == __name__:
    # run bot tests
    logging.basicConfig(filename='debug.log',
                        level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')
    faded_bot = Faded_Bot(True)
    faded_bot.start()
    
    

