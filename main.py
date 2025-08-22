from loguru import logger as _log
from telethon import TelegramClient
from telethon.events import NewMessage

from config import TG_API_HASH, TG_APP_ID, TG_APP_TITLE, TG_BOT_API_TOKEN
from use_cases.scan import sane_list_devices


def factory(loop):
    client = TelegramClient(TG_APP_TITLE, TG_APP_ID, TG_API_HASH, loop=loop)

    load_commands(client)

    client.start(bot_token=TG_BOT_API_TOKEN)
    if devives := loop.run_until_complete(sane_list_devices()):
        _log.debug(f'Найдено устройств сканера: {len(devives)}')
        _log.debug(f'Список устройств: {devives}')
        return client

    raise RuntimeError('Не удалось получить список устройств сканера!')


def load_commands(client):
    from commands.start import start
    client.add_event_handler(start, NewMessage(pattern='/start'))

    from commands.default import default
    client.add_event_handler(default, NewMessage(
        pattern=r'(?P<ScanType>.*?)\s(?P<dpi>\d+)', incoming=True))

