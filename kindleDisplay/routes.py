from flask import request, send_file
from kindleDisplay import app, ha_info
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import json
import requests
import datetime
import sys

# use a truetype font
heading_font = ImageFont.truetype(
    "kindleDisplay/fonts/encode-sans/EncodeSansCompressed-700-Bold.ttf", 64
)
value_font = ImageFont.truetype(
    "kindleDisplay/fonts/encode-sans/EncodeSansCompressed-500-Medium.ttf", 48
)
suffix_font = ImageFont.truetype(
    "kindleDisplay/fonts/encode-sans/EncodeSansCondensed-300-Light.ttf", 48
)

weather_icons = [
    Image.open("kindleDisplay/images/weather-sunshine.png"),
    Image.open("kindleDisplay/images/weather-suncloud.png"),
    Image.open("kindleDisplay/images/weather-cloudsun.png"),
    Image.open("kindleDisplay/images/weather-cloud.png"),
    Image.open("kindleDisplay/images/weather-night.png"),
]


@app.route("/data", methods=["GET"])
def get_data():
    #
    ha_data = requests.get(
        ha_info["url"], headers={"Authorization": f"Bearer {ha_info['key']}"}
    ).json()
    # time to create a picture
    pic = render_picture(ha_data)

    # Save the image to a BytesIO object
    img_io = BytesIO()
    pic.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


# Function to find the dictionary with the specified entity_id
def entity_data(data, entity_id):
    entity = next((item for item in data if item["entity_id"] == entity_id), None)
    return f'{entity["state"]}{entity["attributes"]["unit_of_measurement"]}'


def render_picture(ha_data):

    # pip install Pillow -  https://pillow.readthedocs.io/en/stable/
    image = Image.new("L", (1026, 760), (255))
    draw = ImageDraw.Draw(image)

    # elements are
    # {"solar_in":"sensor.solis_ac_output_total_power",     # current solar power
    # "power_used": "sensor.solis_total_consumption_power", # current consumption
    # "grid_in": "sensor.solis_power_grid_total_power",  # current grid power
    # "battery_per": "sensor.solis_remaining_battery_capacity",  # % battery remaining
    # "export_today":"sensor.solis_daily_on_grid_energy",          # exported today
    # "solar_today":"sensor.solis_energy_today",                   # solar today
    # "grid_in_today":"sensor.solis_daily_grid_energy_purchased"}

    # Heading
    draw.text(
        (80, 10),
        "Solar data",
        font=heading_font,
        fill=(0),
    )

    # Solar icon
    image.paste(weather_icons[4], (5, 100))

    # Solar now
    draw.text(
        (215, 100),
        entity_data(ha_data, "sensor.solis_ac_output_total_power"),
        font=value_font,
        fill=(0),
    )

    # Solar today
    draw.text(
        (215, 180),
        entity_data(ha_data, "sensor.solis_energy_today"),
        font=value_font,
        fill=(0),
    )

    draw.line((9, 25, 9, 100), fill=128)

    out = image.rotate(270, expand=True)  # degrees counter-clockwise
    return out
