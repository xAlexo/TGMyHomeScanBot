import asyncio
import shlex
from asyncio import Lock
from asyncio.subprocess import Process
from uuid import uuid4

from loguru import logger as _log
from parse import compile

from config import SCANNER

parse_progress = compile('Progress: {p}%')
scan_lock = Lock()

async def sane_list_devices():
    cmd = '/usr/bin/scanimage --list-devices'
    process: Process = await asyncio.create_subprocess_exec(
        *shlex.split(cmd),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    out, err = await process.communicate()
    if process.returncode != 0:
        _log.error(f'Ошибка при получении списка устройств: {err.decode().strip()}')
        return []

    devices = out.decode().strip().split('\n')
    return [device.strip() for device in devices if device.strip()]


async def scan(scan_type: str, dpi: int, progress: callable):
    name = uuid4().hex
    fn = f'/tmp/{name}.png'
    cmd = f'/usr/bin/scanimage -d "{SCANNER}" ' \
          f'--format png --progress --output-file {fn} ' \
          f'--mode {scan_type} --resolution {dpi}dpi'

    if scan_lock.locked():
        _log.debug('Scan is already in progress')
        return False

    async with scan_lock:
        process: Process = await asyncio.create_subprocess_exec(
            *shlex.split(cmd),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        line = b''
        while b := await process.stdout.read(1):
            line += b
            if b != b'\r':
                continue

            line = line.decode()
            if p := parse_progress.search(line):
                p = float(p['p'])
                await progress(f'{p: >6.2f}%')
                continue

            if line.count('sane_read: Error during device I/O'):
                raise ValueError('Ошибка сканирования!')

            if line.count('no SANE devices found'):
                raise ValueError('Сканер не найден')

            _log.debug(f'Scan output: {line.strip()}')

        if process.returncode == 0:
            return fn

        out, err = await process.communicate()
        _log.debug(f'Scan output: {out!r}, {err!r}')
        return False
