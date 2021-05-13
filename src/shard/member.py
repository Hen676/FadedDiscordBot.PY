

class Member:
    _account = ""
    _discord_id = ""
    _id = ""

    def __init__(self):
        print("will get values via db")

    def valid_account(self):
        if len(self._account) > 5:
            if self._account[-4:].isnumeric():
                return True
        return False
