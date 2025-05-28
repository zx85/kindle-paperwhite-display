import logging
from kindleDisplay.includes.utils import entity_data, entity_display

# Create a logger instance
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the default logging level to DEBUG

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Define the log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the handler to the logger
log.addHandler(console_handler)


def display_weather(ha_data, display):
    # positions
    weather_left = 60
    weather_top = 392

    rain = entity_data(
        ha_data,
        "sensor.met_office_bury_st_edmunds_probability_of_precipitation_3_hourly",
    )[0]
    temp = entity_data(
        ha_data, "sensor.met_office_bury_st_edmunds_temperature_3_hourly"
    )[0]
    weather = entity_data(
        ha_data, "sensor.met_office_bury_st_edmunds_weather_3_hourly"
    )[0]

    display.draw.text(
        (weather_left, weather_top),
        f"{temp}°C",
        font=display.heading_font,
        fill=(0),
    )
    display.draw.text(
        (weather_left + 130, weather_top),
        f"{weather}",
        font=display.value_font,
        fill=(0),
    )
    display.draw.text(
        (weather_left + 130, weather_top + 55),
        f"{rain}% rain",
        font=display.suffix_font,
        fill=(0),
    )
