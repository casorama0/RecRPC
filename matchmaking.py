import httpx


from recnetlogin import RecNetLogin

rnl = RecNetLogin()

mmend = "https://match.rec.net/player?id=%s"


class response:
    def __init__(self, jsondat):
        for key, value in jsondat[0].items():
            setattr(self, key, value)


class room_instance:
    def __init__(self, response):
        for key, value in response.roomInstance.items():
            setattr(self, key, value)


def info(pid):
    token = rnl.get_token(include_bearer=True)  # Use async method for token retrieval
    data = httpx.get(mmend % (pid), headers={"Authorization": token}).json()
    return response(data)
