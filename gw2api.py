# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 15:17:40 2021

@author: Hen676
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

"""
Call GW2-API and get guild motd.
Parms:
    none
"""
def guild_motd():
    # request guild data
    r = requests.get(url + extension_guild + GW2_KEY, auth=('user', 'pass'))
    if r.status_code != 200:
        return False
    
    data = r.json()
    return data['motd']

"""
Call GW2-API and get guild ranks.
Parms:
    none
"""
def guild_ranks():
    r = requests.get(url + extension_rank + GW2_KEY, auth=('user', 'pass'))
    if r.status_code != 200:
        return None
    return r.json()

"""
Call GW2-API and get members. find if user is in the guild.
Parms:
    name - gw2 account name
"""
def user_in_guild(name):
    
    # request guild members
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

"""
Call GW2-API and get members. find if user is in the guild. if yes, print users infomation.
Parms:
    message - users requesting message.
Returns:
    info - list of 4 elements [rank icon, rank name, user name, date]
"""
def user_guild_info(message):
    name = message.content[7:]
            
    # request guild members
    r = requests.get(url + extension_member + GW2_KEY, auth=('user', 'pass'))
    if r.status_code != 200:
        return
    
    # read data, then loop through for matching name
    data = r.json()
    for user in data:
        if user['name'] == name:
            ranks = guild_ranks()
            if ranks is not None:
                for rank in ranks:
                    if user['rank'] == rank['id']:
                        date = user['joined'][8:10] + '/' + user['joined'][5:7] + '/' + user['joined'][:4]
                        info = [rank['icon'],user['rank'],user['name'],date]
                        return info
            else:
                return 'ranks not found'
    return name + ' not found'