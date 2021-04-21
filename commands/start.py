# Lineart|Gray|Color
from telethon import Button
from telethon.events import NewMessage


async def start(event: NewMessage.Event):
    buttons = [
        [
            Button.text('Серый 300'),
            Button.text('Цветной 300'),
        ],
        [
            Button.text('Серый 600'),
            Button.text('Цветной 600'),
        ],
        [
            Button.text('Серый 1200'),
            Button.text('Цветной 1200'),
        ]
    ]
    await event.respond('Положите документ в сканер и выберите:', buttons=buttons)
