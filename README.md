Script for turning off ps5 controller when Idle

this ignores the gyro as I don't use it

acounts for stick drift by 4 in either direction of 127.5


setup

/dev/inputs are manually specified to check yours
```
udevadm info -a -n /dev/input/eventXX
```
replace event22 and event23 with your event Id's for 
"DualSense Wireles Controller" and "DualSense Wireless Controller Motion Sensors"

update mac address of controller in controllerIdle.py
if its already paired
```
bluetoothctl devices
```
to find mac address

```
chmod +x controllerIdle.py
```

add the udev rule replaceing <location> with this projects location e.g. /etc/udev/rules.d/90-myrules.d
```
ACTION=="add", SUBSYSTEMS=="input", ATTRS{name}=="DualSense Wireless Controller Motion Sensors", RUN+="<location>/idle_controller/controllerIdle.py"
```

reload udev rules
```
sudo udevadm control --reload-rules && sudo udevadm trigger
```
