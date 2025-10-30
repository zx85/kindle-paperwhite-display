from kindleDisplay.includes.utils import entity_data
import pytz
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the default logging level to DEBUG


def display_octopus(ha_data, display):
  rate_left=570
  rate_top=16
  cur_rate = entity_data(ha_data, "sensor.octopus_energy_electricity_18p0906942_1012934837063_current_rate")[0]
  log.debug(f'Doing Octopus things: {cur_rate}')
  display.draw.text(
          (rate_left, rate_top),
          f'{int(float(cur_rate)*10000)/100}p',
          font=display.suffix_font,
          fill=(0),
      )