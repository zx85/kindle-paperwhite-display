from kindleDisplay.includes.utils import entity_data, entity_display


def display_presence_text(entity, index, presence, display):
    # position of things
    presence_left = 940
    presence_top = 110
    presence_spacing = 150
    x = presence_left
    y = presence_top + (index * presence_spacing)

    # define some values
    letter = entity[1]
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

    for index, each_entity in enumerate(
        [
            ("device_tracker.james_phone", " j"),
            ("device_tracker.beth_phone", "B"),
            ("device_tracker.chris_phone", "C"),
            ("device_tracker.lenni_phone", "L"),
        ]
    ):
        ha_presence = entity_data(ha_data, each_entity[0])[0]
        if ha_presence == "home":
            presence = True
        else:
            presence = False
        display_presence_text(
            each_entity,
            index,
            presence,
            display,
        )
