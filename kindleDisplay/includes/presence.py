from kindleDisplay.includes.utils import entity_data, entity_display


def display_presence_text(entity, presence, display):
    # define some values
    letter = entity[1]
    x = entity[2]
    y = entity[3]

    radius = 60
    if presence:
        colour = 64
    else:
        colour = 224
    twoPointList = [(x - radius, y - radius), (x + radius, y + radius)]
    display.draw.ellipse(twoPointList, fill=255, outline=colour, width=15)
    display.draw.text(
        (x - 18, y - 40),
        letter,
        font=display.heading_font,
        fill=(colour),
    )


def display_presence(ha_data, display):
    # position of things
    presence_left = 940

    for each_entity in [
        ("device_tracker.james_phone", " j", presence_left, 110),
        ("device_tracker.beth_phone", "B", presence_left, 250),
        ("device_tracker.chris_phone", "C", presence_left, 390),
        ("device_tracker.lenni_phone", "L", presence_left, 530),
    ]:
        ha_presence = entity_data(ha_data, each_entity[0])[0]
        if ha_presence == "home":
            presence = True
        else:
            presence = False
        display_presence_text(each_entity, presence, display)
