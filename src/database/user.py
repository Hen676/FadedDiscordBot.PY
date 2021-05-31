#!/usr/bin/env python3.7

import src.database.database as db


class User:
    _database = None

    def __init__(self, data: db.Database):
        self._database = data

    def get_user(self, discord_id):
        return self._database.execute(
            sql="SELECT * FROM user Where discordid=:discord_id",
            dic={"discord_id": discord_id},
            single=True)

    def create_user(self, discord_id):
        self._database.execute(
            sql="INSERT INTO user(discordid) VALUES(:discord_id)",
            dic={"discord_id": discord_id},
            commit=True)

    def insert_user(self, discord_id: int, column: str, val):
        self._database.execute(
            sql="INSERT OR REPLACE INTO user(discordid, {}) VALUES(:discord_id, :val)".format(column),
            dic={"discord_id": discord_id,
                 "val": val},
            commit=True)


if __name__ == '__main__':
    database = db.Database(debug=True)
    if not database.check_tables("shard"):
        database.execute(sql=db.sql_create_shard_table, commit=True)
    user = User(database)
    user.create_user(discord_id=0)
    user.insert_user(discord_id=0, column="gwaccount", val="123456789")
    row = user.get_user(discord_id=0)
    database.dump()
    database.close()
