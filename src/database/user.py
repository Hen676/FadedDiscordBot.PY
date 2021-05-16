

class User:
    _account = ""
    _discord_id = ""
    _token = ""

    def __init__(self, id, account, discord_id, token):
        self._account = account
        self._discord_id = discord_id
        self._token = token

    def valid_account(self):
        if len(self._account) > 5:
            if self._account[-4:].isnumeric():
                return True
        return False
