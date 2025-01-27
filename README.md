# kindle-paperwhite-display
First draft of kindle paperwhite display thing

Based on this YouTube video: https://youtu.be/Oel08SDFyIY?si=Cbr3DdWQAcKJvmhC


## 01 - Jailbreak kindle

Based on this thread https://www.mobileread.com/forums/showthread.php?t=346037

Files are in `01-watchthis-jailbreak`

Quite a few steps:

- Factory reset the device. Make sure to use the "en_GB" or "English (United Kingdom)" locale when setting the language.
- Type ;enter_demo in the Kindle search bar after performing a factory reset
- Reboot the device
- Once in demo mode, skip setting up wifi and enter dummy values for store registration when prompted.
- Skip searching for a demo payload
- Select the "standard" demo type
- Press "Done" at the prompt to sideload content. Do not sideload the jailbreak at this stage.
- Once the demo is setup, skip the misconfiguration lockout using the "secret gesture" (double finger tap on bottom right of screen then swipe left)
- Enter the demo configuration menu by typing ;demo into the search bar
- Select the "Sideload Content" option

after a few more reboots it should be done(?)

## 01.5 - get wifi working on the Kindle

## 02 - install KUAL

Based on this thread: https://www.mobileread.com/forums/showthread.php?t=203326

Essentially: 

- Put KUAL-KDK-2.0.azw2 in documents folder.
- Run it by clicking icon.

## 03 - install MR

Based on this thread: https://www.mobileread.com/forums/showthread.php?t=251143

- Copy extensions and mrpackages folder to root of Kindle
- Run KUAL to install the mrpackage extension

## 04 - install usbnet

https://wiki.mobileread.com/wiki/USBNetwork

- copy the Update_usbnet_0.22.N_install_pw2_and_up to the mrpackages folder and run mrpackages

## 05 (for Windows) install rndis driver

- get the Kindle into USB network mode and run ;un

Re-install the driver for rndis driver when the COM port turns up

For USB connection the device will default to 192.168.15.244 
(Set the local IP address 192.168.15.201)

## 06 - install the weather app bits

ssh as root to the kindle once the network connection has been configured (no password)

`mntroot rw` to mount the root volume RW
edit the crontab for root (not sure if crontab -e works?)

`vi /etc/crontab/root`

add the link to the script (that will need to be copied to the root of the kindle)

```
*/5 * * * * /mnt/us/weather/display-weather.sh
```

## Format of the PNG

The PNG needs to be 760 x 1026 8 bit colour (greyscale) depth

### Tools to create the image

It looks like the excellent [Pillow](https://pillow.readthedocs.io/en/stable/) library does everything I need it to do.

I've created a Flask app that does all the things

It can be started up with Docker

```
cd kindleDisplay
docker compose build
docker compose up -d
```

#### Required environment variables

- URL (URL for the home assistant API)
- KEY (Long-term token for access to the API)