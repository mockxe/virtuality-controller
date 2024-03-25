import sys

from evdev import ecodes, UInput, InputDevice, list_devices

import virtual_actions


# TODO implement bullet-proof graceful shutdown
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
    virtual_device = create_virtual_device(device)

    try:
        listen(device, virtual_device)

    except Exception as e:
        print(f"an error occurred: {e}")

    finally:
        unreg_virtual_device(virtual_device)


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


# TODO refactor: figure out what's actually required
def create_virtual_device(device: InputDevice) -> UInput:
    caps = {
        ecodes.EV_MSC: [ecodes.MSC_SCAN],
    }

    if ecodes.EV_ABS in device.capabilities():
        caps[ecodes.EV_ABS] = device.capabilities()[ecodes.EV_ABS]
    else:
        # Some devices do not have axis, so fake at least two axis
        caps[ecodes.EV_ABS] = [ecodes.ABS_X, ecodes.ABS_Y]

    if ecodes.EV_KEY in device.capabilities():
        caps[ecodes.EV_KEY] = device.capabilities()[ecodes.EV_KEY]
    else:
        # Some devices do not have buttons, so fake at least one button
        caps[ecodes.EV_KEY] = [ecodes.BTN_JOYSTICK, ecodes.BTN_TRIGGER]

    virtual_device = UInput(
        events=caps,
        name="Virtual Controller",
        vendor=device.info.vendor,
        product=device.info.product,
        version=device.info.version
    )

    print("registered new virtual input device")
    return virtual_device


def unreg_virtual_device(virtual_device: UInput):
    virtual_device.close()
    print("unregistered virtual input device")


if __name__ == "__main__":
    main()
