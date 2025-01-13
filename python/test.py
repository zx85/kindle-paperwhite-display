import sys

# pip install Pillow -  https://pillow.readthedocs.io/en/stable/
from PIL import Image, ImageFont, ImageDraw

image = Image.new("L", (1026, 760), (255))
draw = ImageDraw.Draw(image)

# use a truetype font
compressed_font = ImageFont.truetype(
    "fonts/encode-sans/EncodeSansCompressed-300-Light.ttf", 48
)
condensed_font = ImageFont.truetype(
    "fonts/encode-sans/EncodeSansCondensed-300-Light.ttf", 48
)

draw.text(
    (400, 80),
    "Preparing all the",
    font=compressed_font,
    fill=(0),
)
draw.text(
    (385, 180),
    "data for things.",
    font=condensed_font,
    fill=(0),
)
draw.line((9, 25, 9, 100), fill=128)

out = image.rotate(270, expand=True)  # degrees counter-clockwise
out.save("kindle-data.png", "PNG")
