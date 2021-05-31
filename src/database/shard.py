#!/usr/bin/env python3.7

import src.database.database as db


class Shard:
    _database = None
    _column = [
        "guildid",
        "motdchannel",
        "raidchannel",
        "raidlogchannel"
    ]

    def __init__(self, data: db.Database):
        self._database = data

    def get_shard(self, shard_id: int):
        return self._database.execute(
            sql="SELECT * FROM shard Where shardid=:shard_id",
            dic={"shard_id": shard_id},
            single=True)

    def create_shard(self, shard_id: int, owner_id: int):
        self._database.execute(
            sql="INSERT INTO shard(shardid, ownerid) VALUES(:shard_id, :owner_id)",
            dic={"shard_id": shard_id,
                 "owner_id": owner_id},
            commit=True)

    def get_column(self):
        return self._column

    def insert_shard(self, shard_id: int, column: str, val):
        """
        :param val: Value to add/replace in shard.
        :param shard_id: Shard to add/replace values too.
        :param column: Column for where to add value
        """
        self._database.execute(
            sql="INSERT OR REPLACE INTO shard(shardid, {}) VALUES(:shard_id, :val)".format(column),
            dic={"shard_id": shard_id,
                 "val": val},
            commit=True)


if __name__ == '__main__':
    database = db.Database(debug=True)
    if not database.check_tables("shard"):
        database.execute(sql=db.sql_create_shard_table, commit=True)
    shard = Shard(database)
    shard.create_shard(shard_id=0, owner_id=0)
    shard.insert_shard(shard_id=0, column=shard.get_column()[0], val=123456789)
    row = shard.get_shard(shard_id=0)
    database.dump()
    database.close()
