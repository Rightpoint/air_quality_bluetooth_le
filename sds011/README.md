# Introduction

The SDS011 module's operational features, including its PM2.5/PM10 sensing features, **greatly surpass those of most other such modules available via the web**. In addition to a standard **duty cycle and firmware / sensor id readouts**, these features include a useful **sleep mode**. The Python3 code described below controls the sensor, developed by Nova Fitness Co., Ltd http://inovafitness.com/en/, for measurement of air particles <=10µm (PM10) and <=2.5µm (PM2.5).
# Goal
The code I found available on the web offers only very limited functionality. In most cases, it solely implements permanent measuring, using the sensor's "no dutycycle" mode (the factory default). But **the sensor offers much more than this one mode**. It actually features two working modes, along with a "going to sleep" mode, **dutycycles ranging from 1 to about 30 minutes** and several other capabilities.
So I decided to put together a python library that would make fuller use of the sensor's capabilities. In addition, my project would

1. enable me to measure air pollution with a Raspberry Pi
2. yield some useful code for other users
3. give me practice in coding python
4. teach me to use git

So yes, admittedly, this is indeed my first python project. But don't let that scare you away! The code has been tested and it works. On the other hand, feel free to suggest improvements!
# Get started..
Just plug your sensor into a USB port, open test.py in an editor of your choice, edit the constructor call to your needs (the device_path) and run **>python3 test.py** in your console. Now you can see just how clean or dirty the air you're breathing everyday is.

**You have to use python3 insead of python2. Depends on your system if python call is mapped to version 2 or version 3.**

**Advice:** If you do not code right, your sensor might get stuck in dutycycle mode when you plug it off an on again. Not so well coded other libraries or software sometimes is not able to handle this situation. Too fix this, just call sensor.reset() in your python3 code. 
# No warranty
SDS011 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
# Some advices
The sensor comes with Windows software, but it can also be coupled with a Raspberry Pi, on USB or GPIO, by using the serial input and output channels. Caution: I don't yet know if switching the sensor back to the measuring mode, directly from the sleep mode, will crash the Raspberry Pi (this is partly because I do not yet know the details of the sensor's power consumption). So you may have to use an external power power source (i.e. a powered USB hub) for your Raspberry Pi.

To use the sensor with Raspberry Pi on GPIO, you have to ensure that no other serial communication is taking place.

So in "/boot/cmdline" the line

dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait 
has to be changed to

dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles 

At the time I wrote these lines, many web threads were available on "edit the inittab". But now the firmware itself does not include any inittab. Details about this issue can be found here: 

https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=123081

So to disable getty, just type ">sudo systemctl stop serial-getty@ttyAMA0.service" in your terminal or disable it with ">sudo systemctl disable serial-getty@ttyAMA0.service"

Copyright 2016, Frank Heuer, Germany 

SDS011 is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
You should have received a copy of the GNU General Public License along with SDS011. If not, see http://www.gnu.org/licenses/.
Have fun, and keep your air (inside and outside of your home) free of pollutants!

# Thanks
Thanks to Eric for proofreading these lines. It is always good to have a friend.
