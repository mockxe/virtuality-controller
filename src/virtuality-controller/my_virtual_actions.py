import asyncio

from evdev import ecodes, UInput, InputEvent


async def vol_down(virtual_device: UInput, event: InputEvent):
    if event.value == 1:
        virtual_device.write(ecodes.EV_KEY, ecodes.BTN_TRIGGER_HAPPY1, 1)
        virtual_device.syn()

        await asyncio.sleep(0.5)

        virtual_device.write(ecodes.EV_KEY, ecodes.BTN_TRIGGER_HAPPY1, 0)
        virtual_device.syn()


async def vol_up(virtual_device: UInput, event: InputEvent):
    if event.value == 1:
        virtual_device.write(ecodes.EV_KEY, ecodes.BTN_TRIGGER_HAPPY2, 1)
        virtual_device.syn()

        await asyncio.sleep(0.5)

        virtual_device.write(ecodes.EV_KEY, ecodes.BTN_TRIGGER_HAPPY2, 0)
        virtual_device.syn()
