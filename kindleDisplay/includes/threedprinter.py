from kindleDisplay.includes.utils import entity_data, utc_to_local
from datetime import datetime
import pytz
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the default logging level to DEBUG


def display_3d_text(cur_percentage, est_finish_hhmm, cur_state, display):
    print_left = 590
    # if cur_state == "3D printer offline":  # Bodge for 3D printer offline
    #     print_left = 390
    print_top = 392

    display.draw.text(
        (print_left, print_top + 35),
        f"{cur_percentage}",
        font=display.value_font,
        fill=(0),
    )
    if est_finish_hhmm:
        display.draw.text(
            (print_left + 140, print_top + 50),
            f"({est_finish_hhmm})",
            font=display.suffix_font,
            fill=(0),
        )

    display.draw.text(
        (print_left, print_top),
        cur_state,
        font=display.suffix_font,
        fill=(0),
    )


def display_printer(ha_data, display):
    cur_state = entity_data(ha_data, "sensor.octoprint_current_state")[0].title()
    cur_state_display = f"3D printer {cur_state.lower()}"
    if cur_state == "Unavailable":
        cur_state_display = "3D printer offline"
    if cur_state == "Printing":
        cur_percentage = f"{'{:.1f}'.format(float(entity_data(ha_data, 'sensor.octoprint_job_percentage')[0]))}%"
        est_finished_time = entity_data(
            ha_data, "sensor.octoprint_estimated_finish_time"
        )[0]
        log.debug(f"Estimated finish time: {est_finished_time}")
        if est_finished_time.lower() != "unknown":
            est_finish_hhmm = utc_to_local(est_finished_time)
            log.debug(
                f"Estimated finish time (local): {utc_to_local(est_finished_time)}"
            )
        else:
            est_finish_hhmm = ""
        display_3d_text(cur_percentage, est_finish_hhmm, cur_state_display, display)
    else:
        display_3d_text("", "", cur_state_display, display)
