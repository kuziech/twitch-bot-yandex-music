import os
from dotenv import load_dotenv

load_dotenv()

# Twitch
TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_NICK = os.getenv('TWITCH_NICK')
TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL')

# Я.Музыка
YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')

# Команды
SONG_COMMAND = os.getenv('SONG_COMMAND', '!песня')

def validate_config():
    required = {
        'TWITCH_TOKEN': TWITCH_TOKEN,
        'TWITCH_CLIENT_ID': TWITCH_CLIENT_ID,
        'TWITCH_NICK': TWITCH_NICK,
        'TWITCH_CHANNEL': TWITCH_CHANNEL,
        'YANDEX_TOKEN': YANDEX_TOKEN
    }
    
    missing = [key for key, value in required.items() if not value]
    
    if missing:
        raise ValueError(f"Отсутствуют обязательные настройки: {', '.join(missing)}")
    
    return True
