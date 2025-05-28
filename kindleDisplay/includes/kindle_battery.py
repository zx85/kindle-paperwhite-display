import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the default logging level to DEBUG


def display_kindle_battery(kindle_battery, display):  # Kindle battery
    log.debug(f"Kindle battery: {kindle_battery}")
    if kindle_battery:
        display.draw.text(
            (960, 715),
            f"{kindle_battery}%",
            font=display.suffix_font,
            fill=(0),
        )
