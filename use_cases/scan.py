from logging import getLogger
from uuid import uuid4

import shlex
import asyncio
from parse import compile

from config import SCANNER
from asyncio import Lock, sleep

parse_progress = compile('Progress: {p}%')
scan_lock = Lock()


async def scan(scan_type: str, dpi: int, progress: callable):
    name = uuid4().hex
    fn = f'/tmp/{name}.png'
    cmd = f'/usr/bin/scanimage -d "{SCANNER}" ' \
          f'--format png --progress --output-file {fn} ' \
          f'--mode {scan_type} --resolution {dpi}dpi'

    if scan_lock.locked():
        getLogger('scan').debug('Scan is already in progress')
        return False

    async with scan_lock:
        process = await asyncio.create_subprocess_exec(
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

            getLogger('scan').debug(f'Scan output: {line.strip()}')

        getLogger('scan').debug(f'Scan output: {process}')
        if process.returncode == 0:
            return fn
