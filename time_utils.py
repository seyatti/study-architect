

def convert_to_minutes(value, unit):
    if unit == "hours":
        return int(round(value * 60))
    else:
        return int(value)