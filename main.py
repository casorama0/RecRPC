import asyncio
import time
import os
from discordrp import Presence
from extras import setup, Room, Event
from matchmaking import info, room_instance





async def main(): 
    """
    Main.
    """
    last = ""
    x = setup()

    client_id = "1124780603200508014"
    RPC = Presence(client_id)

    roomTypes = {
        0: "",  # Public room
        1: " [PRIVATE]",
        2: " [PRIVATE]",  # Dorm Room
        3: " [EVENT]",
        4: "",
        5: " [CLUBHOUSE]",
        6: " [BROADCAST]",
    }

    deviceTypes = {
        0: ["", ""],
        1: ["pcvr", "PCVR"],
        2: ["screen", "Desktop"],
        3: ["cell-phone-svgrepo-com_1", "Mobile"],
        4: ["meta", "Quest 1"], # Quest 1 is no longer supported
        5: ["meta", "Quest 2"]
    }

    while True:
        m = info(x["userID"])
        

        try:
            r = room_instance(m) 
        except:
            RPC.set(
                {
                "state": "Logging In",
                "timestamps": {
                    "start": int(time.time())
                    },
                "assets": {
                    "large_image": "login",
                    "small_image": deviceTypes.get(m.deviceClass)[0],
                    "small_text": deviceTypes.get(m.deviceClass)[1]
                    }
                }
            )

            print("Updated presence: LOGIN")
            time.sleep(15)
            continue
            

        tag = roomTypes.get(r.roomInstanceType)

        # Room Instance Types
        if r.roomInstanceType in (0, 1, 2):  # Standard rooms
            obj = Room(r.roomId, r.name, r.roomInstanceType)
            await obj.async_setup(r.roomId, r.name, r.roomInstanceType)
            
            image = obj.image
            name = obj.name

        elif r.roomInstanceType in (3, 6):
            obj = Event(r.eventId)
            await obj.async_setup(r.eventId)

            image = obj.image
            name = obj.name

        if last != name:
            t = int(time.time())
            last = name

        RPC.set({
            "state": name + tag,
            "timestamps": {
                "start": t
            },
            "assets":{
                "large_image": image,
                "small_image": deviceTypes.get(m.deviceClass)[0],
                "small_text": deviceTypes.get(m.deviceClass)[1]
            },
            "buttons":[
                    {
                        "label": "Profile",
                        "url": f"https://rec.net/user/{x["username"]}"
                    }
                ]
        })
        os.system('cls' if os.name=='nt' else 'clear')
        print(f"Updated Presence:\nRoomID: {r.roomId}\nRoomName: {r.name}")

        time.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())


    

