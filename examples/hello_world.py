import trio

import deartriogui
from dearpygui.dearpygui import *


async def main():
    log_info('Hello from Async!')
    for x in range(10):
        log_debug(f'Step {x}')
        await trio.sleep(0.1)
    log_info('Done...')
    await trio.sleep(0.5)
    return 'Hello World'


show_logger()
set_log_level(0)

assert deartriogui.run(main) == 'Hello World'
