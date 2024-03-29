#!/usr/bin/env python3.7

import requests
import logging


class User:
    _name = ''
    _rank = ''
    _rank_icon = ''
    _join_date = ''

    def __init__(self, name, rank, rank_icon, join_date):
        self._name = name
        self._rank = rank
        self._rank_icon = rank_icon
        self._join_date = join_date[8:10] + '/' + join_date[5:7] + '/' + join_date[:4]

    def get_join_date(self):
        return self._join_date

    def get_name(self):
        return self._name

    def get_rank(self):
        return self._rank

    def get_rank_icon(self):
        return self._rank_icon


# TODO: db Rework
class GuildApi:
    _url = "http://api.guildwars2.com"
    _extension_rank = "/v2/guild/0f5f2161-607e-e511-aa11-ac162daae275/ranks?access_token="
    _extension_member = "/v2/guild/0f5f2161-607e-e511-aa11-ac162daae275/members?access_token="
    _extension_guild = "/v2/guild/0f5f2161-607e-e511-aa11-ac162daae275?access_token="
    _key = ""

    def __init__(self, key: str):
        self._key = key

    def guild_motd(self):
        """Call GW2-API and returns guild motd or else None"""

        r = requests.get(self._url + self._extension_guild + self._key, auth=('user', 'pass'))
        if r.status_code != 200:
            return None
        data = r.json()
        return data['motd']

    def guild_ranks(self):
        """Call GW2-API and get guild ranks or else None"""

        r = requests.get(self._url + self._extension_rank + self._key, auth=('user', 'pass'))
        if r.status_code != 200:
            return None
        return r.json()

    def raid_icon(self):
        """Call GW2-API and get raid icon or else None"""

        r = requests.get(self._url + '/v2/files?id=map_raid_entrance')
        if r.status_code != 200:
            return None
        data = r.json()
        return data['icon']

    def user_in_guild(self, name):
        """
        Call GW2-API and get members. find if user is in the guild.

        :param name: account name
        :return bool: true if user is in guild
        """

        r = requests.get(self._url + self._extension_member + self._key, auth=('user', 'pass'))
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

    def user_guild_info(self, name):
        """
        Call GW2-API and get members. find if user is in the guild. if yes, print users information.

        :param name: account name
        :return User: user object containing user info
        """

        r = requests.get(self._url + self._extension_member + self._key, auth=('user', 'pass'))
        if r.status_code != 200:
            return

        # read data, then loop through for matching name
        data = r.json()
        for user in data:
            if user['name'] == name:
                ranks = self.guild_ranks()
                if ranks is not None:
                    for rank in ranks:
                        if user['rank'] == rank['id']:
                            return User(name=user['name'],
                                        rank=user['rank'],
                                        rank_icon=rank['icon'],
                                        join_date=user['joined'])
                else:
                    return None
        return None


def check_token(arg):
    token_url = "https://api.guildwars2.com/v2/tokeninfo?access_token="
    r = requests.get(token_url + arg, auth=('user', 'pass'))
    if r.status_code != 200:
        return False
    if "id" in r.json():
        return True
    return False


if '__main__' == __name__:
    print('Testing GW2 api enter API key:')
    USER = 'Hen.5687'
    gw2api = GuildApi(input())
    print(gw2api.user_guild_info(USER))
    print(gw2api.guild_motd())
    print(gw2api.guild_ranks())
    print(gw2api.raid_icon())
