Script for turning off ps5 controller when Idle

this ignores the gyro as I don't use it

acounts for stick drift by 8 in either direction of 127.5, highest I've seen on
my controller is 132


setup

"DualSense Wireles Controller" and "DualSense Wireless Controller Touchpad"
unused gyro is "DualSense Wireless Controller Motion Sensors"

"Wireless Controller" and "Wireless Controller Touchpad"
unused gyro is "Wireless Controller Motion Sensors"
for ps4 DualShock

```
chmod +x controllerIdle.py
```

add the udev rule replaceing <location> with this projects location e.g. /etc/udev/rules.d/90-myrules.d
```
# ps5 DualSense
ACTION=="add", SUBSYSTEMS=="input", ATTRS{name}=="DualSense Wireless Controller", RUN+="<location>/idle_controller/controllerIdle.py"
# ps4 DualShock
ACTION=="add", SUBSYSTEMS=="input", ATTRS{name}=="Wireless Controller", RUN+="<location>/idle_controller/controllerIdle.py"
```

reload udev rules
```
sudo udevadm control --reload-rules && sudo udevadm trigger
```
