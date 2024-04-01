import websockets
import json
import wsconfig
import asyncio
import requests
from PyQt6.QtCore import QThread

class DiscordWorker(QThread):
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.lock = None
        self.websocket = None
        self.heartbeat_worker = None
        self.msg_events = []
        self.timeout = 41
        QThread.__init__(self)

    async def msg_loop(self):
        self.websocket = await websockets.connect(wsconfig.WS_URL, max_size=5_000_000)
        await self.websocket.send(wsconfig.S_MSG_HELLO)
        asyncio.create_task(self.heartbeat_loop())
        while True:
            message = json.loads(await self.websocket.recv())
            if message["op"] == 10:
                self.timeout = message["d"]["heartbeat_interval"] / 1_000
                continue
            if message["t"] != "MESSAGE_CREATE": continue
            for event in self.msg_events: event(message)
    
    async def heartbeat_loop(self):
        while True:
            await self.websocket.send(wsconfig.S_MSG_HEARTBEAT)
            await asyncio.sleep(self.timeout)
            print("[discordbot] heartbeat")

    def run(self):
        asyncio.set_event_loop(self.loop)
        task = self.loop.create_task(self.msg_loop())
        self.loop.run_until_complete(task)

def get_guild_channels(guild_id : str):
    req = requests.get("https://discord.com/api/guilds/{}/channels".format(guild_id), headers=wsconfig.HTTP_HEADERS)
    print("HTTP {} {}".format(req.status_code, req.url))
    return req.json()

def get_user_guilds():
    req = requests.get("https://discordapp.com/api/users/@me/guilds", headers=wsconfig.HTTP_HEADERS)
    print("HTTP {} {}".format(req.status_code, req.url))
    return req.json()


GUILDS = get_user_guilds()
