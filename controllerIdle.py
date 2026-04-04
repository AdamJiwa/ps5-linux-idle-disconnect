#!/usr/bin/env python
import evdev
import time
import datetime
import subprocess
from select import select
import logging


logging.basicConfig(
    filename = '/tmp/controllerIdle.log',
    filemode = 'a',
    format = '%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

# TODO handle multiple controllers
# TODO update udev rules to use vendor and product codes
# TODO reduce cpu usage

valid_controllers = ["Wireless Controller", "Wireless Controller Touchpad", "DualSense Wireless Controller", "DualSense Wireless Controller Touchpad"] # "DualSense Wirless Controller Motion Sensors"
vendor = 0x54c
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
controllers = {}

for device in devices:
    if (device.name in valid_controllers and device.info.vendor == vendor):
        logging.info(f"Found valid device {device.name}")
        controllers[device.fd] = device

if (len(controllers) < 1):
    logging.error("Failed to find controller")
    exit()

last_valid_input = datetime.datetime.now()

def validInput(event):
    global last_valid_input
    last_valid_input = datetime.datetime.now()
    # logging.info(f"{last_valid_input} Detected valid input {event}")

def process_event(event, device):
    match event.type:
        case 1:
            validInput(event)
        case 3:
            if (device.name == "DualSense Wireless Controller" or device.name == "Wirless Controller"):
                if (event.code >= 0 and event.code <= 5):
                    if (abs(127.5 - event.value) > 16):
                        validInput(event)
                else:
                    validInput(event)

while  True:
    endTime = last_valid_input + datetime.timedelta(minutes=3)
    # logging.info(f"Time Now {datetime.datetime.now()} Time to shutoff {endTime}")
    if (datetime.datetime.now() >= endTime):
        logging.info("idle time exceeded")
        break
    r, w, x = select(controllers, [], [], 1)
    for fd in r:
        for event in controllers[fd].read():
            process_event(event, controllers[fd])

for controller in controllers:
    logging.info(subprocess.run(["bluetoothctl", "disconnect", controllers[controller].uniq]))
