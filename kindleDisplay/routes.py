from flask import request, send_file
from kindleDisplay import app, ha_info
from kindleDisplay.includes.classes import kindleDisplay
from io import BytesIO
from kindleDisplay.includes.solar import display_solar
from kindleDisplay.includes.kindle_battery import display_kindle_battery
from kindleDisplay.includes.presence import display_presence
from kindleDisplay.includes.weather import display_weather
from kindleDisplay.includes.tasks import display_tasks
from kindleDisplay.includes.threedprinter import display_3d_printer

import json
import requests
import datetime
import sys

display = kindleDisplay(ha_info)


def render_picture(ha_data, kindle_battery, display):
    display.clear_image()
    display_solar(ha_data, display)
    display.draw.line((40, 380, 840, 380), fill=64, width=1)
    display_weather(ha_data, display)
    display.draw.line((40, 500, 840, 500), fill=64, width=1)
    display_tasks(display)
    display_presence(ha_data, display)
    display_3d_printer(ha_data, display)
    display_kindle_battery(kindle_battery, display)

    out = display.image.rotate(270, expand=True)  # degrees counter-clockwise
    return out


@app.route("/kindle-data.png", methods=["GET"])
def get_data():
    global display
    # Get the battery level from the request
    kindle_battery = request.args.get("battery")
    # Get the data from Home Assistant
    ha_data = requests.get(
        f"{ha_info['url']}/states",
        headers={"Authorization": f"Bearer {ha_info['key']}"},
    ).json()
    # time to create a picture
    pic = render_picture(ha_data, kindle_battery, display)

    # Save the image to a BytesIO object
    img_io = BytesIO()
    pic.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")
