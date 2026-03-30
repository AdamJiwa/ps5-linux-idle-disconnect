#!/usr/bin/env python
import evdev
import time
import datetime
import subprocess
from select import select

# TODO handle multiple controllers
# TODO update udev rules to use vendor and product codes
# TODO reduce cpu usage

valid_controllers = ["Wireless Controller", "Wireless Controller Touchpad", "DualSense Wireless Controller", "DualSense Wireless Controller Touchpad"] # "DualSense Wirless Controller Motion Sensors"
vendor = 0x54c
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
controllers = {}

for device in devices:
    if (device.name in valid_controllers and device.info.vendor == vendor):
        # print("Found valid device ", device.path, device.name, device.phys)
        controllers[device.fd] = device

last_valid_input = datetime.datetime.now()

def validInput(event):
    global last_valid_input
    last_valid_input = datetime.datetime.now()
    # print(f"{last_valid_input} Detected valid input {event}")

def process_event(event, device):
    match event.type:
        case 1:
            validInput(event)
        case 3:
            if (device.name == "DualSense Wireless Controller" or device.name == "Wirless Controller"):
                if (event.code >= 0 and event.code <= 5):
                    if (abs(127.5 - event.value) > 8):
                        validInput(event)
                else:
                    validInput(event)

while  True:
    endTime = last_valid_input + datetime.timedelta(minutes=3)
    # print(f"Time Now {datetime.datetime.now()} Time to shutoff {endTime}")
    if (datetime.datetime.now() >= endTime):
        break
    r, w, x = select(controllers, [], [], 1)
    for fd in r:
        for event in controllers[fd].read():
            process_event(event, controllers[fd])

# print(f"{datetime.datetime.now()} Idle time exceeded quiting")
for controller in controllers:
    print(subprocess.run(["bluetoothctl", "disconnect", controllers[controller].uniq]))
