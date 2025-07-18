from PIL import Image, ImageFont, ImageDraw


class kindleDisplay:
    def __init__(self, ha_info):
        # pip install Pillow -  https://pillow.readthedocs.io/en/stable/
        self.ha_info = ha_info
        self.image = Image.new("L", (1026, 760), (255))
        self.draw = ImageDraw.Draw(self.image)
        # use a truetype font
        self.heading_font = ImageFont.truetype(
            "fonts/encode-sans/EncodeSansCompressed-700-Bold.ttf", 64
        )
        self.value_font = ImageFont.truetype(
            "fonts/encode-sans/EncodeSansCompressed-500-Medium.ttf", 48
        )
        self.suffix_font = ImageFont.truetype(
            "fonts/encode-sans/EncodeSansCondensed-300-Light.ttf", 32
        )

        self.weather_icons = [
            Image.open("images/weather-sunshine.png"),
            Image.open("images/weather-suncloud.png"),
            Image.open("images/weather-cloudsun.png"),
            Image.open("images/weather-cloud.png"),
            Image.open("images/weather-night.png"),
        ]
        self.mainsplug_icon = Image.open("images/mains-plug.png")
        self.pylon_icon = Image.open("images/pylon.png")
        self.uparrow_icon = Image.open("images/up-arrow.png")
        self.downarrow_icon = Image.open("images/down-arrow.png")
        self.noarrow_icon = Image.open("images/no-arrow.png")
        self.car_charging_icon = Image.open("images/carcharging-68x80.png")
        self.car_not_charging_icon = Image.open("images/carnotcharging-68x80.png")
        self.zap_icon = Image.open("images/zap-24x41.png")
        self.washing_machine_off = Image.open("images/washing-machine-off-63x80.png")
        self.washing_machine_on = Image.open("images/washing-machine-on-2-63x80.png")

        self.previous_timestamp = ""
        self.previous_battery = 50.0
        self.battery_direction_icon = self.noarrow_icon

    def clear_image(self):
        # Fill the image with white color for RGB images
        self.draw.rectangle([(0, 0), self.image.size], fill=(255))
