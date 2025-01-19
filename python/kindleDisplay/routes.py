@app.route("/api/data", methods=["GET"])
def get_data():
    #
    ha_data = requests.get(
        ha_info["url"], headers={"Authorization": ha_info["key"]}
    ).json
    return send_file("images/kindle-data.png", mimetype="image/png")
