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
    "fonts/encode-sans/EncodeSansCompressed-700-Bold.ttf", 64
)
value_font = ImageFont.truetype(
    "fonts/encode-sans/EncodeSansCompressed-500-Medium.ttf", 48
)
suffix_font = ImageFont.truetype(
    "fonts/encode-sans/EncodeSansCondensed-300-Light.ttf", 32
)

weather_icons = [
    Image.open("images/weather-sunshine.png"),
    Image.open("images/weather-suncloud.png"),
    Image.open("images/weather-cloudsun.png"),
    Image.open("images/weather-cloud.png"),
    Image.open("images/weather-night.png"),
]
mainsplug_icon = Image.open("images/mains-plug.png")
pylon_icon = Image.open("images/pylon.png")
uparrow_icon = Image.open("images/up-arrow.png")
downarrow_icon = Image.open("images/down-arrow.png")
noarrow_icon = Image.open("images/no-arrow.png")
previous_timestamp = ""
previous_battery = 50.0
battery_direction_icon = noarrow_icon


@app.route("/kindle-data.png", methods=["GET"])
def get_data():

    # Get the battery level from the request
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
    value=entity['state'].replace('-','')
    uom=entity['attributes']['unit_of_measurement']
    if uom == 'W' or uom == '%':
        display_value=f"{int(float(value))}"
    elif uom == 'kW' or uom == 'kWh':
        display_value=f"{float(value):.1f}"
    else:
        display_value=value
    return f"{display_value}{uom}"


def solar_text(x, y, ha_data, entities, suffix, draw):
    cur_y = y
    if len(entities) == 2:
        for each_entity in entities:
            draw.text(
                (x, cur_y),
                entity_display(ha_data, each_entity),
                font=value_font,
                fill=(0),
            )
            cur_y += 55
    else:
        draw.text(
            (x, cur_y),
            entity_display(ha_data, entities),
            font=value_font,
            fill=(0),
        )
        cur_y += 55
    draw.text(
        (x, cur_y-10),
        suffix,
        font=suffix_font,
        fill=(0),
    )


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

    # Solar power
    #######################################

    # Solar icon
    solar_value = float(entity_data(ha_data, "sensor.solis_ac_output_total_power")[0])
    if solar_value < 100:
        image.paste(weather_icons[4], (5, 10))
    elif solar_value < 500:
        image.paste(weather_icons[3], (5, 10))
    elif solar_value < 1000:
        image.paste(weather_icons[2], (5, 10))
    elif solar_value < 1800:
        image.paste(weather_icons[1], (5, 10))
    else:
        image.paste(weather_icons[0], (5, 10))

    # Solar now
    solar_text(15, 130, ha_data, "sensor.solis_ac_output_total_power", "now", draw)

    # Solar today
    solar_text(15, 220, ha_data, "sensor.solis_energy_today", "today", draw)

    # Consumed power
    ########################################

    # Power used
    image.paste(mainsplug_icon, (205, 10))

    solar_text(200, 130, ha_data, "sensor.solis_total_consumption_power", "now", draw)
    solar_text(200, 220, ha_data, "sensor.solis_daily_grid_energy_used", "today", draw)

    # Grid power
    ########################################
    image.paste(pylon_icon, (405, 10))

    cur_power = float(entity_data(ha_data, "sensor.solis_power_grid_total_power")[0])
    if cur_power > 0:
        image.paste(uparrow_icon, (408, 150))
    elif cur_power < 0:
        image.paste(downarrow_icon, (408, 150))

    solar_text(430, 130, ha_data, "sensor.solis_power_grid_total_power", "now", draw)

    # Arrows
    image.paste(uparrow_icon, (408, 240))
    image.paste(downarrow_icon, (408, 295))

    solar_text(
        430,
        220,
        ha_data,
        (
            "sensor.solis_daily_on_grid_energy",
            "sensor.solis_daily_grid_energy_purchased",
        ),
        "today",
        draw,
    )

    # Battery
    battery_value = float(
        entity_data(ha_data, "sensor.solis_remaining_battery_capacity")[0]
    )

    draw.rectangle([675, 10, 695, 122], fill=64)  # top
    draw.rectangle([655, 22, 715, 138], fill=64)  # background
    draw.rectangle([665, 30, 705, int(130  - battery_value)], fill=240)

    if previous_timestamp != current_timestamp:
        previous_battery = battery_value

        # Arrows if the time has changed
        if battery_value > previous_battery:
            battery_direction_icon = uparrow_icon
        elif battery_value < previous_battery:
            battery_direction_icon = downarrow_icon
        else:
            battery_direction_icon = noarrow_icon

    image.paste(battery_direction_icon, (620, 70))

    # Battery
    solar_text(630, 150, ha_data, "sensor.solis_remaining_battery_capacity", f"@{entity_data(ha_data, 'sensor.solis_total_consumption_power')[2][11:16]}", draw)

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
