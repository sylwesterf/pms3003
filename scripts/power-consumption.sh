# Disable the HDMI port
sudo nano /etc/rc.local
#add /usr/bin/tvservice -o

# Disable the LED
sudo nano /boot/config.txt
#add dtparam=act_led_trigger=none dtparam=act_led_activelow=on

# Disable Bluetooth
sudo nano /boot/config.txt
#add dtoverlay=pi3-disable-bt
sudo systemctl disable hciuart


# Sources:
# https://raspberry-projects.com/pi/pi-hardware/raspberry-pi-zero/minimising-power-consumption
# https://blog.sleeplessbeastie.eu/2018/12/31/how-to-disable-onboard-wifi-and-bluetooth-on-raspberry-pi-3/
