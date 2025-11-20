from asyncio import run, gather
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.twitch import TwitchBot
from services.yandex import YandexClient

import config
import logging
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

scheduler = AsyncIOScheduler(timezone=pytz.UTC)
config.validate_config()

async def main():
    yandexClient = await YandexClient.create(logger)
    twitchClient = TwitchBot(logger, yandexClient)

    await gather(
        yandexClient.polling_updater(), twitchClient.start()
    )

if __name__ == "__main__": run(main())