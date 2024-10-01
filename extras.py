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

    
    

    def __init__(self, roomID, name, type):
        
        self.roomID = roomID  # Store room ID for potential future use
        if "RN_API_KEY" in self.env:
          self.RecNet = recnetpy.Client(api_key=self.env["RN_API_KEY"])
        else:
          raise ValueError("You're missing the RN_API_KEY in your .env.secret file.")


        asyncio.ensure_future(self.async_setup(roomID, name, type))

    async def async_setup(self, roomID, name, type):
        
        self.loadCache()
        
        try:
          self.cache[str(roomID)]
        except:
          fetched_room = await self.RecNet.rooms.fetch(roomID)
          try:
             fetched_room = {"name": fetched_room.name,
                          "image": fetched_room.image_name}
          except:
             fetched_room = None
          self.cache[str(roomID)] = fetched_room
          print("Cached new room data")
          self.saveCache()
        else:
           fetched_room = self.cache.get(str(roomID))


        self.name = name if fetched_room is None and type == 2 else (fetched_room["name"] if fetched_room else "Private Room")
        self.image = (
            self.default_dorm_image if fetched_room is None and type == 2 else (
                "https://img.rec.net/" + fetched_room["image"] + "?cropSquare=True" if (fetched_room) else self.default_private_image
            )
        )
      
    def loadCache(self, filename="cache.json"):
      try:
        with open(filename, 'r') as f:
            self.cache = json.load(f)
      except FileNotFoundError:
         self.cache = {}
      
      
    def saveCache(self, filename="cache.json"):
       with open(filename, "w") as out:
          json.dump(self.cache, out, indent=4)
         
        

    

class event:
    cache = {}

    env = dotenv_values(".env.secret")

    
    
    async def async_setup(self, eventId):
      
      if eventId in self.cache:
         fetched_event = self.cache.get(eventId)
      else:
        fetched_event = await self.RecNet.events.fetch(eventId)
        self.cache[eventId] = fetched_event
        print("Saved new event to cache")

      self.name = fetched_event.name

      if fetched_event.image_name == None:
          try:
            room = await fetched_event.get_room()
            self.image = "https://img.rec.net/" + room.image_name + "?cropSquare=True"
          except:
            self.image = "https://img.rec.net/DefaultRoomImage.jpg?cropSquare=True"


    def __init__(self, eventId):
      

      if "RN_API_KEY" in self.env:
       self.RecNet = recnetpy.Client(api_key=self.env["RN_API_KEY"])
      else:
       raise ValueError("You're missing the RN_API_KEY in your .env.secret file.")
      asyncio.ensure_future(self.async_setup(eventId))



def setup():
    try: 
        with open('accountInfo.json', 'r') as openfile:
            data = json.load(openfile)
    except FileNotFoundError:
      username = input("Please enter your username: \n")

      try:
        userID = requests.get(f"https://apim.rec.net//accounts/account?username={username}").json()["accountId"]
      except:
        print("Invalid username provided")
        exit()

      data = {"userID": userID,
              "username": username}

      with open('accountInfo.json', 'w') as outfile:
        json.dump(data, outfile)
      print("New user data has been written")
      return data
    else:
      print("User file found and loaded")
      return data