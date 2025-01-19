from flask import request, send_file
from kindleDisplay import app, ha_info
from PIL import Image, ImageFont, ImageDraw
import os
import json
import requests
import datetime


@app.route("/data", methods=["GET"])
def get_data():
    #
    ha_data = requests.get(
        ha_info["url"], headers={"Authorization": ha_info["key"]}
    ).json
    return send_file("images/kindle-data.png", mimetype="image/png")
