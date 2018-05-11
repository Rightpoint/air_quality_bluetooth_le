The Sensor comes with a Windows software but can be used with raspberry pi GPIO feature by using the serial in an d output channels.

In order to use it on raspberry pi one has to enshure that no other serial communication is happening.

So in /boot/cmdline the line
dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait

has to be changed to
dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles

At the time writing this lines you can find many threads in the weg pointing to "edit the inittab". But today working with actual firmware there is no inittab.
Details about that could be found here:

https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=123081

So to disable getty just type
">sudo systemctl stop serial-getty@ttyAMA0.service"
in your terminal or disable it
">sudo systemctl disable serial-getty@ttyAMA0.service"

