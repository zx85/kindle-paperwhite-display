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
    weather_left = 40
    weather_top = 392
    more_weather_data = next(
        (
            item
            for item in ha_data
            if item["entity_id"] == "sensor.local_current_weather"
        ),
        None,
    )
    log.debug(f"more weather data: {more_weather_data}")
    weather_data = next(
        (item for item in ha_data if item["entity_id"] == "weather.met_office_datahub"),
        None,
    )
    rain = more_weather_data.get("attributes").get("status").get("probOfPrecipitation")
    temp = str(round(float(weather_data.get("attributes").get("temperature"))))
    weather = weather_data.get("state")
    if weather == "partlycloudy":
        weather = "party cloudy"
    else:
        weather = "partly cloudy"
        # weather = weather.replace("-", " ")

    if weather != "unavailable":
        display.draw.text(
            (weather_left + 130, weather_top - 5),
            f"{weather}",
            font=display.value_font,
            fill=(0),
        )
        display.draw.text(
            (weather_left, weather_top),
            f"{temp}°C",
            font=display.heading_font,
            fill=(0),
        )
        display.draw.text(
            (weather_left + 130, weather_top + 55),
            f"{rain}% rain",
            font=display.suffix_font,
            fill=(0),
        )
    else:
        display.draw.text(
            (weather_left, weather_top),
            "weather unavailable",
            font=display.suffix_font,
            fill=(0),
        )
