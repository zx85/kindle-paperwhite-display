#!/bin/sh

cd "$(dirname "$0")"

stop framework

lipc-set-prop -i com.lab126.powerd preventScreenSaver 1
lipc-set-prop com.lab126.pillow disableEnablePillow disable

eips -f -g sleeping-670-1026.png
