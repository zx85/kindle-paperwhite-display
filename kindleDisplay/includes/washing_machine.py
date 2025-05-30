from kindleDisplay.includes.utils import entity_data, entity_display


def display_washing_machine(ha_data, display):
    washing_left = 810
    washing_top = 630
    status = entity_data(ha_data, "binary_sensor.washing_machine_status")[0]
    time_remaining = entity_data(ha_data, "sensor.washing_machine_remaining_time")[0]
    if status == "off":
        display.image.paste(display.washing_machine_off, (washing_left, washing_top))
    else:
        display.image.paste(display.washing_machine_on, (washing_left, washing_top))
        display.draw.text(
            (
                washing_left + 5 - (int(int(time_remaining) / 100) * 8),
                washing_top + 72,
            ),
            f"{time_remaining}",
            font=display.value_font,
            fill=(64),
        )
