import asyncio
from typing import List, Callable, Dict, Awaitable

from evdev import UInput, InputEvent


class VirtualAction:
    virtual_device: UInput | None
    name: str
    input_events: Dict[int, List[int]]
    output_events: Dict[int, List[int]]
    function: Callable[[UInput, InputEvent], Awaitable[None]]

    def __init__(
            self,
            name: str,
            input_events: Dict[int, List[int]],
            output_events: Dict[int, List[int]],
            function: Callable[[UInput, InputEvent], Awaitable[None]]
    ):
        self.virtual_device = None
        self.name = name
        self.input_events = input_events
        self.output_events = output_events
        self.function = function

    def call(self, event: InputEvent) -> None:
        if not self.virtual_device:
            print(f"error - call to unregistered action '{self.name}'")

        else:
            print(f"action '{self.name}' was called with {event}")
            asyncio.create_task(self.function(self.virtual_device, event))

    def register(self, virtual_device: UInput) -> None:
        self.virtual_device = virtual_device
        print(f"action '{self.name}' registered on '{virtual_device.name}' at '{virtual_device.device.path}'")
