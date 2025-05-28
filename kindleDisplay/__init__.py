# import the necessary packages
from flask import Flask
from PIL import Image, ImageFont, ImageDraw
import os
import logging

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

app = Flask(__name__)

# configuration used to connect to MariaDB
# Database credentials for the conkers
ha_info = {"url": os.environ.get("URL").strip(), "key": os.environ.get("KEY").strip()}

from kindleDisplay import routes
