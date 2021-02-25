#!/usr/bin/env python3.7
"""
Created on Mon Feb  8 15:17:40 2021

@author: Hen676

GW2API
"""

import requests,os,logging
from dotenv import load_dotenv

load_dotenv()

# global Var
url = "http://api.guildwars2.com"
extension_rank = "/v2/guild/0f5f2161-607e-e511-aa11-ac162daae275/ranks?access_token="
extension_member = "/v2/guild/0f5f2161-607e-e511-aa11-ac162daae275/members?access_token="
extension_guild = "/v2/guild/0f5f2161-607e-e511-aa11-ac162daae275?access_token="

# global ENV Var
GW2_KEY = os.getenv('GW2_KEY')


class User:
    name = ''
    rank = ''
    rank_icon = ''
    join_date = ''
    
    def __init__(self,name,rank,rank_icon,join_date):
        self.name = name
        self.rank = rank
        self.rank_icon = rank_icon
        self.join_date = join_date[8:10] + '/' + join_date[5:7] + '/' + join_date[:4]

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

def raid_icon():
    """Call GW2-API and get raid icon or else None"""
    
    r = requests.get(url + '/v2/files?id=map_raid_entrance')
    if r.status_code != 200:
        return None
    data = r.json()
    return data['icon']

def user_in_guild(name):
    """
    Call GW2-API and get members. find if user is in the guild.
    
    Parameters:
        name(str): account name
        
    Returns:
        boolean: true if user is in guild
    """
    
    r = requests.get(url + extension_member + GW2_KEY, auth=('user', 'pass'))
    if r.status_code != 200:
        return False
    
    # read data, then loop through for matching name
    data = r.json()
    for user in data:
        if user['name'] == name:
            logging.info('{} is in the guild'.format(name))
            return True
    logging.info('{} is not in the guild'.format(name))
    return False

def user_guild_info(name):
    """
    Call GW2-API and get members. find if user is in the guild. if yes, print users infomation.
    
    Parameters:
        name(str): account name
        
    Returns:
        User(object): user object containing user info
    """
    
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
                        return User(name=user['name'],
                                    rank=user['rank'],
                                    rank_icon=rank['icon'],
                                    join_date=user['joined'])
            else:
                return None
    return None