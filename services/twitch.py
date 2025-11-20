from logging import Logger
from twitchio.ext import commands
from twitchio import Message
from services.yandex import YandexClient
import config
import traceback

class TwitchBot(commands.Bot):
    def __init__(self, logger: Logger, yandexClient: YandexClient) -> None:
        self.logger = logger
        self.yandexClient = yandexClient
        
        super().__init__(
            token=config.TWITCH_TOKEN,
            client_id=config.TWITCH_CLIENT_ID,
            nick=config.TWITCH_NICK,
            prefix='!',
            initial_channels=[config.TWITCH_CHANNEL]
        )

    async def event_ready(self) -> None:
        self.logger.info(
            f"Бот {self.nick} подключен к каналу "
            f"{config.TWITCH_CHANNEL}"
        )
    
    async def event_message(self, message: Message) -> None:
        if message.echo: return
        await self.handle_commands(message)

    @commands.command(name=config.SONG_COMMAND[1:])
    async def sond_commands(self, ctx: commands.Context):
        try:
            name = ctx.author.name
            self.logger.info(f"{name}: {config.SONG_COMMAND}")
            await ctx.send(f"@{name} {self.yandexClient._current_track}")
        except:
            self.logger.error(
                f"Ошибка при обработке команды {config.SONG_COMMAND}: "
                f"{traceback.format_exc()}"
            )
    
    @commands.command(name="плип")
    async def plip(self, ctx: commands.Context):
        try:
            name = ctx.author.name
            self.logger.info(f"{name}: !плип")
            await ctx.send(f"@{name} Лали просила передать: иди нахуй.")
        except:
            self.logger.error(
                f"Ошибка при обработке команды плип: "
                f"{traceback.format_exc()}"
            )

        
    
        
