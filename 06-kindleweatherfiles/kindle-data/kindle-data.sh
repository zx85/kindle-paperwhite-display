#!/bin/sh
# Endpoint hosting the picture
url="http://192.168.75.4:5050"

cd "$(dirname "$0")"
rm kindle-data.png

stop framework

lipc-set-prop -i com.lab126.powerd preventScreenSaver 1
lipc-set-prop com.lab126.pillow disableEnablePillow disable

battery_level=$(lipc-get-prop -i com.lab126.powerd battLevel)

if wget -O kindle-data.png "${url}/kindle-data.png?battery=${battery_level}"; then
        eips -f -g kindle-data.png
else
        sleep 10
        if wget -O kindle-data.png "${url}/kindle-data.png?battery=${battery_level}"; then
        eips -f -g kindle-data.png
        fi

fi
