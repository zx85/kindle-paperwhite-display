from flask import request, send_file
from kindleDisplay import app, ha_info
from kindleDisplay.includes.classes import kindleDisplay
from io import BytesIO
from kindleDisplay.includes.solar import display_solar
from kindleDisplay.includes.kindle_battery import display_kindle_battery
from kindleDisplay.includes.presence import display_presence

import json
import requests
import datetime
import sys

display = kindleDisplay()


def render_picture(ha_data, kindle_battery, display):
    display.clear_image()
    display_solar(ha_data, display)
    display_kindle_battery(kindle_battery, display)
    display_presence(ha_data, display)

    out = display.image.rotate(270, expand=True)  # degrees counter-clockwise
    return out


@app.route("/kindle-data.png", methods=["GET"])
def get_data():
    global display
    # Get the battery level from the request
    kindle_battery = request.args.get("battery")
    # Get the data from Home Assistant
    ha_data = requests.get(
        "https://ha.mus-ic.co.uk/api/states",
        headers={"Authorization": f"Bearer {ha_info['key']}"},
    ).json()
    # time to create a picture
    pic = render_picture(ha_data, kindle_battery, display)

    # Save the image to a BytesIO object
    img_io = BytesIO()
    pic.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")
