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
            p = parse_progress.search(line)
            if p:
                p = float(p['p'])
                await progress(f'{p: >6.2f}%')

            line = b''

        return fn
