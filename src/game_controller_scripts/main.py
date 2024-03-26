import sys

from evdev import ecodes, UInput, InputDevice, list_devices

import virtual_actions


def main():
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

    # create out virtual input device
    with create_virtual_device(device) as virtual_device:
        listen(device, virtual_device)


def listen(device: InputDevice, virtual_device: UInput):
    print(f"listening to '{device.name}'")

    for event in device.read_loop():
        # TODO refactor: better method for mapping buttons to actions
        if event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_TRIGGER_HAPPY6 and event.value == 1:
                print("registered volume +")
                virtual_actions.vol_up(virtual_device)

            if event.code == ecodes.BTN_TRIGGER_HAPPY7 and event.value == 1:
                print("registered volume -")
                virtual_actions.vol_down(virtual_device)


def create_virtual_device(device: InputDevice) -> UInput:
    # required events for the controller to show up as game controller
    events = {
        ecodes.EV_ABS: [ecodes.ABS_X, ecodes.ABS_Y],  # create a fake absolute X- and Y-axis
        ecodes.EV_KEY: [ecodes.BTN_TRIGGER],  # create a fake single trigger button
    }

    virtual_device = UInput(
        events=events,
        name="Virtual Controller",
    )

    print("registered new virtual input device")
    return virtual_device


if __name__ == "__main__":
    main()
