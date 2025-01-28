from kindleDisplay.includes.utils import entity_data, entity_display
from datetime import datetime
import pytz


def display_3d_text(cur_percentage, est_finish_hhmm, cur_state, display):
    print_left = 490
    if cur_state == "3D printer offline":  # Bodge for 3D printer offline
        print_left = 400

    print_top = 392
    display.draw.text(
        (print_left, print_top),
        f"{cur_percentage}",
        font=display.heading_font,
        fill=(0),
    )
    display.draw.text(
        (print_left + 200, print_top),
        est_finish_hhmm,
        font=display.value_font,
        fill=(0),
    )
    display.draw.text(
        (print_left + 200, print_top + 55),
        cur_state,
        font=display.suffix_font,
        fill=(0),
    )


def display_3d_printer(ha_data, display):

    cur_state = entity_data(ha_data, "sensor.octoprint_current_state")[0].title()
    cur_percentage = f"{'{:.1f}'.format(float(entity_data(ha_data, 'sensor.octoprint_job_percentage')[0]))}%"
    est_finished_time = entity_data(ha_data, "sensor.octoprint_estimated_finish_time")[
        0
    ]
    if est_finished_time.lower() != "unknown":
        est_finish_hhmm = (
            datetime.fromisoformat(est_finished_time)
            .replace(tzinfo=pytz.timezone("Europe/London"))
            .strftime("%H:%M")
        )
    else:
        est_finish_hhmm = ""
    if cur_state == "Unavailable":
        display_3d_text("", "", "3D printer offline", display)
    elif cur_state == "Printing":
        display_3d_text(cur_percentage, est_finish_hhmm, cur_state, display)
    else:
        display_3d_text("", "", cur_state, display)
