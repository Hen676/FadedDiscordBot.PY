

class User:
    _id = 0
    _account = ""
    _discord_id = ""

    def __init__(self, id, account, discord_id):
        self._account = account
        self._discord_id = discord_id
        self._id = id

    def valid_account(self):
        if len(self._account) > 5:
            if self._account[-4:].isnumeric():
                return True
        return False
