import asyncio
import sys
from typing import List

from evdev import ecodes, InputDevice, list_devices

import virtuality
from virtual_action import VirtualAction
from controls import StickyTimeout


async def main():
    # get device(s) you want to listen to
    device = manual_device_selection()

    # register all your virtual actions here
    virtual_actions: List[VirtualAction] = [
        VirtualAction(
            "Volume Up",
            {ecodes.EV_KEY: [ecodes.BTN_TRIGGER_HAPPY6]},
            {ecodes.EV_KEY: [ecodes.BTN_TRIGGER_HAPPY1]},
            StickyTimeout(ecodes.BTN_TRIGGER_HAPPY1, 0.2).trigger
        ),
        VirtualAction(
            "Volume Down",
            {ecodes.EV_KEY: [ecodes.BTN_TRIGGER_HAPPY7]},
            {ecodes.EV_KEY: [ecodes.BTN_TRIGGER_HAPPY2]},
            StickyTimeout(ecodes.BTN_TRIGGER_HAPPY2, 0.2).trigger
        ),
    ]

    # create out virtual input device
    with virtuality.create_virtual_device(virtual_actions):
        # start listening to all devices
        await virtuality.listen(device, virtual_actions)


def manual_device_selection():
    # get all devices
    devices = [InputDevice(path) for path in list_devices()]
    # print error and exit when no devices are available
    if not devices:
        print("no evdev devices found")
        sys.exit(1)
    # if no arg/device was give print available devices and exit
    if len(sys.argv) == 1:
        print("available devices:")
        for device in devices:
            print(device.path, device.name)

        sys.exit(1)
    # assign given device
    device = None
    for d in devices:
        if d.name == sys.argv[1] or d.path == sys.argv[1]:
            device = d
            break
    # exit if given device was not found
    if not device:
        print(f"device {sys.argv[1]} not found")
        sys.exit(1)

    return device


if __name__ == "__main__":
    asyncio.run(main())
