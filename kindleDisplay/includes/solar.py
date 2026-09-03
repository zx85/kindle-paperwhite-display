from kindleDisplay.includes.utils import entity_data, entity_display, utc_to_local
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the default logging level to DEBUG


# Solar display
def solar_text(x, y, ha_data, entities, suffix, display):
    cur_y = y
    if len(entities) == 2:
        for each_entity in entities:
            display.draw.text(
                (x, cur_y),
                entity_display(ha_data, each_entity),
                font=display.value_font,
                fill=(0),
            )
            cur_y += 55
    else:
        display.draw.text(
            (x, cur_y),
            entity_display(ha_data, entities),
            font=display.value_font,
            fill=(0),
        )
        cur_y += 55
    display.draw.text(
        (x, cur_y - 10),
        suffix,
        font=display.suffix_font,
        fill=(0),
    )


def display_solar(ha_data, display):

    """
    This function displays solar-related information on the display.
    """

    # elements are
    solar_mapping={
    "solar_in":"sensor.hall_solis_inverter_inverter_ac_power",             # current solar power
    "solar_today":"sensor.hall_solis_inverter_inverter_generation_today",  # solar today
    "power_used": "sensor.hall_solis_inverter_home_load_power",            # current consumption
    "power_used_today": "sensor.hall_solis_inverter_home_load_today",      # consumed today
    "grid_in": "sensor.hall_solis_inverter_grid_active_power",             # current grid power
    "export_today":"sensor.hall_solis_inverter_grid_export_today",         # exported today
    "grid_in_today":"sensor.hall_solis_inverter_grid_import_today",        # grid today
    "battery_per": "sensor.hall_solis_inverter_battery_soc",               # % battery remaining
    "runtime_today":"sensor.hall_solis_inverter_inverter_runtime_today",
    "timestamp": "sensor.date_time_iso"
    }

    runtime_today=entity_display(ha_data, solar_mapping['runtime_today'])
    timestamp_full=entity_display(ha_data, solar_mapping['timestamp']).split('T')[1]
    timestamp=':'.join(timestamp_full.split(':')[:2])

    # Positions of things
    solar_left = 30
    powerused_left = 250
    gridpower_left = 470
    battery_left = 710
    # Solar power
    #######################################

    # Solar icon
    solar_value = float(entity_data(ha_data, solar_mapping['solar_in'])[0])
    if solar_value < 40:
        display.image.paste(display.weather_icons[4], (solar_left, 10))
    elif solar_value < 500:
        display.image.paste(display.weather_icons[3], (solar_left, 10))
    elif solar_value < 1000:
        display.image.paste(display.weather_icons[2], (solar_left, 10))
    elif solar_value < 1800:
        display.image.paste(display.weather_icons[1], (solar_left, 10))
    else:
        display.image.paste(display.weather_icons[0], (solar_left, 10))

    # Solar now
    solar_text(
        solar_left + 10,
        130,
        ha_data,
        solar_mapping['solar_in'],
        "now",
        display,
    )
    # Solar today
    solar_text(
        solar_left + 10, 220, ha_data, solar_mapping['solar_today'], "today", display
    )

    # Consumed power
    ########################################

    # Power used
    display.image.paste(display.mainsplug_icon, (powerused_left, 10))

    solar_text(
        powerused_left - 5,
        130,
        ha_data,
        solar_mapping['power_used'],
        "now",
        display,
    )
    solar_text(
        powerused_left - 5,
        220,
        ha_data,
        solar_mapping['power_used_today'],
        "today",
        display,
    )

    # Grid power
    ########################################
    display.image.paste(display.pylon_icon, (gridpower_left, 10))

    cur_power = float(entity_data(ha_data, solar_mapping['grid_in'])[0])
    if cur_power > 0:
        display.image.paste(display.uparrow_icon, (gridpower_left + 3, 150))
    elif cur_power < 0:
        display.image.paste(display.downarrow_icon, (gridpower_left + 3, 150))

    solar_text(
        gridpower_left + 25,
        130,
        ha_data,
        solar_mapping['grid_in'],
        "now",
        display,
    )

    # Arrows
    display.image.paste(display.uparrow_icon, (gridpower_left + 3, 240))
    display.image.paste(display.downarrow_icon, (gridpower_left + 3, 295))

    solar_text(
        gridpower_left + 25,
        220,
        ha_data,
        (
            solar_mapping['export_today'],
            solar_mapping['grid_in_today'],
        ),
        "today",
        display,
    )

    # Battery
    battery_value = float(
        entity_data(ha_data, solar_mapping['battery_per'])[0]
    )
    batt_icon_x = battery_left + 25
    display.draw.rectangle(
        [batt_icon_x + 20, 10, batt_icon_x + 40, 122], fill=64
    )  # top
    display.draw.rectangle(
        [batt_icon_x, 22, batt_icon_x + 60, 138], fill=64
    )  # background
    display.draw.rectangle(
        [batt_icon_x + 10, 30, batt_icon_x + 50, int(130 - battery_value)], fill=240
    )

    battery_direction_icon = display.noarrow_icon
    if display.previous_runtime_today != runtime_today:
        # Arrows if the time has changed
        if battery_value > display.previous_battery:
            battery_direction_icon = display.uparrow_icon
        elif battery_value < display.previous_battery:
            battery_direction_icon = display.downarrow_icon

        display.previous_battery = battery_value

    display.image.paste(battery_direction_icon, (battery_left - 10, 70))

    # Battery timestamp.split(':')[:2]

    solar_text(
        battery_left,
        150,
        ha_data,
        solar_mapping['battery_per'],
        timestamp,
        display,
    )
    # Update the previous timestamps and values
    display.previous_runtime_today = runtime_today
