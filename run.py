import asyncio
from logging import getLogger

from main import factory


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    client = factory(loop)

    try:
        getLogger().info('Запуск бота')
        client.run_until_disconnected()
    except Exception as e:
        getLogger().exception(e)
    finally:
        loop.stop()
