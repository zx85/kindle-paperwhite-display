from websocket import create_connection
from datetime import datetime, timedelta, date
import json


def display_calendar(display):
    # positioning
    calendar_left = 420
    calendar_top = 530

    ws_url = display.ha_info["url"].replace("http", "ws") + "/websocket"
    ws = create_connection(ws_url)

    message = {"type": "auth", "access_token": display.ha_info["key"]}

    ws.send(json.dumps(message))

    auth_result = ws.recv()
    auth_result = ws.recv()

    cal_message = {
        "type": "call_service",
        "domain": "calendar",
        "service": "get_events",
        "target": {"entity_id": "calendar.looking_forward"},
        "service_data": {
            "start_date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_date_time": (datetime.now() + timedelta(days=365)).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        },
        "id": 1,
        "return_response": True,
    }
    ws.send(json.dumps(cal_message))
    cal_result = json.loads(ws.recv())

    upcoming_events = [
        event
        for event in cal_result["result"]["response"]["calendar.looking_forward"][
            "events"
        ]
    ]

    for index, event in enumerate(upcoming_events):
        if index < 5:
            days_until_event = (
                datetime.strptime(event["start"], "%Y-%m-%d") - datetime.now()
            ).days + 1

            display.draw.text(
                (calendar_left, calendar_top + index * 40),
                f"{days_until_event} - {event['summary']}",
                font=display.suffix_font,
                fill=0,
            )
    ws.close()
