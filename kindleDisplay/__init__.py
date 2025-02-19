# import the necessary packages
from flask import Flask
import json
from PIL import Image, ImageFont, ImageDraw
import os

app = Flask(__name__)

# configuration used to connect to MariaDB
# Database credentials for the conkers
ha_info = {"url": os.environ.get("URL"), "key": os.environ.get("KEY")}

from kindleDisplay import routes
