import logging
from datetime import datetime
import pytz

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the default logging level to DEBUG


# Function to find the dictionary with the specified entity_id
def entity_data(data, entity_id):
    entity = next((item for item in data if item["entity_id"] == entity_id), None)
    if uom := entity["attributes"].get("unit_of_measurement"):
        return (
            entity["state"],
            uom,
            entity["last_updated"],
        )
    else:
        return (
            entity["state"],
            entity["last_updated"],
        )


# Function to find the dictionary with the specified entity_id
def entity_display(data, entity_id):
    log.debug(f"entity id: {entity_id}")
    entity = next((item for item in data if item["entity_id"] == entity_id), None)
    log.debug(f"entity state: {entity.get('state')}")
    if value := entity["state"].replace("-", ""):
        uom = entity["attributes"]["unit_of_measurement"]
        try:
            if uom == "W" or uom == "%":
                display_value = f"{int(float(value))}"
            elif uom == "kW" or uom == "kWh":
                display_value = f"{float(value):.1f}"
            else:
                display_value = value
        except:
            display_value = value if value != "unknown" else "unk"
        return f"{display_value}{uom}"
    else:
        return ""


def utc_to_local(utc, format="%H:%M"):
    log.debug(f"utc time: {utc}")
    dt_utc = datetime.fromisoformat(utc)
    dt_utc = dt_utc.astimezone(pytz.utc)  # Ensure it's aware and in UTC
    dt_local = dt_utc.astimezone(pytz.timezone("Europe/London"))
    local = dt_local.strftime(format)
    log.debug(f"local time: {local}")
    return local
