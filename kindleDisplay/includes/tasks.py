from websocket import create_connection
import json


def display_tasks(display):
    # positioning
    tasks_left = 40
    tasks_top = 530

    ws_url = display.ha_info["url"].replace("http", "ws") + "/websocket"
    ws = create_connection(ws_url)

    message = {"type": "auth", "access_token": display.ha_info["key"]}

    ws.send(json.dumps(message))
    result = ws.recv()
    result = ws.recv()
    message = {
        "type": "call_service",
        "domain": "todo",
        "service": "get_items",
        "target": {"entity_id": "todo.my_tasks"},
        "id": 1,
        "return_response": True,
    }
    ws.send(json.dumps(message))
    result = json.loads(ws.recv())
    # print("'%s'" % result)
    incomplete_tasks = [
        task
        for task in result["result"]["response"]["todo.my_tasks"]["items"]
        if task["status"] == "needs_action"
    ]

    for index, task in enumerate(incomplete_tasks):
        display.draw.text(
            (tasks_left, tasks_top + (index * 40)),
            task["summary"],
            font=display.suffix_font,
            fill=0,
        )
    ws.close()
