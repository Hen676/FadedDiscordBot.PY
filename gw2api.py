# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 15:17:40 2021

@author: Hen676

GW2API
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

# global Var
url = "http://api.guildwars2.com"
extension_rank = "/v2/guild/0f5f2161-607e-e511-aa11-ac162daae275/ranks?access_token="
extension_member = "/v2/guild/0f5f2161-607e-e511-aa11-ac162daae275/members?access_token="
extension_guild = "/v2/guild/0f5f2161-607e-e511-aa11-ac162daae275?access_token="

# global ENV Var
GW2_KEY = os.getenv('GW2_KEY')


def guild_motd():
    """Call GW2-API and returns guild motd or else None"""
    
    r = requests.get(url + extension_guild + GW2_KEY, auth=('user', 'pass'))
    if r.status_code != 200:
        return None
    data = r.json()
    return data['motd']

def guild_ranks():
    """Call GW2-API and get guild ranks or else None"""
    
    r = requests.get(url + extension_rank + GW2_KEY, auth=('user', 'pass'))
    if r.status_code != 200:
        return None
    return r.json()

def user_in_guild(message):
    """
    Call GW2-API and get members. find if user is in the guild.
    Parameters:
        message(object): discord.py message
    Returns:
        boolean: true if user is in guild
    """
    
    name = message.content[6:]
    r = requests.get(url + extension_member + GW2_KEY, auth=('user', 'pass'))
    if r.status_code != 200:
        return False
    
    # read data, then loop through for matching name
    data = r.json()
    for user in data:
        if user['name'] == name:
            print(name + ' is in guild')
            return True
    print(name + ' is not in guild')
    return False

def user_guild_info(message):
    """
    Call GW2-API and get members. find if user is in the guild. if yes, print users infomation.
    Parameters:
        message(object): discord.py message
    Returns:
        info(list): list of 4 elements [rank icon, rank name, user name, date]
    """
    
    name = message.content[7:]
    r = requests.get(url + extension_member + GW2_KEY, auth=('user', 'pass'))
    if r.status_code != 200:
        return
    
    # read data, then loop through for matching name
    data = r.json()
    for user in data:
        if user['name'] == name:
            ranks = guild_ranks()
            if ranks != None:
                for rank in ranks:
                    if user['rank'] == rank['id']:
                        date = user['joined'][8:10] + '/' + user['joined'][5:7] + '/' + user['joined'][:4]
                        info = [rank['icon'],user['rank'],user['name'],date]
                        return info
            else:
                return None
    return None