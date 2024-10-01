![RecRPC1](https://github.com/user-attachments/assets/5523ed9a-0879-4ec0-8b30-416350534f88)


RecRPC is a cross-platform Discord rich presence client for Rec Room. It hides private room information, and has the ability to distinguish your instance type between things like events, broadcast events, clubhouses, and more. Also has caching to prevent repeated calls to the RecNet API.

## Disclaimers / What to know:
* ‼️This requires a valid [RecNet API Key](https://devportal.rec.net)‼️
* This uses your RecNet authorization token to obtain data from the matchmaking API
   * Follow [RecNetLogin's setup guide](https://github.com/Jegarde/RecNet-Login?tab=readme-ov-file#setup) for obtaining the proper session token
* This is largely an off and on project for me. The programming might be a little wonky in some areas, but everything seems to work at the moment.
* Alt accounts are supported

## Setup

* Create a file called `.env.secret` in the same directory as `main.py`

The .env.secret file should be setup in the following way:  
```
RN_SESSION_TOKEN=YOUR_SESSION_TOKEN  
RN_API_KEY=YOUR_API_KEY
```
Find out how to grab your SessionToken [here](https://github.com/Jegarde/RecNet-Login?tab=readme-ov-file#setup)  
Grab an API Key from [here](https://devportal.rec.net)  

* Your first run of the program should automatically generate a `accountInfo.json` file. Make sure you enter the correct username, otherwise the presence data will reflect a different user's.
  * If you enter the incorrect username, delete the `accountInfo.json` file. You will be prompted to enter your username the next time you run the program.
* Notice a room's image / name is out of date due to caching?:
  * Delete the `cache.json` file (not recommended!)
  * Find the individual room's entry inside of the `cache.json` file and remove it (recommended!)


