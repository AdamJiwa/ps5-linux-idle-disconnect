Script for turning off ps5 controller when Idle

this ignores the gyro as I don't use it

acounts for stick drift by 16 in either direction of 127.5, highest I've seen is
on my old DS4 controller with 143 

setup

"DualSense Wireles Controller" and "DualSense Wireless Controller Touchpad"
unused gyro is "DualSense Wireless Controller Motion Sensors"

"Wireless Controller" and "Wireless Controller Touchpad"
unused gyro is "Wireless Controller Motion Sensors"
for ps4 DualShock

```
chmod +x controllerIdle.py
```

create a systemd task e.g. /etc/systemd/system/controller-idle.service
```
[Unit]
Description=Idle shut off for play station controllers

[Service]
Type=oneshot
RemainAfterExt=true
ExecStart=controllerIdle.py
User=
Group=
```

fill out the path to controllerIdle.py and add the user/group you want to run it as


add the udev rule replaceing <location> with this projects location e.g. /etc/udev/rules.d/90-myrules.d
```
# ps5 DualSense
ACTION=="add", SUBSYSTEMS=="input", ATTRS{name}=="DualSense Wireless Controller", TAG+="systemd", ENV{SYSTEMD_WANTS}="controller-idle.service" 
# ps4 DualShock
ACTION=="add", SUBSYSTEMS=="input", ATTRS{name}=="Wireless Controller", TAG+="systemd", ENV{SYSTEMD_WANTS}="controller-idle.service"
```

reload udev rules
```
sudo udevadm control --reload-rules && sudo udevadm trigger
```
