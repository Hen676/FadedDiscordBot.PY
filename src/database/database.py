#!/usr/bin/env python3.7

import os
import sys
import appdirs
import sqlite3
from sqlite3 import Error

sql_create_user_table = """CREATE TABLE user(
gwaccount VARCHAR(30),
discordid VARCHAR(30) PRIMARY KEY,
token CHAR(36)
);"""
sql_create_evtc_table = """CREATE TABLE evtc(
url VARCHAR(80) PRIMARY KEY,
cm BOOL NOT NULL,
success BOOL NOT NULL,
timestamp DATETIME NOT NULL,
bossname VARCHAR(80) NOT NULL
);"""
sql_create_evtc_user_table = """ CREATE TABLE evtcuser(
evtcuserid INT AUTO_INCREMENT PRIMARY KEY,
gwaccount VARCHAR(30) NOT NULL,
evtc VARCHAR(80) NOT NULL,
FOREIGN KEY (evtc) REFERENCES evtc(url)
 );"""
sql_create_shard_table = """CREATE TABLE shard(
shardid INT PRIMARY KEY,
guildid CHAR(36),
ownerid INT,
motdchannel INT, 
raidchannel INT,
raidlogchannel INT 
FOREIGN KEY (owner) REFERENCES user(discordid)
);"""
tables = {"shard": sql_create_shard_table,
          "user": sql_create_user_table,
          "evtc": sql_create_evtc_table,
          "evtcuser": sql_create_evtc_user_table}


def get_file_path():
    path = appdirs.user_log_dir('FadedBotApp', 'Hen676')
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


class Database:
    conn = None
    curs = None
    path = ""
    debug = False

    def __init__(self, debug: bool = False):
        self.path = os.path.join(get_file_path(), "Faded_sqlite.db")
        self.debug = debug
        self._create_connection()
        if self.conn is None:
            sys.exit("Failed to create Database with path: {path}".format(path=self.path))

    def _create_connection(self):
        try:
            if self.debug:
                self.conn = sqlite3.connect(':memory:')
            else:
                self.conn = sqlite3.connect(self.path)
            self.curs = self.conn.cursor()
        except Error as e:
            print(e)

    def execute(self, sql: str, dic=None, single=False, commit=False):
        """
        Executes SQL in database

        :param commit: Commit Database cmd
        :param single: Return multiple or one result
        :param sql: SQL to Execute
        :param dic: Dictionary for SQL cmd
        :return: Row or Rows of data requested
        """
        if dic is None:
            dic = {}
        with self.conn:
            self.curs.execute(sql, dic)
        if commit:
            self.conn.commit()
        else:
            if single:
                return self.curs.fetchone()
            else:
                return self.curs.fetchall()

    def check_tables(self, table_name: str):
        """
        Checks if table exists

        :param table_name: table name
        :return: bool
        """
        return self.execute(sql="SELECT count(name) FROM sqlite_master WHERE type='table' AND name=:table_name;",
                            dic={"table_name": table_name})[0] == 1

    def dump(self):
        """
        Dump Database
        """
        for line in self.conn.iterdump():
            print(line)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.commit()
        self.conn.close()


if __name__ == '__main__':
    database = Database(debug=True)
    for name, val in tables.items():
        if not database.check_tables(name):
            database.execute(val)
    database.commit()
    database.dump()
    database.close()
