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
    "kindleDisplay/fonts/encode-sans/EncodeSansCompressed-500-Medium.ttf", 36
)
suffix_font = ImageFont.truetype(
    "kindleDisplay/fonts/encode-sans/EncodeSansCondensed-300-Light.ttf", 24
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
previous_timestamp = ""
previous_battery = 50.0
battery_direction_icon = noarrow_icon


@app.route("/kindle-data.png", methods=["GET"])
def get_data():

    kindle_battery = request.args.get("battery")
    # Get the data from Home Assistant
    ha_data = requests.get(
        "https://ha.mus-ic.co.uk/api/states",
        headers={"Authorization": f"Bearer {ha_info['key']}"},
    ).json()
    # time to create a picture
    pic = render_picture(ha_data, kindle_battery)

    # Save the image to a BytesIO object
    img_io = BytesIO()
    pic.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")
    return f"{ha_data}"


# Function to find the dictionary with the specified entity_id
def entity_data(data, entity_id):
    entity = next((item for item in data if item["entity_id"] == entity_id), None)
    return (
        entity["state"],
        entity["attributes"]["unit_of_measurement"],
        entity["last_updated"],
    )


# Function to find the dictionary with the specified entity_id
def entity_display(data, entity_id):
    entity = next((item for item in data if item["entity_id"] == entity_id), None)
    return f"{entity['state']}{entity['attributes']['unit_of_measurement']}"


def render_picture(ha_data, kindle_battery):
    # make the variables global so they update on every call
    global previous_timestamp
    global previous_battery
    global battery_direction_icon

    current_timestamp = entity_data(ha_data, "sensor.solis_total_consumption_power")[2]

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
    draw.line((0, 90, 380, 90), fill=128)

    # Time
    draw.text(
        (320, 92),
        f"@{entity_data(ha_data, 'sensor.solis_total_consumption_power')[2][11:16]}",
        font=suffix_font,
        fill=(0),
    )
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
        (165, 100),
        entity_display(ha_data, "sensor.solis_ac_output_total_power"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (165, 135),
        "now",
        font=suffix_font,
        fill=(0),
    )

    # Solar today
    draw.text(
        (165, 170),
        entity_display(ha_data, "sensor.solis_energy_today"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (165, 205),
        "today",
        font=suffix_font,
        fill=(0),
    )

    # Power used
    image.paste(mainsplug_icon, (5, 260))

    draw.text(
        (165, 260),
        entity_display(ha_data, "sensor.solis_total_consumption_power"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (165, 295),
        "now",
        font=suffix_font,
        fill=(0),
    )

    draw.text(
        (165, 330),
        entity_display(ha_data, "sensor.solis_daily_grid_energy_used"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (165, 365),
        "today",
        font=suffix_font,
        fill=(0),
    )

    # Grid power
    image.paste(pylon_icon, (5, 455))

    cur_power = float(entity_data(ha_data, "sensor.solis_power_grid_total_power")[0])
    if cur_power > 0:
        image.paste(uparrow_icon, (140, 440))
    elif cur_power < 0:
        image.paste(downarrow_icon, (140, 440))

    draw.text(
        (165, 430),
        entity_display(ha_data, "sensor.solis_power_grid_total_power"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (165, 465),
        "now",
        font=suffix_font,
        fill=(0),
    )

    # Exported today
    image.paste(uparrow_icon, (140, 510))
    draw.text(
        (165, 500),
        entity_display(ha_data, "sensor.solis_daily_on_grid_energy"),
        font=value_font,
        fill=(0),
    )

    # Import today
    image.paste(downarrow_icon, (140, 552))
    draw.text(
        (165, 540),
        entity_display(ha_data, "sensor.solis_daily_grid_energy_purchased"),
        font=value_font,
        fill=(0),
    )

    draw.text(
        (165, 575),
        "today",
        font=suffix_font,
        fill=(0),
    )

    # Battery
    battery_value = float(
        entity_data(ha_data, "sensor.solis_remaining_battery_capacity")[0]
    )

    draw.rectangle([60, 624, 70, 630], fill=64)  # top
    draw.rectangle([50, 630, 80, 700], fill=64)  # background
    draw.rectangle([55, 640, 75, int(640 + (100 - battery_value) / 2)], fill=240)

    if previous_timestamp != current_timestamp:
        previous_battery = battery_value

    # Arrows if the time has changed
    if battery_value > previous_battery:
        battery_direction_icon = uparrow_icon
    elif battery_value < previous_battery:
        battery_direction_icon = downarrow_icon
    else:
        battery_direction_icon = noarrow_icon

    image.paste(battery_direction_icon, (140, 652))

    draw.text(
        (165, 640),
        f"{entity_display(ha_data, 'sensor.solis_remaining_battery_capacity').split('.')[0]}%",
        font=value_font,
        fill=(0),
    )

    # Kindle battery
    draw.text(
        (960, 715),
        f"{kindle_battery}%",
        font=suffix_font,
        fill=(0),
    )
    # Update the previous timestamps and values

    previous_timestamp = current_timestamp
    out = image.rotate(270, expand=True)  # degrees counter-clockwise
    return out
