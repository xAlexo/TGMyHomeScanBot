from contextlib import suppress
from datetime import datetime
from functools import partial
from logging import getLogger

from telethon import TelegramClient
from telethon.errors import MessageNotModifiedError
from telethon.events import NewMessage
from telethon.tl.types import Message

from config import ALLOW_IDS
from contrib.scan_type import ScanType
from contrib.default_buttons import buttons
from use_cases.scan import scan

last_update = datetime.utcnow()


async def progress(event, msg, data, f=None):
    global last_update
    c: TelegramClient = event.client

    with suppress(MessageNotModifiedError):
        delta = (datetime.utcnow() - last_update).total_seconds()
        if delta > 1:
            if not f:
                await c.edit_message(event.chat_id, msg,
                                     f'Сканирование: {data}')
            if f:
                await c.edit_message(event.chat_id, msg,
                                     f'Выгрузка: {data / f * 100:>6.2f}%')

            last_update = datetime.utcnow()


async def default(event: NewMessage.Event):
    c: TelegramClient = event.client

    await event.delete()

    if event.chat_id not in ALLOW_IDS:
        return await event.respond(
            f'Вашего ID: {event.chat_id} нет в списке разрешённых, '
            f'обратитесь к администратору', buttons=buttons)

    try:
        st = event.pattern_match.groupdict()['ScanType']
        dpi = event.pattern_match.groupdict()['dpi']
        msg: Message = await event.respond('Сканирую...')
        pf = partial(progress, event, msg)

        try:
            fn = await scan(ScanType(st).name, dpi, pf)
            if not fn:
                return await c.edit_message(
                    event.chat_id, msg, 'Сканер занят!')

            await c.edit_message(event.chat_id, msg, 'Отправка')
            await c.send_file(
                event.chat_id, file=fn, force_document=True, buttons=buttons,
                progress_callback=pf
            )
            await c.delete_messages(event.chat_id, msg)
        except (FileNotFoundError, ValueError) as e:
            return await event.client.edit_message(
                event.chat_id, msg.id, f'Проблема со сканером: {e}')
    except (ValueError, KeyError) as e:
        getLogger().exception(e)
        await event.respond('Параметры не распознаны')
