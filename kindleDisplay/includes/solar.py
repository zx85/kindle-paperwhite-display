from kindleDisplay.includes.utils import entity_data, entity_display


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
    current_timestamp = entity_data(ha_data, "sensor.solis_total_consumption_power")[2]

    """
    This function displays solar-related information on the display.
    """

    # elements are
    # {"solar_in":"sensor.solis_ac_output_total_power",     # current solar power
    # "solar_today":"sensor.solis_energy_today",                   # solar today
    # "power_used": "sensor.solis_total_consumption_power", # current consumption
    # "power_used_today": "sensor.solis_daily_grid_energy_used",  # power used today
    # "grid_in": "sensor.solis_power_grid_total_power",  # current grid power
    # "export_today":"sensor.solis_daily_on_grid_energy",          # exported today
    # "grid_in_today":"sensor.solis_daily_grid_energy_purchased"}
    # "battery_per": "sensor.solis_remaining_battery_capacity",  # % battery remaining

    # Positions of things
    solar_left = 30
    powerused_left = 250
    gridpower_left = 470
    battery_left = 710
    # Solar power
    #######################################

    # Solar icon
    solar_value = float(entity_data(ha_data, "sensor.solis_ac_output_total_power")[0])
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
        "sensor.solis_ac_output_total_power",
        "now",
        display,
    )
    # Solar today
    solar_text(
        solar_left + 10, 220, ha_data, "sensor.solis_energy_today", "today", display
    )

    # Consumed power
    ########################################

    # Power used
    display.image.paste(display.mainsplug_icon, (powerused_left, 10))

    solar_text(
        powerused_left - 5,
        130,
        ha_data,
        "sensor.solis_total_consumption_power",
        "now",
        display,
    )
    solar_text(
        powerused_left - 5,
        220,
        ha_data,
        "sensor.solis_daily_grid_energy_used",
        "today",
        display,
    )

    # Grid power
    ########################################
    display.image.paste(display.pylon_icon, (gridpower_left, 10))

    cur_power = float(entity_data(ha_data, "sensor.solis_power_grid_total_power")[0])
    if cur_power > 0:
        display.image.paste(display.uparrow_icon, (gridpower_left + 3, 150))
    elif cur_power < 0:
        display.image.paste(display.downarrow_icon, (gridpower_left + 3, 150))

    solar_text(
        gridpower_left + 25,
        130,
        ha_data,
        "sensor.solis_power_grid_total_power",
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
            "sensor.solis_daily_on_grid_energy",
            "sensor.solis_daily_grid_energy_purchased",
        ),
        "today",
        display,
    )

    # Battery
    battery_value = float(
        entity_data(ha_data, "sensor.solis_remaining_battery_capacity")[0]
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
    if display.previous_timestamp != current_timestamp:
        # Arrows if the time has changed
        if battery_value > display.previous_battery:
            battery_direction_icon = display.uparrow_icon
        elif battery_value < display.previous_battery:
            battery_direction_icon = display.downarrow_icon

        display.previous_battery = battery_value

    display.image.paste(battery_direction_icon, (battery_left - 10, 70))

    # Battery
    solar_text(
        battery_left,
        150,
        ha_data,
        "sensor.solis_remaining_battery_capacity",
        f"@{entity_data(ha_data, 'sensor.solis_total_consumption_power')[2][11:16]}",
        display,
    )
    # Update the previous timestamps and values
    display.previous_timestamp = current_timestamp
