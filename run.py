import asyncio

from loguru import logger as _log

from main import factory

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = factory(loop)

    try:
        _log.info('Запуск бота')
        client.run_until_disconnected()
    except Exception as e:
        _log.exception(e)
    finally:
        loop.stop()
