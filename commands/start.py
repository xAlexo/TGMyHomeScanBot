from telethon.events import NewMessage

from contrib.default_buttons import buttons


async def start(event: NewMessage.Event):
    await event.respond(
        'Положите документ в сканер и выберите:', buttons=buttons)
