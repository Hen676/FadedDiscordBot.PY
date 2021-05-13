import src.shard.database as db

if __name__ == '__main__':
    database = db.database()
    database.execute(db.sql_create_user_table)
    database.execute(db.sql_create_shard_table)
    database.close()
