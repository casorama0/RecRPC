import httpx as requests
import json
import recnetpy
import asyncio
from dotenv import dotenv_values


class room:
    default_dorm_image = "https://img.rec.net/a7c4mxpejlasupag1mkdne875.jpg?cropSquare=True"
    default_private_image = "https://img.rec.net/DefaultRoomImage.jpg?cropSquare=True"
    cache = {}
    
    env = dotenv_values(".env.secret")

    if "RN_API_KEY" in env:
       RecNet = recnetpy.Client(api_key=env["RN_API_KEY"])
    else:
       raise ValueError("You're missing the RN_API_KEY in your .env.secret file.")
    

    def __init__(self, roomID, name, type):
        self.roomID = roomID  # Store room ID for potential future use
        
        asyncio.ensure_future(self.async_setup(roomID, name, type))

    async def async_setup(self, roomID, name, type):
        if roomID in self.cache:
           fetched_room = self.cache.get(roomID)
           print("Retrieved room data from cache.")
        else:
          fetched_room = await self.RecNet.rooms.fetch(roomID)
          self.cache[roomID] = fetched_room


        self.name = name if fetched_room is None and type == 2 else (fetched_room.name if fetched_room else "Private Room")
        self.image = (
            self.default_dorm_image if fetched_room is None and type == 2 else (
                "https://img.rec.net/" + fetched_room.image_name + "?cropSquare=True" if (fetched_room) else self.default_private_image
            )
        )

    

class event:
    cache = {}

    env = dotenv_values(".env.secret")

    if "RN_API_KEY" in env:
       RecNet = recnetpy.Client(api_key=env["RN_API_KEY"])
    else:
       raise ValueError("You're missing the RN_API_KEY in your .env.secret file.")
    
    async def async_setup(self, eventId):
      
      if eventId in self.cache:
         fetched_event = self.cache.get(eventId)
      else:
        fetched_event = await self.RecNet.events.fetch(eventId)
        self.cache[eventId] = fetched_event

      self.name = fetched_event.name

      if fetched_event.image_name == None:
          try:
            room = await fetched_event.get_room()
            self.image = "https://img.rec.net/" + room.image_name + "?cropSquare=True"
          except:
            self.image = "https://img.rec.net/DefaultRoomImage.jpg?cropSquare=True"


    def __init__(self, eventId):
      
      asyncio.ensure_future(self.async_setup(eventId))



def setup():
    try: 
        with open('accountInfo.json', 'r') as openfile:
            data = json.load(openfile)
    except:
      username = input("Please enter your username: \n")

      try:
        userID = requests.get(f"https://apim.rec.net//accounts/account?username={username}").json()["accountId"]
      except:
        print("Invalid username provided")
        exit()

      data = {"userID": userID}
      data = json.dumps(data)

      with open('accountInfo.json', 'w') as outfile:
        outfile.write(data)
      print("New user data has been written")
    else:
      print("User file found and loaded")
      return data["userID"]