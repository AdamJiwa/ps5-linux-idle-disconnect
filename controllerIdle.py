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

for dev in devices.values(): print(dev)

#for dev in devices.values():
#    pprint(dev.capabilities(verbose=True))

def validInput(event):
    global last_valid_input
    last_valid_input = datetime.datetime.now()
    # print(f"{last_valid_input} Detected valid input {event}")

def process_event(event, device):
    match event.type:
        case 1:
            validInput(event)
        case 3:
            if (device.name == "DualSense Wireless Controller"):
                if (event.code >= 0 and event.code <= 5):
                    if (abs(127.5 - event.value) > 8):
                        validInput(event)
                else:
                    validInput(event)

while  True:
    endTime = last_valid_input + datetime.timedelta(minutes=1)
    # print(f"Time Now {datetime.datetime.now()} Time to shutoff {endTime}")
    if (datetime.datetime.now() >= endTime):
        break
    r, w, x = select(devices, [], [], 1)
    for fd in r:
        for event in devices[fd].read():
            process_event(event, devices[fd])

# print(f"{datetime.datetime.now()} Idle time exceeded quiting")
print(subprocess.run(["bluetoothctl", "disconnect", "58:10:31:E0:9B:DD"]))
#pprint(tolerences)

