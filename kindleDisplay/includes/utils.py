# Function to find the dictionary with the specified entity_id
def entity_data(data, entity_id):
    entity = next((item for item in data if item["entity_id"] == entity_id), None)
    return (
        entity["state"],
        entity["attributes"]["unit_of_measurement"],
        entity["last_updated"],
    )


# Function to find the dictionary with the specified entity_id
def entity_display(data, entity_id):
    entity = next((item for item in data if item["entity_id"] == entity_id), None)
    value = entity["state"].replace("-", "")
    uom = entity["attributes"]["unit_of_measurement"]
    if uom == "W" or uom == "%":
        display_value = f"{int(float(value))}"
    elif uom == "kW" or uom == "kWh":
        display_value = f"{float(value):.1f}"
    else:
        display_value = value
    return f"{display_value}{uom}"
