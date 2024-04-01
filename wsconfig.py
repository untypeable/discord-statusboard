import json

WS_URL = "wss://gateway-us-east1-c.discord.gg?v=10&encoding=json"
BOT_TOKEN = ""

MSG_HELLO = {
   "op":2,
   "d":{
      "token": BOT_TOKEN,
      "capabilities": 4093,
      "properties":{
         "client_build_number": 279687,
         "client_event_source": None,
         "design_id":0
      },
      "compress": False,
   }
}; S_MSG_HELLO = json.dumps(MSG_HELLO)

MSG_HEARTBEAT = {
    "op": 1,
    "d": {
        "token": BOT_TOKEN,
        "properties":{
            "client_build_number": 279687,
            "client_event_source": None,
            "release_channel": "stable"
        },
    }
}; S_MSG_HEARTBEAT = json.dumps(MSG_HEARTBEAT)

HTTP_HEADERS = {
    "authorization": BOT_TOKEN
}
