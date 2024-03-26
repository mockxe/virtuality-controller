# virtuality-controller

A python tool which creates a virtual input device, enabling the creation of input actions through highly customizable 
virtual action scripts. It allows users with basic python skills the creation of complex macros and custom input 
configurations by listening to actual device inputs and generating virtual device outputs. virtuality-controller is a
more flexible alternative to conventional macro editors and companion apps of game controllers and other input devices,
which are often not available on linux or barely work (on any OS).

Since the project relies on `evdev` it's only available for linux.


## installation

The project is set up using [pdm](https://pdm-project.org/), if you have pdm installed run `pdm install` in the
repository root. This should set up a venv and the necessary dependencies.

You can run the script with `pdm start`


## usage

Currently, there are no configurations or similar, everything is configured through code. This may or may not change in
the future. The repo already contains my personal setup, you can extend it in any way you like, the basics are explained
below.


### 1. get real input device

Firstly, you need to get your real input devices you want to listen and react to. You can listen to any number of input
devices, but currently a virtual action can only react to a single event at the time, so it's not possible to react to
key combinations.

```python
# get device(s) you want to listen to
device = manual_device_selection()
```

The included main.py contains a manual device selection, which takes a single devices given via command line argument.
E.g. `pdm start /dev/input/event26`


### 2. register virtual actions

Next up, virtual actions have to be registered. This is explained in further detail below, but in general you have to
give a name, define which input events it will react to, which input events it might send and what the actual function
is that should be executed on an input event. Again, you can find an example in the included main.py

```python
# register all your virtual actions here
virtual_actions: List[VirtualAction] = [
    VirtualAction(
        "Volume Down",
        {ecodes.EV_KEY: [ecodes.BTN_TRIGGER_HAPPY7]},
        {ecodes.EV_KEY: [ecodes.BTN_TRIGGER_HAPPY1]},
        my_virtual_actions.vol_down
    ),
    VirtualAction(
        "Volume Up",
        {ecodes.EV_KEY: [ecodes.BTN_TRIGGER_HAPPY6]},
        {ecodes.EV_KEY: [ecodes.BTN_TRIGGER_HAPPY2]},
        my_virtual_actions.vol_up
    ),
]
```


### 3. start listening for input events

Finally, you can register the virtual input device and start to listen for input events on your real input devices. It's
important to use pythons context manager (the `with`-block) as it takes care of gracefully closing the virtual device
when stopping the script. You could listen to multiple devices using threading, but the included main.py only listens to
a single device.

```python
# create out virtual input device
with virtuality.create_virtual_device(virtual_actions):
    # start listening to all devices
    virtuality.listen(device, virtual_actions)
```


## defining virtual actions

A new VirtualAction takes four arguments, a name, input events, output events and a function. 


**name**

The name serves just as an identifier for the virtual action and is printed in the log.


**input_events**

A dictionary with three keys representing the supported action types: `ecodes.EV_KEY`, `ecodes.EV_REL` and 
`ecodes.EV_ABS`. Each key takes a list of key codes, also found in `ecodes`. The action will be triggered for any event 
with this type / keycode combination. Further filtering for the value needs to be implemented manually in the function.
If you are unsure which event you need to react to use `evtest` to monitor what your input device is doing (This can
also serve as an entry point for designing your output events). Detailed information can be found in the [kernel 
documentation](https://www.kernel.org/doc/html/latest/input/event-codes.html).


**output_events**

Similar to input_events, this is a dict of the same format, but serving a different purpose. All events listed here will
be added when the virtual device is registered. If two functions send the same events, it's not strictly necessary to
mention the codes again, but it's strongly recommend, already for documentation purposes. You can freely write to any
keycode from your function, but the virtual device might not work as expected, if the output events are not properly
registered. Please note that `BTN_TRIGGER` from `EV_KEY`, as well as `ABS_X` and `ABS_Y` from `EV_ABS` will always be
registered, even when not in use by a virtual action (in this case without any function) as those are the minimal
requirement for the device to be picked up as game controller by other applications.


**function**

This defines the actual function which can react to the input event. The function has two arguments, the 
`virtual_device` to send out new input events and the actual input `event` which triggered the virtual action. You can
add any additional filtering for event values (or event codes if you react to multiple with same action) at the very 
beginning of the function. Virtual input events can be sent to the virtual device, details can be found in the [evdev
python documentation](https://python-evdev.readthedocs.io/en/latest/apidoc.html#evdev.uinput.UInput). For a simple
example, have a look at `my_virtual_actions.py`


## about the name

The name - virtuality-controller - got inspired by the virtuality headsets from Cyberpunk RED, which adds
a layer on top of the real world to access the virtual world.


## special thanks

 - https://github.com/beniwtv/evdev-spoof-device for giving insights how to create a virtual controller that is actually
picked up by games
