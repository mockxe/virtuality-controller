from itertools import chain
from typing import List

from evdev import UInput, InputDevice
from evdev.ecodes import *

from virtual_action import VirtualAction


def listen(device: InputDevice, virtual_actions: List[VirtualAction]):
    print(f"listening to '{device.name}' on '{device.path}'")

    key_actions: List[VirtualAction] = [action for action in virtual_actions if EV_KEY in action.input_events.keys()]
    rel_actions: List[VirtualAction] = [action for action in virtual_actions if EV_REL in action.input_events.keys()]
    abs_actions: List[VirtualAction] = [action for action in virtual_actions if EV_ABS in action.input_events.keys()]

    for event in device.read_loop():
        if event.type == EV_KEY:
            [action.call(event) for action in key_actions if event.code in action.input_events[EV_KEY]]

        elif event.type == EV_REL:
            [action.call(event) for action in rel_actions if event.code in action.input_events[EV_REL]]

        elif event.type == EV_ABS:
            [action.call(event) for action in abs_actions if event.code in action.input_events[EV_ABS]]


def create_virtual_device(virtual_actions: List[VirtualAction]) -> UInput:
    # required events for the controller to show up as game controller
    events = {
        EV_KEY: [BTN_TRIGGER],  # create a fake single trigger button
        EV_REL: [],
        EV_ABS: [ABS_X, ABS_Y],  # create a fake absolute X- and Y-axis
    }

    # extend with registered actions
    events[EV_KEY].extend(event for event in chain.from_iterable(
        [action.output_events[EV_KEY] for action in virtual_actions if EV_KEY in action.output_events.keys()]) if
                          event not in events[EV_KEY])

    events[EV_REL].extend(event for event in chain.from_iterable(
        [action.output_events[EV_REL] for action in virtual_actions if EV_REL in action.output_events.keys()]) if
                          event not in events[EV_REL])

    events[EV_ABS].extend(event for event in chain.from_iterable(
        [action.output_events[EV_ABS] for action in virtual_actions if EV_ABS in action.output_events.keys()]) if
                          event not in events[EV_ABS])

    virtual_device = UInput(
        events=events,
        name="Virtuality Controller",
    )

    print(f"registered new virtual input device at '{virtual_device.device.path}'")

    # register virtual device on all actions
    [action.register(virtual_device) for action in virtual_actions]

    return virtual_device
