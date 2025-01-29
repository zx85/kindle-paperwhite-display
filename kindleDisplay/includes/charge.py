from kindleDisplay.includes.utils import entity_data, entity_display


def display_charge(ha_data, display):
    zappi_charge_mode = entity_data(ha_data, "select.myenergi_zappi_2_charge_mode")[0].lower()
    solis_battery_charging = entity_data(
        ha_data, "input_boolean.solar_battery_charging"
    )[0]

    if zappi_charge_mode == "fast":
        display.image.paste(display.car_charging_icon, (906, 630))
    else:
        display.image.paste(display.car_not_charging_icon, (906, 630))

    if solis_battery_charging == "on":
        display.image.paste(display.zap_icon, (800, 30))
