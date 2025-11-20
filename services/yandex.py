from logging import Logger
from typing import Optional 
from yandex_music import ClientAsync
import aiohttp
from asyncio import sleep
import traceback
import config

class YandexClient:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.token = config.YANDEX_TOKEN
        self.client: Optional[ClientAsync] = None
        self._current_track = None
    
    async def initialize(self):
        if not self.client:
            self.client = await ClientAsync(self.token).init()
            await self.update_current_track()
            self.logger.info("Клиент Я.Музыки авторизован")
    
    @classmethod
    async def create(cls, logger: Logger):
        instance = cls(logger)
        await instance.initialize()
        return instance

    async def polling_updater(self):
        while True:
            await sleep(3)
            await self.update_current_track()

    async def update_current_track(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    "http://track.mipoh.ru/get_current_track_beta", 
                    headers={"ya-token": self.token}
                ) as response:
                    data = await response.json()

                    track_id = data["track"]["track_id"]
                    track = (await self.client.tracks(track_id))[0]

                    artists = ", ".join(i["name"] for i in track["artists"])
                    title = track["title"]

                    self._current_track = f"{artists} — {title}"
            except:
                self.logger.error(traceback.format_exc())
    


        
    
    