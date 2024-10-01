import httpx
import os


from recnetlogin import RecNetLogin

if not os.path.exists(".env.secret"):
    print("You don't have a .env.secret file created!")
    sessionToken = input("Enter your session token: ")
    os.system("cls" if os.name == "nt" else "clear")
    recNetApiKey = input("\n\nEnter your RecNet API key: ")
    with open(".env.secret", "w", encoding="UTF-8") as f:
        f.write(f"RN_SESSION_TOKEN={sessionToken}")
        f.write(f"\nRN_API_KEY={recNetApiKey}")

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
