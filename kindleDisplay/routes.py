from flask import request, send_file
from kindleDisplay import app, ha_info
from kindleDisplay.includes.classes import kindleDisplay
from io import BytesIO
from kindleDisplay.includes.solar import display_solar
from kindleDisplay.includes.kindle_battery import display_kindle_battery
from kindleDisplay.includes.presence import display_presence
from kindleDisplay.includes.weather import display_weather
from kindleDisplay.includes.tasks import display_tasks
from kindleDisplay.includes.calendar import display_calendar
from kindleDisplay.includes.threedprinter import display_printer
from kindleDisplay.includes.charge import display_charge
from kindleDisplay.includes.washing_machine import display_washing_machine
import requests
import logging

log = logging.getLogger(__name__)

display = kindleDisplay(ha_info)


def render_picture(ha_data, kindle_battery, display):
    display.clear_image()
    display_solar(ha_data, display)
    display.draw.line((40, 380, 840, 380), fill=64, width=1)
    display_weather(ha_data, display)
    display.draw.line((40, 500, 840, 500), fill=64, width=1)
    display_printer(ha_data, display)
    display_tasks(display)
    display_calendar(display)
    display_presence(ha_data, display)
    display_kindle_battery(kindle_battery, display)
    display_charge(ha_data, display)
    display_washing_machine(ha_data, display)

    out = display.image.rotate(90, expand=True)  # degrees counter-clockwise
    return out


@app.route("/kindle-data.png", methods=["GET"])
def get_data():
    global display
    # Get the battery level from the request
    kindle_battery = request.args.get("battery")
    # Get the data from Home Assistant
    log.debug(f'URL: {ha_info["url"]}')
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
