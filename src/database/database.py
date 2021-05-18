import os
import sys

import appdirs
import sqlite3
from sqlite3 import Error

sql_create_user_table = """CREATE TABLE user(
gwaccount VARCHAR(30),
discordid VARCHAR(30),
token CHAR(36),
CONSTRAINT comp_key PRIMARY KEY (gwaccount, discordid)
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
token CHAR(36),
motdchannel INT, 
raidchannel INT,
raidlogchannel INT 
);"""
tables = [sql_create_shard_table, sql_create_user_table, sql_create_evtc_table, sql_create_evtc_user_table]
tables_name = ["shard", "user", "evtc", "evtcuser"]


def get_file_path():
    path = appdirs.user_log_dir('FadedBotApp', 'Hen676')
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


class Database:
    conn = None
    path = ""
    debug = False

    def __init__(self, debug: bool = False):
        self.path = os.path.join(get_file_path(), "Faded_sqlite.db")
        self.debug = debug
        self.conn = self._create_connection()
        if self.conn is None:
            sys.exit("Failed to create Database with path: {path}".format(path=self.path))

    def _create_connection(self):
        conn = None
        try:
            if self.debug:
                conn = sqlite3.connect(':memory:')
            else:
                conn = sqlite3.connect(self.path)
        except Error as e:
            print(e)
        return conn

    def execute(self, sql: str, dic: dict = None):
        """
        Creates a Table in conn database

        :param string sql: SQL to Execute
        :param dic: Dictionary for SQL cmd
        """
        try:
            c = self.conn.cursor()
            if dic is None:
                c.execute(sql)
            else:
                c.execute(sql, dic)
        except Error as e:
            print(e)

    def check_tables(self, table_name: str):
        """
        Checks if table exists

        :param table_name: table name
        :return bool:
        """
        toggle = False
        try:
            c = self.conn.cursor()
            c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=:table_name;",
                      {"table_name": table_name})
            toggle = c.fetchone()[0] == 1
        except Error as e:
            print(e)
        return toggle

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
    for table in tables:
        database.execute(table)
    for name in tables_name:
        print("{name} table is {toggle}".format(name=name, toggle=database.check_tables(name)))
    database.commit()
    database.dump()
    database.close()
