# Twitch Bot с интеграцией Яндекс.Музыки

Twitch бот для отображает текущего трека из Яндекс.Музыки по команде в чате.

## Возможности

- Отображение текущего трека из Яндекс.Музыки
- Автоматическое обновление информации о треке каждые 3 секунды
- Команды в чате Twitch

## Требования

- Python 3.10+
- Токен Twitch Bot
- Токен Яндекс.Музыки

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd my
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

4. Получите токены:

**Twitch токен:**
- Перейдите на https://twitchapps.com/tmi/
- Авторизуйтесь и скопируйте токен

**Яндекс.Музыка токен:**
- Перейдите по ссылке: https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d
- Авторизуйтесь
- Токен будет в адресной строке после `access_token=`

5. Заполните `.env` своими токенами и настройками:
```env
TWITCH_TOKEN=your_twitch_oauth_token_here
TWITCH_CLIENT_ID=your_twitch_client_id_here
TWITCH_NICK=your_bot_nickname
TWITCH_CHANNEL=target_channel_name
YANDEX_TOKEN=your_yandex_music_token_here
SONG_COMMAND=!песня
```

## Запуск

```bash
python main.py
```

## Команды

- `!песня` (или настроенная команда) - показывает текущий трек из Яндекс.Музыки

## Структура проекта

```
my/
├── config.py          # Конфигурация и переменные окружения
├── main.py            # Точка входа приложения
├── requirements.txt   # Зависимости проекта
├── services/
│   ├── twitch.py     # Twitch бот
│   └── yandex.py     # Клиент Яндекс.Музыки
└── .env              # Переменные окружения
```

## Лицензия

MIT
