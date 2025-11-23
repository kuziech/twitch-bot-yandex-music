from logging import Logger
from time import time
from twitchio.ext import commands
from twitchio import Message
from services.yandex import YandexClient
import config
import traceback
from asyncio import sleep
from aiohttp import ClientSession

class TwitchBot(commands.Bot):
    def __init__(self, logger: Logger, yandexClient: YandexClient) -> None:
        self.logger = logger
        self.yandexClient = yandexClient
        self.timeCooldown = time() - 30
        self.session = None
        
        super().__init__(
            token=config.TWITCH_TOKEN,
            client_id=config.TWITCH_CLIENT_ID,
            nick=config.TWITCH_NICK,
            prefix='!',
            initial_channels=[config.TWITCH_CHANNEL]
        )
        self.session = ClientSession()
        

    async def polling_reminder(self) -> None:
        while True:
            await sleep(60*10)
            channel = self.get_channel(config.TWITCH_CHANNEL)
            await channel.send(f"{config.TEXT_TG}")

    async def event_ready(self) -> None:
        self.logger.info(
            f"Бот {self.nick} подключен к каналу "
            f"{config.TWITCH_CHANNEL}"
        )
    
    async def event_message(self, message: Message) -> None:
        if message.echo: return
        
        source_room_id = message.tags.get('source-room-id')
        room_id = message.tags.get('room-id')
        if source_room_id and source_room_id != room_id: return
        
        print(source_room_id, room_id)
        await self.handle_commands(message)


    @commands.command(name=config.SONG_COMMAND[1:])
    async def song_command(self, ctx: commands.Context) -> None:
        try:
            name = ctx.author.name
            self.logger.info(f"{name}: {config.SONG_COMMAND}")
            await ctx.send(f"@{name} {self.yandexClient._current_track}")
        except:
            self.logger.error(
                f"Ошибка при обработке команды {config.SONG_COMMAND}: "
                f"{traceback.format_exc()}"
            )
    
    @commands.command(name=config.PLIP_COMMAND[1:])
    async def plip_command(self, ctx: commands.Context) -> None:
        try:
            name = ctx.author.name
            self.logger.info(f"{name}: {config.PLIP_COMMAND}")
            await ctx.send(f"@{name} иди нахуй.")
        except:
            self.logger.error(
                f"Ошибка при обработке команды плип: "
                f"{traceback.format_exc()}"
            )

    @commands.command(name=config.TG_COMMAND[1:])
    async def tg_command(self, ctx: commands.Context) -> None:
        try:
            name = ctx.author.name
            self.logger.info(f"{name}: {config.TG_COMMAND}")
            await ctx.send(f"@{name} {config.TEXT_TG}")
        except:
            self.logger.error(
                f"Ошибка при обработке команды тг: "
                f"{traceback.format_exc()}"
            )
    
    @commands.command(name=config.CLIP_COMMAND[1:])
    async def clip_command(self, ctx: commands.Context) -> None:
        try:
            name = ctx.author.name
            self.logger.info(f"{name}: {config.CLIP_COMMAND}")
            if self.timeCooldown+30 > time(): return

            headers = {
                "Authorization": f"Bearer {config.TWITCH_TOKEN.replace('oauth:', '')}",
                "Client-Id": config.TWITCH_CLIENT_ID
            }

            async with self.session.get(
                f"https://api.twitch.tv/helix/users?login={config.TWITCH_CHANNEL}",
                headers=headers
            ) as resp:
                data = await resp.json()
                broadcaster_id = data["data"][0]["id"]
            
            clip_data = {"broadcaster_id": broadcaster_id}
            async with self.session.post(
                'https://api.twitch.tv/helix/clips',
                headers=headers,
                json=clip_data
            ) as resp:
                if resp.status == 202:
                    clip_info = await resp.json()
                    clip_id = clip_info['data'][0]['id']

                    clip_url = f"https://clips.twitch.tv/{clip_id}"
                    self.timeCooldown = time()
                    await ctx.send(f"@{name} Клип создан: {clip_url}")
                else:
                    text = await resp.text()
                    self.logger.error(f"{name}: Ошибка при создании клипа: {text}")
        except:
            self.logger.error(
                f"Ошибка при обработки команды клип: "
                f"{traceback.format_exc()}"
            )

        
    
        
