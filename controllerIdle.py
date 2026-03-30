#!/usr/bin/env python
import evdev
import time
import datetime
import sys
import subprocess
from pprint import pprint
from select import select

# TODO autoscan for correct input events by name

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
# for device in devices:
#     print(device.path, device.name, device.phys)

# event 23 is the motion controls which we won't rely on cause I don't use them
# and trying to figure out a good value to set as the dead zone is confusing
controller = map(evdev.InputDevice, ('/dev/input/event24', '/dev/input/event22'))
devices = {dev.fd: dev for dev in controller}

last_valid_input = datetime.datetime.now()

tolerences = {
    0: {
        "key": "ABS_X",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": -32768,
        "max": 32768,
    },
    1: {
        "key": "ABS_Y",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": -32768,
        "max": 32768,
    },
    2: {
        "key": "ABS_Z",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": -32768,
        "max": 32768,
    },
    3: {
        "key": "ABS_RX",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": -2097152,
        "max": 2097152,
    },
    4: {
        "key": "ABS_RY",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": -2097152,
        "max": 2097152,
    },
    5: {
        "key": "ABS_RZ",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": -2097152,
        "max": 2097152,
    }
}

joysticks = {
    0: {
        "key": "ABS_X",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": 0,
        "max": 255
    },
    1: {
        "key": "ABS_Y",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": 0,
        "max": 255
    },
    2: {
        "key": "ABS_Z",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": 0,
        "max": 255
    },
    3: {
        "key": "ABS_RX",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": 0,
        "max": 255
    },
    4: {
        "key": "ABS_RY",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": 0,
        "max": 255
    },
    5: {
        "key": "ABS_RZ",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": 0,
        "max": 255
    },
    16: {
        "key": "ABS_HAT0X",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": -1,
        "max": 1
    },
    17: {
        "key": "ABS_HAT0Y",
        "detectedMin": sys.maxsize,
        "detectedMax": -sys.maxsize -1,
        "min": -1,
        "max": 1
    }
}

for dev in devices.values(): print(dev)

#for dev in devices.values():
#    pprint(dev.capabilities(verbose=True))

def validInput():
    last_valid_input = datetime.datetime.now()
    # print(f"{last_valid_input} Detected valid input")

def process_event(event, device):
    match event.type:
        case 1:
            validInput()
            # print("Button event")
        case 3:
            #print("EV event")
            #if (device.name == "DualSense Wireless Controller Motion Sensors"):
            #    if (event.value < tolerences[event.code]["detectedMin"]):
            #        tolerences[event.code]["detectedMin"] = event.value
            #    if (event.value > tolerences[event.code]["detectedMax"]):
            #        tolerences[event.code]["detectedMax"] = event.value
                #print(event)
            if (device.name == "DualSense Wireless Controller"):
                if (event.code >= 0 and event.code <= 5):
                    if (abs(127.5 - event.value) > 4):
                        validInput()
                else:
                    validInput()
                # if (event.value < tolerences[event.code]["detectedMin"]):
                #     tolerences[event.code]["detectedMin"] = event.value
                # if (event.value > tolerences[event.code]["detectedMax"]):
                #     tolerences[event.code]["detectedMax"] = event.value

while  True:
    if (datetime.datetime.now() >= last_valid_input + datetime.timedelta(minutes=5)):
        break
    r, w, x = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            # print(event)
            process_event(event, devices[fd])

print(f"{datetime.datetime.now()} Idle time exceeded quiting")
print(subprocess.run(["bluetoothctl", "disconnect", "58:10:31:E0:9B:DD"]))
#pprint(tolerences)

# use pybluez to disconnect controller when no valid input is detected

"""
motion controller 1 min test output with table vibrations
{0: {'detectedMax': 3276,
     'detectedMin': -4009,
     'key': 'ABS_X',
     'max': 32768,
     'min': -32768},
 1: {'detectedMax': 32746,
     'detectedMin': -5323,
     'key': 'ABS_Y',
     'max': 32768,
     'min': -32768},
 2: {'detectedMax': 7481,
     'detectedMin': -2809,
     'key': 'ABS_Z',
     'max': 32768,
     'min': -32768},
 3: {'detectedMax': 28134,
     'detectedMin': -42799,
     'key': 'ABS_RX',
     'max': 2097152,
     'min': -2097152},
 4: {'detectedMax': 8108,
     'detectedMin': -6487,
     'key': 'ABS_RY',
     'max': 2097152,
     'min': -2097152},
 5: {'detectedMax': 16682,
     'detectedMin': -23999,
     'key': 'ABS_RZ',
     'max': 2097152,
     'min': -2097152}}
"""

"""
controller test output
sticks are supposed to be about 60 degrees range of motion 4.25 would be 1 degree
so adding a dead zone of 4 should only remove .5 degree in either direction and
currently some of the sticks rare showing 2.5 in stick drift
{0: {'detectedMax': -9223372036854775808,
     'detectedMin': 9223372036854775807,
     'key': 'ABS_X',
     'max': 32768,
     'min': -32768},
 1: {'detectedMax': -9223372036854775808,
     'detectedMin': 9223372036854775807,
     'key': 'ABS_Y',
     'max': 32768,
     'min': -32768},
 2: {'detectedMax': -9223372036854775808,
     'detectedMin': 9223372036854775807,
     'key': 'ABS_Z',
     'max': 32768,
     'min': -32768},
 3: {'detectedMax': 126,
     'detectedMin': 125,
     'key': 'ABS_RX',
     'max': 2097152,
     'min': -2097152},
 4: {'detectedMax': 130,
     'detectedMin': 129,
     'key': 'ABS_RY',
     'max': 2097152,
     'min': -2097152},
 5: {'detectedMax': -9223372036854775808,
     'detectedMin': 9223372036854775807,
     'key': 'ABS_RZ',
     'max': 2097152,
     'min': -2097152}}
"""
