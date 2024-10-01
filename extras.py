"""
Handles all of the room and event data and returns the proper images / names / etc.
"""

import json
import asyncio
import httpx as requests
import recnetpy
from dotenv import dotenv_values


class Room:
    """
    Room data handling. This returns data based on whether the room is private or not,
    among other things.
    """

    default_dorm_image = (
        "https://img.rec.net/a7c4mxpejlasupag1mkdne875.jpg?cropSquare=True"
    )
    default_private_image = "https://img.rec.net/DefaultRoomImage.jpg?cropSquare=True"
    cache = {}
    env = dotenv_values(".env.secret")

    def __init__(self, room_id, name, instance_type):

        self.room_id = room_id  # Store room ID for potential future use
        if "RN_API_KEY" in self.env:
            self.RecNet = recnetpy.Client(api_key=self.env["RN_API_KEY"])
        else:
            raise ValueError("You're missing the RN_API_KEY in your .env.secret file.")

        asyncio.ensure_future(self.async_setup(room_id, name, instance_type))

    async def async_setup(self, room_id, name, instance_type):

        self.load_cache()

        try:
            self.cache[str(room_id)]
        except KeyError:
            fetched_room = await self.RecNet.rooms.fetch(room_id)
            try:
                fetched_room = {
                    "name": fetched_room.name,
                    "image": fetched_room.image_name,
                }
            except AttributeError:
                fetched_room = None
            self.cache[str(room_id)] = fetched_room
            print("Cached new room data")
            self.save_cache()
        else:
            fetched_room = self.cache.get(str(room_id))

        self.name = (
            name
            if fetched_room is None and instance_type == 2
            else (fetched_room["name"] if fetched_room else "Private Room")
        )
        self.image = (
            self.default_dorm_image
            if fetched_room is None and instance_type == 2
            else (
                "https://img.rec.net/" + fetched_room["image"] + "?cropSquare=True"
                if (fetched_room)
                else self.default_private_image
            )
        )

    def load_cache(self, filename="cache.json"):
        """
        Loads temporary cache from cache.json
        """
        try:
            with open(filename, "r", encoding="UTF-8") as f:
                self.cache = json.load(f)
        except FileNotFoundError:
            self.cache = {}

    def save_cache(self, filename="cache.json"):
        """
        Writes to the cache.json file from the temporary cache
        """

        with open(filename, "w", encoding="UTF-8") as out:
            json.dump(self.cache, out, indent=4)


class Event:
    """
    Event data handling
    """

    cache = {}

    env = dotenv_values(".env.secret")

    async def async_setup(self, event_id):

        if event_id in self.cache:
            fetched_event = self.cache.get(event_id)
        else:
            fetched_event = await self.RecNet.events.fetch(event_id)
            self.cache[event_id] = fetched_event
            print("Saved new event to cache")

        self.name = fetched_event.name

        if fetched_event.image_name is None:
            try:
                room = await fetched_event.get_room()
                self.image = (
                    "https://img.rec.net/" + room.image_name + "?cropSquare=True"
                )
            except AttributeError:
                self.image = "https://img.rec.net/DefaultRoomImage.jpg?cropSquare=True"

    def __init__(self, event_id):

        if "RN_API_KEY" in self.env:
            self.RecNet = recnetpy.Client(api_key=self.env["RN_API_KEY"])
        else:
            raise ValueError("You're missing the RN_API_KEY in your .env.secret file.")
        asyncio.ensure_future(self.async_setup(event_id))


def setup():
    try:
        with open("accountInfo.json", "r", encoding="UTF-8") as openfile:
            data = json.load(openfile)
    except FileNotFoundError:
        username = input("Please enter your username: \n")

        try:
            userID = requests.get(
                f"https://apim.rec.net//accounts/account?username={username}"
            ).json()["accountId"]
        except KeyError:
            print("Invalid username provided")
            exit()

        data = {"userID": userID, "username": username}

        with open("accountInfo.json", "w", encoding="UTF-8") as outfile:
            json.dump(data, outfile)
        print("New user data has been written")
        return data
    else:
        print("User file found and loaded")
        return data
