from src.shard.database import database


class Shard:
    _database = None
    _token = ""
    _motd_channel = 0
    _raid_channel = 0
    _raid_log_channel = 0
    _guild_token = ""
    _guild_id = ""

    def __init__(self, data: database, id: int):
        self.id = id
        self._database = data
        self.get_shard_from_db()

    def get_shard_from_db(self):
        cursor = self._database.execute("SELECT * FROM Shard Where shardid=:shard_id",
                                        {"shard_id": self.id})
        print(cursor)
