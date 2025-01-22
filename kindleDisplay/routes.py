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
    "kindleDisplay/fonts/encode-sans/EncodeSansCondensed-300-Light.ttf", 32
)

weather_icons = [
    Image.open("kindleDisplay/images/weather-sunshine.png"),
    Image.open("kindleDisplay/images/weather-suncloud.png"),
    Image.open("kindleDisplay/images/weather-cloudsun.png"),
    Image.open("kindleDisplay/images/weather-cloud.png"),
    Image.open("kindleDisplay/images/weather-night.png"),
]
mainsplug_icon = Image.open("kindleDisplay/images/mains-plug.png")
pylon_icon = Image.open("kindleDisplay/images/pylon.png")
uparrow_icon = Image.open("kindleDisplay/images/up-arrow.png")
downarrow_icon = Image.open("kindleDisplay/images/down-arrow.png")
noarrow_icon = Image.open("kindleDisplay/images/no-arrow.png")


@app.route("/data", methods=["GET"])
def get_data():
    #
    ha_data = requests.get(
        "https://ha.mus-ic.co.uk/api/states",
        headers={"Authorization": f"Bearer {ha_info['key']}"},
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
    return (entity["state"], entity["attributes"]["unit_of_measurement"])


# Function to find the dictionary with the specified entity_id
def entity_display(data, entity_id):
    entity = next((item for item in data if item["entity_id"] == entity_id), None)
    return f"{entity['state']}{entity['attributes']['unit_of_measurement']}"


def render_picture(ha_data):

    # pip install Pillow -  https://pillow.readthedocs.io/en/stable/
    image = Image.new("L", (1026, 760), (255))
    draw = ImageDraw.Draw(image)

    # elements are
    # {"solar_in":"sensor.solis_ac_output_total_power",     # current solar power
    # "solar_today":"sensor.solis_energy_today",                   # solar today
    # "power_used": "sensor.solis_total_consumption_power", # current consumption
    # "power_used_today": "sensor.solis_daily_grid_energy_used",  # power used today
    # "grid_in": "sensor.solis_power_grid_total_power",  # current grid power
    # "export_today":"sensor.solis_daily_on_grid_energy",          # exported today
    # "grid_in_today":"sensor.solis_daily_grid_energy_purchased"}
    # "battery_per": "sensor.solis_remaining_battery_capacity",  # % battery remaining

    # Heading
    draw.text(
        (80, 10),
        "Solar data",
        font=heading_font,
        fill=(0),
    )
    draw.line((80, 90, 360, 90), fill=128)

    # Solar icon
    solar_value = float(entity_data(ha_data, "sensor.solis_ac_output_total_power")[0])
    if solar_value < 100:
        image.paste(weather_icons[4], (5, 110))
    elif solar_value < 500:
        image.paste(weather_icons[3], (5, 110))
    elif solar_value < 1000:
        image.paste(weather_icons[2], (5, 110))
    elif solar_value < 1800:
        image.paste(weather_icons[1], (5, 110))
    else:
        image.paste(weather_icons[0], (5, 110))

    # Solar now
    draw.text(
        (195, 100),
        entity_display(ha_data, "sensor.solis_ac_output_total_power"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (195, 145),
        "now",
        font=suffix_font,
        fill=(0),
    )

    # Solar today
    draw.text(
        (195, 180),
        entity_display(ha_data, "sensor.solis_energy_today"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (195, 225),
        "today",
        font=suffix_font,
        fill=(0),
    )

    # Power used
    image.paste(mainsplug_icon, (5, 290))

    draw.text(
        (195, 280),
        entity_display(ha_data, "sensor.solis_total_consumption_power"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (195, 325),
        "now",
        font=suffix_font,
        fill=(0),
    )

    draw.text(
        (195, 360),
        entity_display(ha_data, "sensor.solis_daily_grid_energy_used"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (195, 405),
        "today",
        font=suffix_font,
        fill=(0),
    )

    # Grid power
    image.paste(pylon_icon, (5, 510))

    cur_power = float(entity_data(ha_data, "sensor.solis_power_grid_total_power")[0])
    if cur_power > 0:
        image.paste(uparrow_icon, (170, 482))
    elif cur_power < 0:
        image.paste(downarrow_icon, (170, 482))
    else:
        image.paste(noarrow_icon, (170, 482))

    draw.text(
        (195, 460),
        entity_display(ha_data, "sensor.solis_power_grid_total_power"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (195, 505),
        "now",
        font=suffix_font,
        fill=(0),
    )

    # Exported today
    draw.text(
        (195, 540),
        entity_display(ha_data, "sensor.solis_daily_on_grid_energy"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (195, 585),
        "today",
        font=suffix_font,
        fill=(0),
    )

    # Import today

    draw.text(
        (195, 620),
        entity_display(ha_data, "sensor.solis_daily_grid_energy_purchased"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (195, 665),
        "today",
        font=suffix_font,
        fill=(0),
    )

    out = image.rotate(270, expand=True)  # degrees counter-clockwise
    return out
