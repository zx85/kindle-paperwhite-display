from kindleDisplay.includes.utils import entity_data, entity_display

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the default logging level to DEBUG

def display_recording(ha_data, display):
    x = 760
    y = 304
    radius=45
    log.debug(f"Recording: {entity_data(ha_data, 'input_boolean.toggl_button')[0]}")
    recording = entity_data(ha_data, "input_boolean.toggl_button")[0]
    if recording == "on":
        log.debug('Recording is on')

        twoPointList = [(x - radius, y - radius), (x + radius, y + radius)]
        display.draw.ellipse(twoPointList, fill=96, outline=95, width=15)
        display.draw.text(
            (x - 28, y - 36),
            'rec',
            font=display.value_font,
            fill=224,
        )
