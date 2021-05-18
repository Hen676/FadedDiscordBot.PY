#!/usr/bin/env python3.7

import json
import os
import sys
import appdirs


def create_dummy_members(filepath: str):
    with open(filepath, 'w') as file:
        json.dump({}, file)
    return True


def get_data_file_dir():
    path = appdirs.user_data_dir('FadedBotApp', 'Hen676')
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def get_data_file_path():
    path = os.path.join(get_data_file_dir(), 'faded_bot_members.json')
    if not os.path.isfile(path):
        if not create_dummy_members(path):
            sys.exit("Failed to create members file {path}".format(path=path))
    return path


class Members:
    _filepath = ""
    _members = {}

    def __init__(self, path: str = ""):
        if path is None or len(path) == 0:
            path = get_data_file_path()
        self._filepath = path
        self.load_members()

    def add_member(self, discord: str, account: str):
        self._members.update({discord: account})

    def get_member(self, discord: str):
        return self._members.get(discord)

    def remove_member(self, discord: str):
        self._members.pop(discord)

    def load_members(self):
        with open(self._filepath, 'r') as file:
            self._members = json.load(file)

    def save_members(self):
        with open(self._filepath, 'w') as file:
            json.dump(self._members, file, sort_keys=True)

    def dump_members(self):
        print(f'{self._filepath}')
        print(f'{self._members}')


if '__main__' == __name__:
    members = Members()
    members.dump_members()
    members.save_members()
