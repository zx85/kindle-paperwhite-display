def display_kindle_battery(kindle_battery, display):  # Kindle battery
    display.draw.text(
        (960, 715),
        f"{kindle_battery}%",
        font=display.suffix_font,
        fill=(0),
    )
