from src.shard.database import database

_sql_create_user_table = """

"""
_sql_create_shard_table = """

"""

if __name__ == '__main__':
    database = database()
    database.execute(_sql_create_user_table)
    database.execute(_sql_create_shard_table)
    database.close()
