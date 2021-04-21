from telethon import TelegramClient
from telethon.events import NewMessage

from config import TG_API_HASH, TG_APP_ID, TG_APP_TITLE, TG_BOT_API_TOKEN


def factory(loop):
    client = TelegramClient(TG_APP_TITLE, TG_APP_ID, TG_API_HASH, loop=loop)

    load_commands(client)

    client.start(bot_token=TG_BOT_API_TOKEN)

    return client


def load_commands(client):
    from commands.start import start
    client.add_event_handler(start, NewMessage(pattern='/start'))

    from commands.default import default
    client.add_event_handler(default, NewMessage(
        pattern=r'(?P<ScanType>.*?)\s(?P<dpi>\d+)', incoming=True))

