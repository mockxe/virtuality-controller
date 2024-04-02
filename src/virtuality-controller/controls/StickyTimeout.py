import asyncio
from asyncio import Task
from typing import Callable

from evdev import ecodes, UInput, InputEvent


class StickyTimeout:
    ecode: int
    timeout: float
    timer: Task | None

    def __init__(self, ecode: int, timeout: float):
        self.ecode = ecode
        self.timeout = timeout
        self.timer = None

    async def trigger(self, virtual_device: UInput, event: InputEvent):
        if event.value == 1:
            if self.timer is not None:
                self.timer.cancel()

            virtual_device.write(ecodes.EV_KEY, self.ecode, 1)
            virtual_device.syn()

            self.timer = asyncio.create_task(self.after_timeout(self.end, virtual_device))

    async def after_timeout(self, on_timeout: Callable[[UInput], None], *args, **kwargs):
        try:
            await asyncio.sleep(self.timeout)
            on_timeout(*args, **kwargs)
        except asyncio.CancelledError:
            pass

    def end(self, virtual_device: UInput):
        virtual_device.write(ecodes.EV_KEY, self.ecode, 0)
        virtual_device.syn()
