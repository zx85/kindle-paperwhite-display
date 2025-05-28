from kindleDisplay.includes.utils import entity_data, entity_display
from datetime import datetime
import pytz
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the default logging level to DEBUG


def display_3d_text(cur_percentage, est_finish_hhmm, cur_state, display):
    print_left = 490
    if cur_state == "3D printer offline":  # Bodge for 3D printer offline
        print_left = 390
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


def display_printer(ha_data, display):
    cur_state = entity_data(ha_data, "sensor.octoprint_current_state")[0].title()
    if cur_state == "Unavailable":
        display_3d_text("", "", "3D printer offline", display)
    elif cur_state == "Printing":
        cur_percentage = f"{'{:.1f}'.format(float(entity_data(ha_data, 'sensor.octoprint_job_percentage')[0]))}%"
        est_finished_time = entity_data(
            ha_data, "sensor.octoprint_estimated_finish_time"
        )[0]
        log.debug(f"Estimated finish time: {est_finished_time}")
        if est_finished_time.lower() != "unknown":
            dt_utc = datetime.fromisoformat(est_finished_time)
            dt_utc = dt_utc.astimezone(pytz.utc)  # Ensure it's aware and in UTC
            dt_local = dt_utc.astimezone(pytz.timezone("Europe/London"))
            est_finish_hhmm = dt_local.strftime("%H:%M")
            log.debug(f"Estimated finish time (local): {est_finish_hhmm}")
        else:
            est_finish_hhmm = ""
        display_3d_text(cur_percentage, est_finish_hhmm, cur_state, display)
    else:
        display_3d_text("", "", cur_state, display)
