from kindleDisplay.includes.utils import entity_data

def display_rounded_rectangle(status_left,
                              status_top,
                              display):
    rect_x=status_left-20
    rect_y=status_top-32
    rect_width=92
    rect_height=75
    rect_xy=[(rect_x,rect_y), (rect_x + rect_width, rect_y + rect_height)]
    display.draw.rounded_rectangle(rect_xy, radius=8, fill=240, outline=None, width=1, corners=None)


def display_status_text(entity,
                        index,
                        status,
                        status_left,
                        status_top,
                        status_spacing,
                        display):
    x = status_left
    y = status_top + (index * status_spacing)

    # define some values
    device = entity[1]
    if status:
        colour = 64
    else:
        colour = 255
    display.draw.text(
        (x - 12, y - 32),
        device,
        font=display.suffix_font,
        fill=(colour),
    )
   

def display_status(ha_data, display):
    # position of things
    status_left = 915
    status_top = 450
    status_spacing = 32

    display_rounded_rectangle(status_left, status_top, display)
    for index, each_entity in enumerate(
        [
            ("binary_sensor.wireless_vm_ttyacm0", "ACM0"),
            ("binary_sensor.wireless_vm_ttyusb0", "USB0"),
        ]
    ):
        ha_status = entity_data(ha_data, each_entity[0])[0]
        if ha_status == "on":
            status = True
        else:
            status = False
        display_status_text(
            each_entity,
            index,
            status,
            status_left,
            status_top,
            status_spacing,
            display,
        )
